# 🚀 How to Start BECA (Docker/Cloud Setup)

**Your BECA AI agent runs in Docker containers on Google Cloud with GPU acceleration.**

---

## Quick Start (Every Time)

### Windows Method
1. **Double-click `start-beca.bat`** in `C:\dev\`
2. Wait 60 seconds for Docker containers to start
3. Open browser to **http://34.55.204.139:7860**
4. Start using BECA! 🎉

### iPad/Mobile Method
1. Visit https://console.cloud.google.com
2. Go to **Compute Engine → VM Instances**
3. Click **START** on `beca-ollama` instance
4. Wait 60 seconds
5. Open browser to **http://34.55.204.139:7860**

**Done!** No Python setup, no pip installs, no virtual environments needed.

---

## What's Running?

Your BECA setup includes:

### BECA AI Agent (Main Interface)
- **URL**: http://34.55.204.139:7860
- **Port**: 7860
- Full Gradio GUI with 39+ AI tools
- Autonomous learning system
- Memory and knowledge systems

### Ollama (GPU-Accelerated AI)
- **URL**: http://34.55.204.139:11434
- **Port**: 11434
- NVIDIA Tesla T4 GPU
- Models: Llama 3.1 8B + Qwen2.5-Coder 7B

### MCP Server (Claude/Cline Integration)
- **URL**: http://34.55.204.139:8080
- **Port**: 8080
- Model Context Protocol for IDE integration

### Portainer (Docker Management)
- **URL**: http://34.55.204.139:9000
- **Port**: 9000
- Visual container management interface

All services auto-start when the VM boots!

---

## Management Commands

### Start VM (Windows)
```batch
# Double-click this file:
start-beca.bat

# Or run in PowerShell:
gcloud compute instances start beca-ollama --zone=us-central1-b
```

### Stop VM (Save Money!)
```batch
# Double-click this file:
stop-beca.bat

# Or run in PowerShell:
gcloud compute instances stop beca-ollama --zone=us-central1-b
```

### Check Status
```batch
# Double-click this file:
check-beca.bat

# Or run in PowerShell:
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)"
```

---

## Cost Management

### Pricing
- **Running (SPOT)**: ~$0.17/hour (~$4/day if left on 24/7)
- **Stopped**: ~$0.07/day (storage only)
- **Monthly with smart usage**: $10-20/month ✅
- **Monthly if left on 24/7**: ~$125/month ⚠️

### Best Practice
**Always stop the VM when done for the day!**

```batch
# Save ~$3/day by stopping when not in use
stop-beca.bat
```

### Daily Workflow
**Morning**: Run `start-beca.bat` → Wait 60 sec → Open browser  
**Evening**: Run `stop-beca.bat` → VM stops, cost drops to $0.07/day

---

## Features

### 🎯 Visual Interface
- **File Tree**: Project structure visualization
- **Code Viewer**: Syntax highlighting
- **Diff Viewer**: Compare changes
- **Real-time Updates**: Auto-refreshing file tree

### 🧠 AI Capabilities
- **39+ Development Tools**: File ops, Git, testing, code analysis, web search
- **Memory System**: Remembers conversations and preferences
- **Knowledge Base**: Learns from docs and code patterns
- **Autonomous Learning**: Background learning system
- **Meta-Learning**: Learns from every feature built

### 🛠️ Development Tools
- Build full applications (React, Flask, FastAPI, Python CLI)
- Debug and fix code
- Analyze codebases
- Generate and run tests
- Git integration
- Web scraping and research

---

## Access from Any Device

### Windows Laptop/Desktop
- Use batch files (`start-beca.bat`, `stop-beca.bat`)
- Access at http://34.55.204.139:7860

### iPad/Tablet
- Start VM from Google Cloud Console app
- Open Safari/Chrome to http://34.55.204.139:7860
- Full functionality (no app needed!)

### Other Computers
- Start VM from https://console.cloud.google.com
- Access BECA in any browser

---

## Troubleshooting

### ❌ Can't Access http://34.55.204.139:7860

**Solution 1**: Check if VM is running
```powershell
gcloud compute instances list --project=beca-0001
# Look for STATUS = RUNNING
```

**Solution 2**: Wait longer (containers need time to start)
```powershell
# After starting VM, wait 60-90 seconds
```

**Solution 3**: Check if IP changed
```powershell
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### ❌ Containers Not Starting

**SSH into VM and check**:
```powershell
gcloud compute ssh beca-ollama --zone=us-central1-b

# Once in VM, check containers:
sudo docker ps

# View logs:
sudo docker logs beca-agent
sudo docker logs ollama-gpu

# Restart containers if needed:
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml restart
```

### ❌ GPU Not Working

**Check GPU status**:
```powershell
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker exec ollama-gpu nvidia-smi"

# Should show Tesla T4 GPU details
```

### ❌ BECA Responding Slowly

**Possible causes**:
1. High network latency (check your internet connection)
2. GPU not being used (see above)
3. Models loading for first time (wait 30 seconds)

---

## Docker Container Details

### Container Architecture
```
beca-ollama VM (Google Cloud)
├── beca-agent (Port 7860)
│   └── Gradio GUI + BECA tools
├── ollama-gpu (Port 11434)
│   └── AI models with GPU acceleration
├── mcp-server (Port 8080)
│   └── Claude/Cline integration
└── portainer (Port 9000)
    └── Docker management GUI
```

### Data Persistence
All your data is preserved across VM restarts:
- **BECA Memory** → Docker volume `beca-memory`
- **Workspace Files** → Docker volume `beca-workspace`
- **AI Models** → Docker volume `ollama-models` (~10GB)
- **Portainer Config** → Docker volume `portainer-data`

Even when you stop the VM, all data remains intact!

---

## Advanced Management

### Restart Specific Container
```powershell
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Restart BECA agent
sudo docker restart beca-agent

# Restart Ollama
sudo docker restart ollama-gpu
```

### View Container Logs
```powershell
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# View BECA logs
sudo docker logs beca-agent --tail 100

# View Ollama logs
sudo docker logs ollama-gpu --tail 100

# Follow logs in real-time
sudo docker logs -f beca-agent
```

### Update BECA Code
```powershell
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Navigate to BECA directory
cd /opt/beca

# Pull latest changes (if using git)
sudo git pull

# Rebuild and restart containers
sudo docker-compose -f docker/docker-compose.yml up -d --build
```

### Manual Container Control
```powershell
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Stop all containers
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml down

# Start all containers
sudo docker-compose -f docker/docker-compose.yml up -d

# View all containers
sudo docker ps -a
```

---

## SPOT Instance Note

Your VM uses a **SPOT (preemptible) instance** for 70% cost savings:

✅ **Advantages**:
- Runs normally 99% of the time
- Costs ~$0.17/hr instead of ~$0.65/hr
- All data preserved on disk

⚠️ **What happens if Google preempts it**:
- VM stops with 30-second warning (rare)
- Simply restart with `start-beca.bat`
- All data intact, containers auto-start
- No work lost

This is very rare and the savings are worth it!

---

## Additional Resources

### Detailed Guides
- `docker/FINAL-WORKFLOW-GUIDE.md` - Complete Docker workflow
- `docker/README.md` - Docker setup details
- `docker/DEPLOYMENT-SUMMARY.md` - Deployment process
- `readme.md` - Full BECA documentation

### Portainer Management
Visit **http://34.55.204.139:9000** for:
- Visual container management
- Resource monitoring
- Log viewing
- Container restart/rebuild
- Volume management

---

## Quick Reference

```powershell
# Essential Commands
start-beca.bat                    # Start VM (Windows)
stop-beca.bat                     # Stop VM (Windows)
check-beca.bat                    # Check status (Windows)

# Access URLs
http://34.55.204.139:7860        # BECA GUI
http://34.55.204.139:9000        # Portainer
http://34.55.204.139:8080        # MCP Server
http://34.55.204.139:11434       # Ollama API

# Cloud Console
https://console.cloud.google.com  # Manage from any device
```

---

## Summary

### To Use BECA:
1. ✅ Run `start-beca.bat` (or start from cloud console)
2. ✅ Wait 60 seconds
3. ✅ Open http://34.55.204.139:7860
4. ✅ Use BECA!
5. ✅ Run `stop-beca.bat` when done (save money!)

### Why This Setup is Great:
- ✅ Works from ANY device (Windows, iPad, Mac, Linux)
- ✅ No local Python setup needed
- ✅ GPU-accelerated AI models
- ✅ Auto-starts containers on VM boot
- ✅ All data persists across restarts
- ✅ Cost-effective with SPOT pricing
- ✅ Professional Docker-based deployment

---

**Enjoy your cloud-powered AI development assistant! 🚀**
