# BECA Docker Deployment Guide

Complete guide for deploying BECA to Google Cloud Platform using Docker containers.

## 🎯 Overview

This Docker deployment transforms BECA into a fully containerized, cloud-native system that can be managed from any device including iPad, laptop, or desktop.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Any Device (iPad/Laptop/Desktop)                       │
│  ┌────────────────┐  ┌───────────────────────────┐    │
│  │ VS Code        │  │ Browser                    │    │
│  │ + Cline        │  │ Access BECA GUI           │    │
│  │ (Local)        │  │ Portainer, MCP            │    │
│  └────────────────┘  └───────────────────────────┘    │
└───────────┬─────────────────────┬───────────────────────┘
            │                     │
            │ MCP (optional)      │ HTTPS
            ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│  GCP VM - Docker Compose Stack                          │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────┐  ┌───────────────┐ │
│  │ BECA Agent   │  │ Ollama+GPU  │  │ MCP Server    │ │
│  │ (Gradio GUI) │  │ (T4 GPU)    │  │ (Claude API)  │ │
│  │ Port: 7860   │  │ Port: 11434 │  │ Port: 8080    │ │
│  └──────────────┘  └─────────────┘  └───────────────┘ │
│  ┌──────────────┐                                      │
│  │ Portainer    │ Docker Management from any device    │
│  │ Port: 9000   │                                      │
│  └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

### Required
- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Docker installed (for local testing only)
- Bash shell (Git Bash on Windows, Terminal on Mac/Linux)

### Optional
- Claude Desktop or Cline extension (for MCP integration)
- Domain name (for SSL/HTTPS)

## 🚀 Quick Start (3 Steps)

### 1. Configure Environment

```bash
# Copy example environment file
cp docker/.env.example docker/.env

# Edit configuration
nano docker/.env  # or use your preferred editor

# Required settings:
# - GCP_PROJECT_ID: Your GCP project ID
# - MCP_AUTH_TOKEN: Generate with: openssl rand -hex 32
```

### 2. Deploy to GCP

```bash
# Make scripts executable
chmod +x docker/*.sh

# Deploy BECA to Google Cloud
./docker/deploy-gcp.sh
```

This will:
- ✅ Create GCP VM with T4 GPU (SPOT instance for cost savings)
- ✅ Install Docker and NVIDIA Container Toolkit
- ✅ Set up firewall rules
- ✅ Deploy BECA stack automatically
- ✅ Configure all services

### 3. Access BECA

The deployment script will output access URLs:

```
Access URLs:
  BECA GUI:  http://YOUR_IP:7860
  Portainer: http://YOUR_IP:9000
  MCP Server: http://YOUR_IP:8080
```

**Note:** Wait 2-3 minutes after deployment for Docker containers to fully start and models to download.

## 📊 Daily Usage

### Start BECA (Morning)

```bash
./docker/start-beca.sh
```

Wait 30-60 seconds, then access BECA GUI in your browser.

### Check Status

```bash
./docker/status-beca.sh
```

Shows VM status, container health, and access URLs.

### Stop BECA (Evening)

```bash
./docker/stop-beca.sh
```

**💰 Saves ~$3-4/day** in compute costs!

## 🖥️ Managing from iPad

### Option 1: Web Browser (Safari/Chrome)

1. **Access BECA GUI**: Open `http://your-vm-ip:7860`
   - Chat with BECA
   - Monitor learning progress
   - View file changes

2. **Access Portainer**: Open `http://your-vm-ip:9000`
   - Manage Docker containers
   - View logs
   - Restart services
   - Monitor resource usage

### Option 2: Google Cloud Console App (iOS)

1. Install **Google Cloud Console** from App Store
2. Navigate to Compute Engine
3. Start/stop VM instances
4. View costs and billing
5. SSH into VM via Cloud Shell (in app)

### Option 3: Remote Desktop Apps

- **Termius** (SSH client for iPad)
- **Prompt** (SSH client with good iPad support)
- **Blink Shell** (advanced terminal for iPad)

## 🔧 Container Services

### BECA Agent (Python/Gradio)
- **Purpose**: Main BECA application with GUI
- **Port**: 7860
- **Features**:
  - Chat interface
  - Autonomous learning dashboard
  - Meta-learning metrics
  - File tree browser
  - Code viewer with diff

### Ollama GPU
- **Purpose**: LLM inference with GPU acceleration
- **Port**: 11434
- **Models**: llama3.1:8b, qwen2.5-coder:7b-instruct
- **GPU**: NVIDIA T4 (16GB)

### MCP Server
- **Purpose**: Expose BECA tools to Claude/Cline
- **Port**: 8080
- **Authentication**: Token-based (set in .env)
- **Features**:
  - 39+ BECA tools as MCP resources
  - File operations
  - Git commands
  - Code analysis
  - Knowledge search
  - Memory management

### Portainer
- **Purpose**: Docker management GUI
- **Port**: 9000, 9443 (HTTPS)
- **Features**:
  - Container management
  - Log viewing
  - Resource monitoring
  - Stack deployment
  - iPad-compatible interface

## 🔐 Security

### Firewall Rules

The deployment automatically creates firewall rules that:
- Restrict BECA GUI, Portainer, and MCP to your IP address
- Allow HTTP/HTTPS for nginx proxy (if enabled)
- Use network tags for easy management

### Update Allowed IP

If your IP changes:

```bash
# Get your current IP
curl ifconfig.me

# Update .env file
nano docker/.env
# Set: ALLOWED_IP=your-new-ip/32

# Re-run firewall setup
./docker/deploy-gcp.sh  # Only creates/updates firewall rules
```

### MCP Authentication

MCP server uses token-based authentication:

```bash
# Generate secure token
openssl rand -hex 32

# Add to docker/.env
MCP_AUTH_TOKEN=your-generated-token
```

Include this token in Claude Desktop MCP configuration.

## 🔌 Claude/Cline Integration

See [MCP-INTEGRATION.md](./MCP-INTEGRATION.md) for detailed instructions on:
- Configuring Claude Desktop to use BECA's MCP server
- Setting up Cline extension with MCP
- Available tools and resources
- Example workflows

## 💰 Cost Management

### Current Configuration

**SPOT Instance (Recommended)**:
- Compute: ~$0.10/hr
- GPU: ~$0.07/hr
- **Total: ~$0.17/hr** when running
- **Disk: ~$0.07/day** when stopped

**Monthly Costs**:
- 24/7 runtime: ~$125/mo
- 8 hours/day: ~$40/mo
- Stopped: ~$2/mo (disk only)

### Savings Tips

1. **Always stop when not in use**:
   ```bash
   ./docker/stop-beca.sh
   ```

2. **Use SPOT instances** (already default):
   - 70% cost savings
   - May be preempted (rarely)
   - Auto-restarts if needed

3. **Set budget alerts** in Google Cloud Console:
   - Project → Billing → Budgets & Alerts
   - Set alert at $50, $100, etc.

4. **Schedule automatic shutdown**:
   ```bash
   # Add to VM metadata (runs at midnight)
   gcloud compute instances add-metadata beca-ollama \
     --zone=us-central1-b \
     --metadata=shutdown-schedule="0 0 * * *"
   ```

## 🛠️ Troubleshooting

### Containers Not Starting

```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Check container status
sudo docker ps -a

# View logs
sudo docker-compose -f /opt/beca/docker/docker-compose.yml logs

# Restart containers
sudo docker-compose -f /opt/beca/docker/docker-compose.yml restart
```

### GPU Not Working

```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Check GPU
nvidia-smi

# Check NVIDIA Docker runtime
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Restart Docker
sudo systemctl restart docker
```

### Can't Access BECA GUI

1. **Check VM is running**:
   ```bash
   ./docker/status-beca.sh
   ```

2. **Wait for containers to start** (2-3 minutes after VM start)

3. **Check firewall rules**:
   ```bash
   gcloud compute firewall-rules list --filter="name~beca"
   ```

4. **Verify your IP is allowed**:
   ```bash
   curl ifconfig.me  # Get your current IP
   # Update firewall if needed
   ```

### Models Not Downloading

```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Manually pull models
sudo docker exec ollama-gpu ollama pull llama3.1:8b
sudo docker exec ollama-gpu ollama pull qwen2.5-coder:7b-instruct

# List models
sudo docker exec ollama-gpu ollama list
```

## 📁 File Structure

```
docker/
├── Dockerfile.beca          # BECA agent container
├── Dockerfile.mcp           # MCP server container
├── docker-compose.yml       # Complete stack definition
├── mcp-server.js           # MCP server implementation
├── nginx.conf              # Reverse proxy config (optional)
├── .env.example            # Configuration template
├── .env                    # Your configuration (create from example)
├── deploy-gcp.sh           # Full deployment automation
├── start-beca.sh           # Quick start
├── stop-beca.sh            # Quick stop
├── status-beca.sh          # Status checker
├── README.md               # This file
└── MCP-INTEGRATION.md      # Claude/Cline setup guide
```

## 🔄 Updates and Maintenance

### Update BECA Code

```bash
# Option 1: Upload from local
gcloud compute scp --recurse . beca-ollama:/opt/beca --zone=us-central1-b

# Option 2: Pull from git (if repo is public)
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca && git pull"

# Rebuild and restart
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca && sudo docker-compose -f docker/docker-compose.yml up -d --build"
```

### Backup Databases

```bash
# Download databases to local machine
gcloud compute scp beca-ollama:/opt/beca/beca_memory.db ./backups/ --zone=us-central1-b
gcloud compute scp beca-ollama:/opt/beca/beca_knowledge.db ./backups/ --zone=us-central1-b
```

### View Container Logs

```bash
# All containers
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker-compose -f /opt/beca/docker/docker-compose.yml logs"

# Specific container
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-agent -f"
```

## 📚 Additional Resources

- [MCP Integration Guide](./MCP-INTEGRATION.md) - Connect Claude/Cline
- [Google Cloud Documentation](https://cloud.google.com/compute/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Portainer Documentation](https://docs.portainer.io/)

## 🆘 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Review container logs
3. Check Google Cloud Console for VM/billing issues
4. Verify firewall rules and network connectivity

## 📝 License

Same as BECA project - MIT License

