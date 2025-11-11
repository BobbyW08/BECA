# BECA - AI-Powered Development Assistant

## Overview

BECA (Building Enhanced Coding Assistant) is an AI-powered development environment running on Google Cloud Platform. It features:

- **Eclipse Theia IDE** - Full-featured web-based IDE
- **BECA Chat** - Integrated AI assistant with Plan/Act modes
- **Ollama LLM** - Running qwen2.5-coder:7b-instruct and llama3.1:8b on VM with GPU
- **FastAPI Backend** - 39+ tools for code generation, file operations, and more
- **Docker-based Deployment** - All services containerized on GCP VM

## Architecture

```
Your Browser (http://VM_IP:3000)
        ↓
┌─────────────────────────────────────┐
│  GCP VM: beca-ollama                │
│  Zone: us-central1-b                │
│  Project: beca-0001                 │
├─────────────────────────────────────┤
│  Docker Containers:                 │
│  ├─ beca-frontend (Port 3000)       │
│  ├─ beca-backend (Port 8000)        │
│  ├─ mcp-server (Port 8080)          │
│  ├─ portainer (Port 9000)           │
│  └─ ollama-gpu (Port 11434)         │
│                                     │
│  VM Directory: /opt/beca            │
└─────────────────────────────────────┘
```

## Quick Start

### Start BECA
```bash
start-beca.bat
```
This will:
1. Start the GCP VM (if stopped)
2. Get the current external IP
3. Start Docker containers on the VM
4. Wait for services to be healthy
5. Open BECA in your browser

### Stop BECA (Save Costs)
```bash
stop-beca.bat
```
**Important:** Always stop the VM when done to minimize costs (~$0.17/hour running, ~$0.07/day stopped)

### Get Current VM IP
```bash
get-beca-ip.bat
```
The VM's external IP changes each time it starts (Spot instance)

### Diagnose Issues
```bash
diagnose-beca.bat
```
Shows VM status, IP, containers running, and connectivity

## Access URLs

After starting BECA, access these services (replace `VM_IP` with current IP from `get-beca-ip.bat`):

- **Theia IDE:** http://VM_IP:3000
- **Backend API:** http://VM_IP:8000/docs
- **Portainer:** http://VM_IP:9000
- **MCP Server:** http://VM_IP:8080
- **Ollama:** http://VM_IP:11434

## Using BECA

### Theia IDE Features
- **File Explorer:** Browse project files in `/workspace`
- **Code Editor:** Monaco editor (same as VS Code)
- **BECA Chat Panel:** Right sidebar - AI assistant
- **Integrated Terminal:** Built-in terminal access
- **Git Integration:** Source control built-in

### BECA Chat Modes
- **Plan Mode:** Discuss and plan solutions before implementation
- **Act Mode:** Execute changes and create files
- **Follow Mode:** Auto-opens files BECA modifies (eye icon)

## Project Structure

```
c:\dev/
├── api/                    # FastAPI backend
├── src/                    # Core BECA Python code
├── frontend-theia/         # Eclipse Theia IDE
├── docker/                 # Docker compose configs
├── scripts/                # Utility scripts
├── prompts/                # Prompt templates
├── data/                   # Database files
├── start-beca.bat          # Start VM and services
├── stop-beca.bat           # Stop VM
├── get-beca-ip.bat         # Get current IP
├── diagnose-beca.bat       # Diagnostic tool
└── setup-beca-autostart.sh # VM autostart config
```

## Troubleshooting

### Issue: Website won't load (connection refused)

**Possible causes:**
1. Docker containers not running on VM
2. Firewall ports not open
3. Services still starting up

**Solutions:**
```bash
# Check container status
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps"

# Manually start containers
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose up -d"

# Check logs
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-frontend"
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-backend"
```

### Issue: GCP Authentication Error

**Solution:**
```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project beca-0001

# Verify
gcloud config list
```

### Issue: Containers won't start

**Check Docker on VM:**
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b

# On VM:
sudo systemctl status docker
sudo docker ps -a
cd /opt/beca/docker
sudo docker-compose ps
sudo docker-compose logs
```

### Issue: Backend can't connect to Ollama

**Verify Ollama is running:**
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="curl http://localhost:11434/api/tags"
```

## VM Management

### SSH to VM
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b
```

### Check VM Status
```bash
gcloud compute instances list --filter="name=beca-ollama"
```

### View Container Logs
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs -f beca-frontend"
```

### Rebuild Containers
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b

# On VM:
cd /opt/beca/docker
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
```

## Cost Management

- **Running:** ~$0.17/hour (~$4/day)
- **Stopped:** ~$0.07/day (disk storage only)

**Always stop the VM when done working:**
```bash
stop-beca.bat
```

## Development Workflow

1. **Start BECA:** Run `start-beca.bat`
2. **Access IDE:** Open http://VM_IP:3000 in browser
3. **Use BECA Chat:** Ask questions, plan features, generate code
4. **Review Changes:** Follow Mode auto-opens modified files
5. **Stop VM:** Run `stop-beca.bat` when done

## Models

BECA uses dual models on the VM:
- **qwen2.5-coder:7b-instruct** - Primary coding model
- **llama3.1:8b** - General reasoning
- **Automatic selection** based on task type

## Support

### Check Logs
```bash
diagnose-beca.bat
```

### Manual Container Start
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose up -d"
```

### Firewall Rules
Ensure these ports are open in GCP:
- TCP 3000 (Frontend)
- TCP 8000 (Backend)
- TCP 9000 (Portainer)
- TCP 8080 (MCP)
- TCP 11434 (Ollama)

## Notes

- VM uses Spot instance (cheaper, IP changes on restart)
- Code lives at `/opt/beca` on VM
- Local `c:\dev` is for development and deployment scripts
- Docker containers auto-update via Watchtower (checks every 5 minutes)

## GitHub Repository

https://github.com/BobbyW08/BECA.git
