#!/usr/bin/env python3
"""
Script to set up firewall for BECA Ollama VM
Allows access to Ollama API (port 11434) from your current IP
"""
import subprocess
import sys
import urllib.request

def get_public_ip():
    """Get current public IP address"""
    try:
        with urllib.request.urlopen('https://api.ipify.org') as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error getting public IP: {e}")
        sys.exit(1)

def run_command(cmd):
    """Execute command and return result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def setup_firewall():
    """Create firewall rule to allow Ollama access from current IP"""
    print("Getting your public IP...")
    my_ip = get_public_ip()
    print(f"Your IP: {my_ip}")

    print("\nCreating firewall rule...")

    cmd = [
        "gcloud", "compute", "firewall-rules", "create", "allow-ollama-from-home",
        "--project=beca-0001",
        "--direction=INGRESS",
        "--priority=1000",
        "--network=default",
        "--action=ALLOW",
        "--rules=tcp:11434",
        f"--source-ranges={my_ip}/32",
        "--target-tags=ollama-server",
        "--description=Allow Ollama API access from home IP"
    ]

    run_command(cmd)

    print("\nFirewall rule created! Ollama port 11434 is now accessible from your IP.")

if __name__ == "__main__":
    setup_firewall()
