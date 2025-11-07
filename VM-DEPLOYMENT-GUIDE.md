# BECA VM Deployment Guide

## Quick Start - Deploy Theia IDE to VM

This guide explains how to deploy the updated BECA with Theia IDE to your GCP VM.

## What Changed

- ✅ Migrated from React frontend to **Eclipse Theia IDE**
- ✅ Removed all legacy React components
- ✅ Updated all batch scripts
- ✅ docker-compose.yml already configured for Theia
- ✅ All ports remain the same (Port 3000 = Theia IDE)

## Prerequisites

- GCP VM: `beca-ollama` in zone `us-central1-b`
- Git configured with push access to repository
- VM must have Docker and Docker Compose installed

## Deployment Steps

### Step 1: Commit and Push Changes

```bash
# From your local c:\dev directory
git add .
git commit -m "Migrate to Theia IDE, remove React frontend and legacy files"
git push origin main
```

### Step 2: SSH to VM

```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --project=beca-0001
```

### Step 3: Pull Latest Code

```bash
cd /opt/beca
sudo git pull origin main
```

### Step 4: Stop Old Containers

```bash
sudo docker-compose -f docker/docker-compose.yml down
```

This will stop all running containers cleanly.

### Step 5: Build New Containers

```bash
sudo docker-compose -f docker/docker-compose.yml build
```

**Note**: Building the Theia frontend will take 5-10 minutes the first time as it:
- Installs Node.js dependencies
- Compiles TypeScript
- Builds the Theia application
- Creates the Docker image

### Step 6: Start New Stack

```bash
sudo docker-compose -f docker/docker-compose.yml up -d
```

### Step 7: Verify Deployment

```bash
# Check all containers are running
sudo docker ps

# Check Theia frontend logs
sudo docker logs beca-frontend -f

# Check backend logs
sudo docker logs beca-backend -f
```

**Expected containers**:
- `beca-frontend` (Theia IDE)
- `beca-backend` (FastAPI)
- `ollama-gpu` (LLM inference)
- `mcp-server` (Claude integration)
- `portainer` (Docker management)

### Step 8: Test Access

Exit SSH and run from your local machine:

```batch
start-beca.bat
```

This will:
1. Start the VM (if stopped)
2. Get the current external IP
3. Wait for services to be healthy
4. Open Theia IDE in your browser

**Access URLs**:
- Theia IDE: `http://YOUR_VM_IP:3000`
- Backend API: `http://YOUR_VM_IP:8000/docs`
- Portainer: `http://YOUR_VM_IP:9000`
- MCP Server: `http://YOUR_VM_IP:8080`

## Troubleshooting

### Container Build Fails

```bash
# Check Docker is running
sudo systemctl status docker

# Check available disk space
df -h

# View build logs
sudo docker-compose -f docker/docker-compose.yml build --no-cache
```

### Theia Frontend Won't Start

```bash
# Check logs
sudo docker logs beca-frontend

# Common issues:
# - Port 3000 already in use
# - Out of memory
# - Build failed

# Try rebuild
sudo docker-compose -f docker/docker-compose.yml build --no-cache beca-frontend
sudo docker-compose -f docker/docker-compose.yml up -d beca-frontend
```

### Backend Can't Connect to Ollama

```bash
# Check Ollama is running
sudo docker logs ollama-gpu

# Check network
sudo docker network ls
sudo docker network inspect beca-network

# Restart backend
sudo docker-compose -f docker/docker-compose.yml restart beca-backend
```

### Port 3000 Not Accessible

```bash
# Check firewall rules
gcloud compute firewall-rules list --filter="name:beca"

# Should see:
# - beca-frontend: tcp:3000
# - beca-backend: tcp:8000
# - beca-portainer: tcp:9000
# - beca-mcp: tcp:8080

# If missing, create firewall rule:
gcloud compute firewall-rules create beca-frontend \
  --allow=tcp:3000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=beca-server \
  --description="Allow BECA Theia IDE access" \
  --project=beca-0001
```

## Architecture Overview

```
┌─────────────────────────────────────────┐
│  Your Browser                           │
│  http://VM_IP:3000                      │
└────────────────┬────────────────────────┘
                 │ HTTPS
                 ▼
┌─────────────────────────────────────────┐
│  GCP VM (beca-ollama)                   │
│  Docker Compose Stack                   │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────┐    │
│  │ beca-frontend (Theia IDE)      │    │
│  │ Port: 3000                     │    │
│  │ - BECA Chat Panel              │    │
│  │ - Code Editor (Monaco)         │    │
│  │ - File Explorer                │    │
│  │ - Integrated Terminal          │    │
│  └─────────────┬──────────────────┘    │
│                │                        │
│  ┌─────────────▼──────────────────┐    │
│  │ beca-backend (FastAPI)         │    │
│  │ Port: 8000                     │    │
│  │ - LangChain Agent              │    │
│  │ - 39+ Tools                    │    │
│  │ - Plan/Act Modes               │    │
│  └─────────────┬──────────────────┘    │
│                │                        │
│  ┌─────────────▼──────────────────┐    │
│  │ ollama-gpu (LLM Engine)        │    │
│  │ Port: 11434                    │    │
│  │ - llama3.1:8b                  │    │
│  │ - qwen2.5-coder:7b-instruct   │    │
│  │ - NVIDIA T4 GPU                │    │
│  └────────────────────────────────┘    │
│                                         │
│  Other Services:                        │
│  - mcp-server (port 8080)              │
│  - portainer (port 9000)               │
└─────────────────────────────────────────┘
```

## Post-Deployment

### Using Theia IDE

1. **Access IDE**: Open `http://VM_IP:3000` in your browser
2. **BECA Chat**: Look for BECA chat panel on the right sidebar
3. **Plan/Act Toggle**: Switch between planning and execution modes
4. **Follow Mode**: Enable to auto-open files BECA modifies
5. **Terminal**: Built-in terminal for running commands
6. **File Explorer**: Browse and edit files in `/workspace`

### Testing BECA

```batch
# From local machine
test-agent.bat
```

This will:
1. Check backend health
2. Send a test request
3. Display response

### Daily Usage

**Start BECA**:
```batch
start-beca.bat
```

**Stop BECA** (save costs):
```batch
stop-beca.bat
```

**Get Current IP**:
```batch
get-beca-ip.bat
```

**Validate Services**:
```batch
validate-startup.bat
```

## Cost Management

- **Running**: ~$0.17/hour (~$4/day)
- **Stopped**: ~$0.07/day (disk only)

**Always stop the VM when done!**

## Next Steps

1. ✅ Deploy Theia to VM (this guide)
2. Test Theia IDE functionality
3. Set up Claude Desktop MCP integration (optional)
4. Configure multi-user access (future)

## Support

If you encounter issues:

1. Check logs: `sudo docker logs beca-frontend`
2. Run diagnostics: `diagnose-beca.bat`
3. Check connection: `diagnose-connection.bat`
4. Verify firewall: `gcloud compute firewall-rules list --filter="name:beca"`

## Summary

After following this guide:
- ✅ Theia IDE running on VM at port 3000
- ✅ BECA backend connected to Theia
- ✅ All services healthy and accessible
- ✅ Ready for development and testing
- ✅ No more React frontend references

**Important**: The external IP changes each time you start the VM (SPOT instance). Always run `get-beca-ip.bat` or `start-beca.bat` to get the current IP.
