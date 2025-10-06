# Script to create BECA Ollama VM once GPU quota is approved

$env:PATH = "$env:PATH;C:\dev\google-cloud-sdk\bin"

Write-Host "Creating BECA Ollama VM with T4 GPU..." -ForegroundColor Cyan

gcloud compute instances create beca-ollama `
  --project=beca-0001 `
  --zone=us-central1-c `
  --machine-type=n1-standard-2 `
  --accelerator=type=nvidia-tesla-t4,count=1 `
  --provisioning-model=SPOT `
  --instance-termination-action=DELETE `
  --maintenance-policy=TERMINATE `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --boot-disk-size=30GB `
  --boot-disk-type=pd-standard `
  --tags=ollama-server `
  --metadata=startup-script='#!/bin/bash
# Install NVIDIA drivers
apt-get update
apt-get install -y ubuntu-drivers-common
ubuntu-drivers autoinstall

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Configure Ollama for remote access
mkdir -p /etc/systemd/system/ollama.service.d
cat > /etc/systemd/system/ollama.service.d/override.conf <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# Reload and restart
systemctl daemon-reload
systemctl enable ollama
systemctl restart ollama

# Pull the model
sleep 30
ollama pull llama3.1:8b
'

Write-Host ""
Write-Host "VM creation started! This will take 5-10 minutes." -ForegroundColor Green
Write-Host "The startup script will automatically:"
Write-Host "  1. Install NVIDIA drivers"
Write-Host "  2. Install Ollama"
Write-Host "  3. Configure Ollama for remote access"
Write-Host "  4. Pull llama3.1:8b model"
Write-Host ""
Write-Host "You can check status with:"
Write-Host "  gcloud compute instances list --project=beca-0001"
