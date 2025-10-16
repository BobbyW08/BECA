#!/bin/bash
# Deploy BECA Docker Stack to Existing VM
# Uses your existing beca-ollama VM instead of creating a new one

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration - using existing VM
PROJECT_ID="beca-0001"
ZONE="us-central1-b"
INSTANCE_NAME="beca-ollama"  # Your existing VM

echo "=========================================="
echo "🚀 BECA Docker Deployment"
echo "   To Existing VM: $INSTANCE_NAME"
echo "=========================================="
echo "Project: $PROJECT_ID"
echo "Zone: $ZONE"
echo "VM: $INSTANCE_NAME"
echo "=========================================="
echo ""

# Function to check if VM is running
check_vm_status() {
    echo "Checking VM status..."
    STATUS=$(gcloud compute instances describe $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --format="get(status)" 2>/dev/null || echo "NOT_FOUND")
    
    if [ "$STATUS" = "NOT_FOUND" ]; then
        echo -e "${RED}Error: VM '$INSTANCE_NAME' not found${NC}"
        echo "Please check the VM name and zone in this script."
        exit 1
    fi
    
    echo -e "${GREEN}✓ VM found: $STATUS${NC}"
    echo "$STATUS"
}

# Function to start VM if stopped
start_vm() {
    STATUS=$1
    if [ "$STATUS" = "TERMINATED" ]; then
        echo ""
        echo "VM is stopped. Starting..."
        gcloud compute instances start $INSTANCE_NAME \
            --project=$PROJECT_ID \
            --zone=$ZONE
        
        echo "Waiting for VM to be ready..."
        sleep 30
        echo -e "${GREEN}✓ VM started${NC}"
    else
        echo -e "${GREEN}✓ VM already running${NC}"
    fi
}

# Function to install Docker on VM
install_docker() {
    echo ""
    echo "Installing Docker on VM..."
    
    gcloud compute ssh $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --command='
            # Check if Docker is already installed
            if command -v docker &> /dev/null; then
                echo "✓ Docker already installed"
                docker --version
            else
                echo "Installing Docker..."
                curl -fsSL https://get.docker.com -o get-docker.sh
                sudo sh get-docker.sh
                sudo systemctl enable docker
                sudo systemctl start docker
                rm get-docker.sh
                echo "✓ Docker installed"
            fi
            
            # Check Docker Compose
            if command -v docker-compose &> /dev/null; then
                echo "✓ Docker Compose already installed"
                docker-compose --version
            else
                echo "Installing Docker Compose..."
                sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose
                echo "✓ Docker Compose installed"
            fi
        '
    
    echo -e "${GREEN}✓ Docker setup complete${NC}"
}

# Function to copy BECA files to VM
copy_files() {
    echo ""
    echo "Copying BECA files to VM..."
    
    # Create temp directory on VM
    gcloud compute ssh $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --command='sudo mkdir -p /opt/beca && sudo chmod 777 /opt/beca'
    
    # Copy directories
    echo "  Copying docker/ directory..."
    gcloud compute scp --recurse docker/ $INSTANCE_NAME:/opt/beca/ \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --quiet 2>/dev/null || echo "Warning: Some files may have been skipped"
    
    echo "  Copying src/ directory..."
    gcloud compute scp --recurse src/ $INSTANCE_NAME:/opt/beca/ \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --quiet 2>/dev/null || echo "Warning: Some files may have been skipped"
    
    echo "  Copying prompts/ directory..."
    gcloud compute scp --recurse prompts/ $INSTANCE_NAME:/opt/beca/ \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --quiet 2>/dev/null || echo "Warning: Some files may have been skipped"
    
    # Copy Python files and databases
    echo "  Copying Python files and databases..."
    gcloud compute scp beca_gui.py requirements.txt *.db $INSTANCE_NAME:/opt/beca/ \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --quiet 2>/dev/null || true
    
    echo -e "${GREEN}✓ Files copied${NC}"
}

# Function to start Docker containers
start_containers() {
    echo ""
    echo "Starting Docker containers..."
    
    gcloud compute ssh $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --command='
            cd /opt/beca
            
            # Stop any existing containers
            sudo docker-compose -f docker/docker-compose.yml down 2>/dev/null || true
            
            # Start containers
            sudo docker-compose -f docker/docker-compose.yml up -d
            
            echo ""
            echo "Waiting for containers to start..."
            sleep 10
            
            echo ""
            echo "Container status:"
            sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        '
    
    echo -e "${GREEN}✓ Containers started${NC}"
}

# Function to get access information
show_access_info() {
    echo ""
    echo "Getting VM external IP..."
    
    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --format="get(networkInterfaces[0].accessConfigs[0].natIP)")
    
    echo ""
    echo "=========================================="
    echo "✅ Deployment Complete!"
    echo "=========================================="
    echo ""
    echo "Access URLs:"
    echo "  BECA GUI:  http://$EXTERNAL_IP:7860"
    echo "  Portainer: http://$EXTERNAL_IP:9000"
    echo "  MCP Server: http://$EXTERNAL_IP:8080"
    echo ""
    echo "Note: Wait 2-3 minutes for containers to fully start"
    echo "      and for Ollama models to load."
    echo ""
    echo "To check container status:"
    echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo docker ps'"
    echo ""
    echo "To view logs:"
    echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo docker-compose -f /opt/beca/docker/docker-compose.yml logs'"
    echo ""
    echo "To stop BECA (save costs):"
    echo "  gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE"
    echo ""
    echo "=========================================="
}

# Main execution
main() {
    # Check VM exists and get status
    VM_STATUS=$(check_vm_status)
    
    # Start VM if needed
    start_vm "$VM_STATUS"
    
    # Install Docker
    install_docker
    
    # Copy BECA files
    copy_files
    
    # Start containers
    start_containers
    
    # Show access information
    show_access_info
}

# Run main function
main
