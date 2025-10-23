# 🚀 How to Start BECA (Docker/Cloud Setup)

**Your BECA AI agent runs in Docker containers on Google Cloud with GPU acceleration.**

---

## Quick Start (Every Time)

### Windows Method ⭐ RECOMMENDED
1. **Double-click `start-beca.bat`** in `C:\dev\`
2. Wait 90 seconds for Docker containers to start
3. **Browser will automatically open** with the correct IP address
4. Start using BECA! 🎉

**Note**: The script automatically fetches the current external IP and opens your browser to the correct address. This is the easiest method!

### iPad/Mobile Method
1. Visit https://console.cloud.google.com
2. Go to **Compute Engine → VM Instances**
3. Click **START** on `beca-ollama` instance
4. Wait 90 seconds for containers to start
5. **Click on the VM name** `beca-ollama` to see details
6. Copy the **External IP** shown in the details
7. Open browser to **http://[EXTERNAL-IP]:3000** (replace [EXTERNAL-IP] with the copied IP)

**Note**: The external IP changes every time you start the VM (SPOT instance behavior). Always check the current IP from the VM details page.

**Done!** No Python setup, no pip installs, no virtual environments needed.

---

## What's Running?

Your BECA setup includes:

### BECA Frontend (React UI)
- **URL**: http://[EXTERNAL-IP]:3000
- **Port**: 3000
- Modern React interface with Plan/Act modes
- File tree, code viewer, diff viewer
- Real-time updates

### BECA Backend (FastAPI)
- **URL**: http://[EXTERNAL-IP]:8000
- **Port**: 8000
- RESTful API with 39+ AI tools
- Autonomous learning system
- Memory and knowledge systems

### Ollama (GPU-Accelerated AI)
- **URL**: http://[EXTERNAL-IP]:11434
- **Port**: 11434
- NVIDIA Tesla T4 GPU
- Models: Llama 3.1 8B + Qwen2.5-Coder 7B

### MCP Server (Claude/Cline Integration)
- **URL**: http://[EXTERNAL-IP]:8080
- **Port**: 8080
- Model Context Protocol for IDE integration

### Portainer (Docker Management)
- **URL**: http://[EXTERNAL-IP]:9000
- **Port**: 9000
- Visual container management interface

**All services now automatically start when the VM boots!** 🎉

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
- Browser opens automatically to correct IP address

### iPad/Tablet
- Start VM from Google Cloud Console app
- Get current external IP from VM details page
- Open Safari/Chrome to http://[EXTERNAL-IP]:3000
- Full functionality (no app needed!)

### Other Computers
- Start VM from https://console.cloud.google.com
- Get current external IP from VM details page
- Access BECA in any browser at http://[EXTERNAL-IP]:3000

---

## Troubleshooting

### ❌ Can't Access BECA

**IMPORTANT**: The external IP address changes every time you start the VM (SPOT instance behavior).

**Solution**: Always use `start-beca.bat` on Windows - it automatically finds and opens the correct IP!

**For iPad/Mobile users**: 
1. Go to Google Cloud Console → Compute Engine → VM Instances
2. Click on `beca-ollama` VM name to see details
3. Copy the current **External IP** address
4. Open browser to `http://[EXTERNAL-IP]:3000`

**Manual IP lookup**:
```powershell
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

**Still not working?**
- Wait 90 seconds for containers to start after VM boots
- Check VM status: `gcloud compute instances list --project=beca-0001`

### ❌ Containers Not Starting

**SSH into VM and check**:
```powershell
gcloud compute ssh beca-ollama --zone=us-central1-b

# Once in VM, check containers:
sudo docker ps

# View logs:
sudo docker logs beca-frontend
sudo docker logs beca-backend
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
├── beca-frontend (Port 3000)
│   └── React UI + Modern interface
├── beca-backend (Port 8000)
│   └── FastAPI + 39+ AI tools
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

# Restart BECA frontend
sudo docker restart beca-frontend

# Restart BECA backend
sudo docker restart beca-backend

# Restart Ollama
sudo docker restart ollama-gpu
```

### View Container Logs
```powershell
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# View BECA frontend logs
sudo docker logs beca-frontend --tail 100

# View BECA backend logs
sudo docker logs beca-backend --tail 100

# View Ollama logs
sudo docker logs ollama-gpu --tail 100

# Follow logs in real-time
sudo docker logs -f beca-backend
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
Visit **http://[EXTERNAL-IP]:9000** for:
- Visual container management
- Resource monitoring
- Log viewing
- Container restart/rebuild
- Volume management

**Note**: The external IP changes each time the VM starts. Use `start-beca.bat` on Windows (automatically opens correct IP) or get the current IP from the VM details page in Google Cloud Console.

---

## Quick Reference

```powershell
# Essential Commands
start-beca.bat                    # Start VM (Windows)
stop-beca.bat                     # Stop VM (Windows)
check-beca.bat                    # Check status (Windows)

# Access URLs (replace [EXTERNAL-IP] with current VM IP)
http://[EXTERNAL-IP]:3000        # BECA Frontend
http://[EXTERNAL-IP]:8000        # BECA Backend API
http://[EXTERNAL-IP]:9000        # Portainer
http://[EXTERNAL-IP]:8080        # MCP Server
http://[EXTERNAL-IP]:11434       # Ollama API

# Get current external IP:
# Windows: Run start-beca.bat (automatically uses correct IP)
# Manual:  gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# Cloud Console
https://console.cloud.google.com  # Manage from any device
```

---

## Summary

### To Use BECA:
1. ✅ Run `start-beca.bat` (Windows - automatically opens browser with correct IP)
2. ✅ Wait 90 seconds for containers to start
3. ✅ Browser opens automatically to BECA (or get IP from VM details and visit http://[EXTERNAL-IP]:3000)
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
