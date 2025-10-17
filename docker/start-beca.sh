#!/bin/bash
# Quick start script for BECA Docker deployment

set -e

# Colors
GREEN='\033[0;32m'
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
echo "🚀 Starting BECA"
echo "=========================================="

# Start VM
echo "Starting VM: $INSTANCE_NAME..."
gcloud compute instances start $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE

echo ""
echo "Waiting for VM to be ready..."
sleep 15

# Get external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

echo -e "${GREEN}✓ BECA started successfully!${NC}"
echo ""
echo "=========================================="
echo "Access URLs (wait 30-60 seconds for startup):"
echo "=========================================="
echo "  BECA Frontend (React): http://$EXTERNAL_IP:3000"
echo "  BECA Backend (API):    http://$EXTERNAL_IP:8000/docs"
echo "  Ollama API:            http://$EXTERNAL_IP:11434"
echo "  Portainer:             http://$EXTERNAL_IP:9000"
echo "  MCP Server:            http://$EXTERNAL_IP:8080"
echo ""
echo "To check status:"
echo "  ./docker/status-beca.sh"
echo ""
echo "To view logs:"
echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo docker-compose -f /opt/beca/docker/docker-compose.yml logs -f'"
echo "=========================================="
