#!/bin/bash
# Check BECA Docker deployment status

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Load config
if [ -f "docker/.env" ]; then
    set -a
    source <(cat docker/.env | grep -v '^#' | grep -v '^$' | grep '=')
    set +a
fi

PROJECT_ID=${GCP_PROJECT_ID:-"beca-0001"}
ZONE=${GCP_ZONE:-"us-central1-b"}
INSTANCE_NAME=${GCP_INSTANCE_NAME:-"beca-ollama"}

echo "=========================================="
echo "📊 BECA Status"
echo "=========================================="

# Check VM status
echo "Checking VM status..."
VM_STATUS=$(gcloud compute instances describe $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --format="get(status)" 2>/dev/null || echo "NOT_FOUND")

if [ "$VM_STATUS" = "RUNNING" ]; then
    echo -e "VM Status: ${GREEN}RUNNING ✓${NC}"
    
    # Get external IP
    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --format="get(networkInterfaces[0].accessConfigs[0].natIP)")
    
    echo "External IP: $EXTERNAL_IP"
    echo ""
    
    # Check Docker containers
    echo "Checking Docker containers..."
    gcloud compute ssh $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --zone=$ZONE \
        --command="sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" \
        2>/dev/null || echo "Could not connect to VM"
    
    echo ""
    echo "=========================================="
    echo "Access URLs:"
    echo "=========================================="
    echo "  BECA Frontend (React): http://$EXTERNAL_IP:3000"
    echo "  BECA Backend (API):    http://$EXTERNAL_IP:8000/docs"
    echo "  Ollama API:            http://$EXTERNAL_IP:11434"
    echo "  Portainer:             http://$EXTERNAL_IP:9000"
    echo "  MCP Server:            http://$EXTERNAL_IP:8080"
    echo ""
    
    # Health checks
    echo "Health Checks:"
    
    # Check BECA Frontend
    if curl -s -f "http://$EXTERNAL_IP:3000/" > /dev/null 2>&1; then
        echo -e "  BECA Frontend: ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  BECA Frontend: ${RED}✗ Not responding${NC}"
    fi
    
    # Check BECA Backend
    if curl -s -f "http://$EXTERNAL_IP:8000/health" > /dev/null 2>&1; then
        echo -e "  BECA Backend:  ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  BECA Backend:  ${RED}✗ Not responding${NC}"
    fi
    
    # Check Ollama
    if curl -s -f "http://$EXTERNAL_IP:11434/" > /dev/null 2>&1; then
        echo -e "  Ollama API:    ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  Ollama API:    ${RED}✗ Not responding${NC}"
    fi
    
    # Check Portainer
    if curl -s -f "http://$EXTERNAL_IP:9000/" > /dev/null 2>&1; then
        echo -e "  Portainer:     ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  Portainer:     ${RED}✗ Not responding${NC}"
    fi
    
    # Check MCP Server
    if curl -s -f "http://$EXTERNAL_IP:8080/health" > /dev/null 2>&1; then
        echo -e "  MCP Server:    ${GREEN}✓ Healthy${NC}"
    else
        echo -e "  MCP Server:    ${RED}✗ Not responding${NC}"
    fi
    
elif [ "$VM_STATUS" = "TERMINATED" ]; then
    echo -e "VM Status: ${YELLOW}STOPPED${NC}"
    echo ""
    echo "VM is currently stopped. To start:"
    echo "  ./docker/start-beca.sh"
elif [ "$VM_STATUS" = "NOT_FOUND" ]; then
    echo -e "VM Status: ${RED}NOT FOUND${NC}"
    echo ""
    echo "VM does not exist. To deploy:"
    echo "  ./docker/deploy-gcp.sh"
else
    echo -e "VM Status: ${YELLOW}$VM_STATUS${NC}"
fi

echo "=========================================="
