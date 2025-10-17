#!/bin/bash
# BECA Docker Deployment to Google Cloud Platform
# Automates creation and deployment of BECA stack to GCP with GPU support

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load configuration from .env
if [ -f "docker/.env" ]; then
    echo -e "${GREEN}Loading configuration from .env...${NC}"
    # Use set -a to automatically export variables, handle comments and empty lines properly
    set -a
    source <(cat docker/.env | grep -v '^#' | grep -v '^$' | grep '=')
    set +a
else
    echo -e "${YELLOW}No .env file found. Using defaults from .env.example${NC}"
    set -a
    source <(cat docker/.env.example | grep -v '^#' | grep -v '^$' | grep '=')
    set +a
fi

# Default values
PROJECT_ID=${GCP_PROJECT_ID:-"beca-0001"}
ZONE=${GCP_ZONE:-"us-central1-b"}
INSTANCE_NAME=${GCP_INSTANCE_NAME:-"beca-ollama"}
MACHINE_TYPE=${GCP_MACHINE_TYPE:-"n1-standard-4"}
GPU_TYPE=${GCP_GPU_TYPE:-"nvidia-tesla-t4"}
GPU_COUNT=${GCP_GPU_COUNT:-1}
BOOT_DISK_SIZE=${GCP_BOOT_DISK_SIZE:-100}
USE_SPOT=${GCP_USE_SPOT:-true}

echo "=========================================="
echo "🚀 BECA GCP Deployment Script"
echo "=========================================="
echo "Project: $PROJECT_ID"
echo "Zone: $ZONE"
echo "Instance: $INSTANCE_NAME"
echo "Machine Type: $MACHINE_TYPE"
echo "GPU: $GPU_TYPE (${GPU_COUNT}x)"
echo "Disk Size: ${BOOT_DISK_SIZE}GB"
echo "SPOT Instance: $USE_SPOT"
echo "=========================================="
echo ""

# Function to check if gcloud is installed
check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}Error: gcloud CLI not found. Please install Google Cloud SDK.${NC}"
        echo "Visit: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    echo -e "${GREEN}✓ gcloud CLI found${NC}"
}

# Function to set GCP project
set_project() {
    echo ""
    echo "Setting GCP project..."
    gcloud config set project $PROJECT_ID
    echo -e "${GREEN}✓ Project set to $PROJECT_ID${NC}"
}

# Function to enable required APIs
enable_apis() {
    echo ""
    echo "Enabling required GCP APIs..."
    gcloud services enable compute.googleapis.com --project=$PROJECT_ID
    gcloud services enable container.googleapis.com --project=$PROJECT_ID
    echo -e "${GREEN}✓ APIs enabled${NC}"
}

# Function to create startup script
create_startup_script() {
    echo ""
    echo "Creating VM startup script..."
    
    cat > /tmp/beca-startup.sh << 'EOF'
#!/bin/bash
# BECA Docker VM Startup Script
# Runs on VM boot to set up Docker environment

set -e

echo "=========================================="
echo "BECA VM Startup Script"
echo "=========================================="

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✓ Docker installed"
else
    echo "✓ Docker already installed"
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✓ Docker Compose installed"
else
    echo "✓ Docker Compose already installed"
fi

# Install NVIDIA Container Toolkit (for GPU support)
echo "Installing NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
apt-get install -y nvidia-container-toolkit
systemctl restart docker
echo "✓ NVIDIA Container Toolkit installed"

# Create BECA directory
mkdir -p /opt/beca
cd /opt/beca

# Clone BECA repository (or copy files if already present)
if [ ! -d ".git" ]; then
    echo "Cloning BECA repository..."
    # Note: Replace with your actual repo URL
    # git clone https://github.com/yourusername/beca.git .
    echo "Note: Repository cloning skipped. Upload files manually or via deployment script."
fi

# Create .env file from metadata
cat > docker/.env << ENVEOF
MCP_AUTH_TOKEN=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/mcp-token 2>/dev/null || echo "beca-default-token")
OLLAMA_URL=http://ollama-gpu:11434
GCP_PROJECT_ID=$PROJECT_ID
GCP_ZONE=$ZONE
ENVEOF

# Pull Ollama models on first boot
if [ ! -f "/opt/beca/.models-pulled" ]; then
    echo "Pulling Ollama models on first boot..."
    echo "This will happen after containers start..."
    cat > /opt/beca/pull-models.sh << 'MODELEOF'
#!/bin/bash
sleep 60  # Wait for Ollama to start
docker exec ollama-gpu ollama pull llama3.1:8b
docker exec ollama-gpu ollama pull qwen2.5-coder:7b-instruct
touch /opt/beca/.models-pulled
MODELEOF
    chmod +x /opt/beca/pull-models.sh
    nohup /opt/beca/pull-models.sh &
fi

# Start Docker Compose stack
echo "Starting BECA Docker stack..."
cd /opt/beca
docker-compose -f docker/docker-compose.yml up -d

echo "=========================================="
echo "✓ BECA startup complete!"
echo "=========================================="
echo "Access BECA Frontend: http://$(curl -s ifconfig.me):3000"
echo "Access BECA Backend:  http://$(curl -s ifconfig.me):8000"
echo "Portainer at: http://$(curl -s ifconfig.me):9000"
echo "MCP Server at: http://$(curl -s ifconfig.me):8080"
echo "=========================================="
EOF

    echo -e "${GREEN}✓ Startup script created${NC}"
}

# Function to create firewall rules
create_firewall_rules() {
    echo ""
    echo "Creating firewall rules..."
    
    # Get current IP
    CURRENT_IP=$(curl -s ifconfig.me)
    ALLOWED_IP=${ALLOWED_IP:-"$CURRENT_IP/32"}
    
    echo "Allowing access from: $ALLOWED_IP"
    
    # BECA Frontend (React)
    gcloud compute firewall-rules create beca-frontend \
        --project=$PROJECT_ID \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:3000 \
        --source-ranges=$ALLOWED_IP \
        --target-tags=beca-server \
        --description="Allow BECA React Frontend access" \
        2>/dev/null || echo "Firewall rule 'beca-frontend' already exists"
    
    # BECA Backend (FastAPI)
    gcloud compute firewall-rules create beca-backend \
        --project=$PROJECT_ID \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:8000 \
        --source-ranges=$ALLOWED_IP \
        --target-tags=beca-server \
        --description="Allow BECA FastAPI Backend access" \
        2>/dev/null || echo "Firewall rule 'beca-backend' already exists"
    
    # Portainer
    gcloud compute firewall-rules create beca-portainer \
        --project=$PROJECT_ID \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:9000,tcp:9443 \
        --source-ranges=$ALLOWED_IP \
        --target-tags=beca-server \
        --description="Allow Portainer access" \
        2>/dev/null || echo "Firewall rule 'beca-portainer' already exists"
    
    # MCP Server
    gcloud compute firewall-rules create beca-mcp \
        --project=$PROJECT_ID \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:8080 \
        --source-ranges=$ALLOWED_IP \
        --target-tags=beca-server \
        --description="Allow MCP Server access" \
        2>/dev/null || echo "Firewall rule 'beca-mcp' already exists"
    
    # HTTP/HTTPS (for nginx proxy)
    gcloud compute firewall-rules create beca-web \
        --project=$PROJECT_ID \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:80,tcp:443 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=beca-server \
        --description="Allow HTTP/HTTPS access" \
        2>/dev/null || echo "Firewall rule 'beca-web' already exists"
    
    echo -e "${GREEN}✓ Firewall rules created${NC}"
}

# Function to create VM instance
create_instance() {
    echo ""
    echo "Creating GCP VM instance..."
    
    # Build command
    CMD="gcloud compute instances create $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --accelerator=type=$GPU_TYPE,count=$GPU_COUNT \
        --maintenance-policy=TERMINATE \
        --image-family=cos-stable \
        --image-project=cos-cloud \
        --boot-disk-size=${BOOT_DISK_SIZE}GB \
        --boot-disk-type=pd-ssd \
        --metadata-from-file=startup-script=/tmp/beca-startup.sh \
        --metadata=mcp-token=$(openssl rand -hex 32) \
        --tags=beca-server \
        --scopes=cloud-platform"
    
    # Add SPOT flag if enabled
    if [ "$USE_SPOT" = "true" ]; then
        CMD="$CMD --provisioning-model=SPOT --instance-termination-action=STOP"
    fi
    
    # Execute command
    if $CMD; then
        echo -e "${GREEN}✓ VM instance created successfully${NC}"
    else
        echo -e "${RED}Error creating VM instance${NC}"
        exit 1
    fi
}

# Function to wait for VM to be ready
wait_for_vm() {
    echo ""
    echo "Waiting for VM to be ready..."
    
    for i in {1..30}; do
        STATUS=$(gcloud compute instances describe $INSTANCE_NAME \
            --project=$PROJECT_ID \
            --zone=$ZONE \
            --format="get(status)" 2>/dev/null || echo "")
        
        if [ "$STATUS" = "RUNNING" ]; then
            echo -e "${GREEN}✓ VM is running${NC}"
            sleep 10  # Wait a bit more for startup script
            return 0
        fi
        
        echo "Waiting... ($i/30)"
        sleep 10
    done
    
    echo -e "${RED}Timeout waiting for VM${NC}"
    exit 1
}

# Function to get VM details
get_vm_details() {
    echo ""
    echo "=========================================="
    echo "VM Details"
    echo "=========================================="
    
    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --format="get(networkInterfaces[0].accessConfigs[0].natIP)")
    
    echo "Instance Name: $INSTANCE_NAME"
    echo "External IP: $EXTERNAL_IP"
    echo ""
    echo "Access URLs:"
    echo "  BECA Frontend: http://$EXTERNAL_IP:3000"
    echo "  BECA Backend:  http://$EXTERNAL_IP:8000"
    echo "  Portainer:     http://$EXTERNAL_IP:9000"
    echo "  MCP Server:    http://$EXTERNAL_IP:8080"
    echo ""
    echo "SSH Command:"
    echo "  gcloud compute ssh $INSTANCE_NAME --project=$PROJECT_ID --zone=$ZONE"
    echo "=========================================="
}

# Main execution
main() {
    check_gcloud
    set_project
    enable_apis
    create_startup_script
    create_firewall_rules
    create_instance
    wait_for_vm
    get_vm_details
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✅ Deployment Complete!"
    echo "==========================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Wait 2-3 minutes for Docker setup to complete"
    echo "2. SSH into VM: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
    echo "3. Check Docker status: sudo docker ps"
    echo "4. View logs: sudo docker-compose -f /opt/beca/docker/docker-compose.yml logs"
    echo ""
    echo "To upload BECA files to VM:"
    echo "  gcloud compute scp --recurse . $INSTANCE_NAME:/opt/beca --zone=$ZONE"
    echo ""
    echo "To stop VM (save costs):"
    echo "  gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE"
    echo ""
}

# Run main function
main
