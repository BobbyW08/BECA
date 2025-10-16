#!/bin/bash
# Stop BECA Docker deployment to save costs

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
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
echo "⏸️  Stopping BECA"
echo "=========================================="

# Stop VM
echo "Stopping VM: $INSTANCE_NAME..."
gcloud compute instances stop $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE

echo -e "${GREEN}✓ BECA stopped successfully!${NC}"
echo ""
echo "=========================================="
echo "💰 Cost Savings Active"
echo "=========================================="
echo "VM is now stopped. You are only charged for:"
echo "  - Disk storage: ~\$0.07/day"
echo "  - No compute or GPU charges!"
echo ""
echo "To start BECA again:"
echo "  ./docker/start-beca.sh"
echo "=========================================="
