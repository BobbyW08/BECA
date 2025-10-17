#!/usr/bin/env python3
"""
Script to create BECA Ollama VM with T4 GPU on Google Cloud
"""
import subprocess
import sys

def run_command(cmd):
    """Execute command and return result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def create_vm():
    """Create BECA Ollama VM with SPOT instance and T4 GPU"""
    print("Creating BECA Ollama VM with T4 GPU...")

    startup_script = """#!/bin/bash
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
"""

    cmd = [
        "gcloud", "compute", "instances", "create", "beca-ollama",
        "--project=beca-0001",
        "--zone=us-central1-c",
        "--machine-type=n1-standard-2",
        "--accelerator=type=nvidia-tesla-t4,count=1",
        "--provisioning-model=SPOT",
        "--instance-termination-action=DELETE",
        "--maintenance-policy=TERMINATE",
        "--image-family=ubuntu-2204-lts",
        "--image-project=ubuntu-os-cloud",
        "--boot-disk-size=30GB",
        "--boot-disk-type=pd-standard",
        "--tags=ollama-server",
        f"--metadata=startup-script={startup_script}"
    ]

    run_command(cmd)

    print("\nVM creation started! This will take 5-10 minutes.")
    print("The startup script will automatically:")
    print("  1. Install NVIDIA drivers")
    print("  2. Install Ollama")
    print("  3. Configure Ollama for remote access")
    print("  4. Pull llama3.1:8b model")
    print("\nYou can check status with:")
    print("  gcloud compute instances list --project=beca-0001")

if __name__ == "__main__":
    create_vm()
