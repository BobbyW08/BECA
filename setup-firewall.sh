#!/bin/bash
# Script to set up firewall for BECA Ollama VM

export PATH="$PATH:/c/dev/google-cloud-sdk/bin"

echo "Getting your public IP..."
MY_IP=$(curl -s https://api.ipify.org)
echo "Your IP: $MY_IP"

echo ""
echo "Creating firewall rule..."

gcloud compute firewall-rules create allow-ollama-from-home \
  --project=beca-0001 \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:11434 \
  --source-ranges="$MY_IP/32" \
  --target-tags=ollama-server \
  --description="Allow Ollama API access from home IP"

echo ""
echo "Firewall rule created! Ollama port 11434 is now accessible from your IP."
