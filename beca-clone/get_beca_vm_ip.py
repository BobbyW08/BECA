#!/usr/bin/env python3
"""
Get the current external IP of the BECA Ollama VM.
This is needed because the VM is preemptible and gets a new IP each time it restarts.
"""
import subprocess
import sys

def get_vm_ip(project="beca-0001", instance="beca-ollama"):
    """Get the external IP of the BECA VM."""
    try:
        result = subprocess.run(
            [
                "gcloud", "compute", "instances", "describe",
                instance,
                f"--project={project}",
                "--format=get(networkInterfaces[0].accessConfigs[0].natIP)"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        ip = result.stdout.strip()
        if ip:
            return ip
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: gcloud CLI not found. Please install Google Cloud SDK.", file=sys.stderr)
        return None

if __name__ == "__main__":
    ip = get_vm_ip()
    if ip:
        print(ip)
        sys.exit(0)
    else:
        print("Failed to get VM IP", file=sys.stderr)
        sys.exit(1)
