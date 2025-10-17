# 🎉 BECA Docker Deployment - Complete! 

## ✅ Deployment Status

Your BECA AI agent is now successfully deployed on Google Cloud with Docker!

**VM Name:** `beca-ollama`  
**External IP:** `34.55.204.139`  
**Zone:** `us-central1-b`  
**GPU:** NVIDIA Tesla T4  
**Cost:** ~$0.17/hour when running (~$4/day) or ~$0.003/hour when stopped (~$0.07/day)

---

## 🌐 Access Your Services

### BECA Frontend (React UI)
- **URL:** http://34.55.204.139:3000
- **Purpose:** Modern web interface for BECA
- **Features:** Plan/Act modes, file tree, code viewer, diff viewer

### BECA Backend (FastAPI)
- **URL:** http://34.55.204.139:8000
- **Purpose:** RESTful API with AI agent logic
- **Features:** 39+ tools, autonomous learning, code generation

### Portainer (Docker Management)
- **URL:** http://34.55.204.139:9000
- **Purpose:** Visual Docker container management
- **Login:** Create admin account on first visit

### MCP Server (Claude Integration)
- **URL:** http://34.55.204.139:8080
- **Purpose:** Model Context Protocol server for Claude Desktop/Cline
- **Health:** http://34.55.204.139:8080/health

### Ollama API (LLM Inference)
- **URL:** http://34.55.204.139:11434
- **Purpose:** GPU-accelerated AI model inference
- **Models:** llama3.1:8b, qwen2.5-coder:7b

---

## 🚀 Easy Management with Windows Shortcuts

Three batch files have been created in `c:\dev` for easy management:

### 1. `start-beca.bat` - Start Your VM
```batch
@echo off
echo Starting BECA VM...
gcloud compute instances start beca-ollama --zone=us-central1-b
echo.
echo Waiting 60 seconds for Docker containers to start...
timeout /t 60 /nobreak
echo.
echo BECA is ready!
echo Frontend: http://34.55.204.139:3000
echo Backend:  http://34.55.204.139:8000/docs
pause
```

**What it does:**
- Starts the stopped VM
- Waits for Docker containers to start automatically
- Shows you the access URL

### 2. `stop-beca.bat` - Stop Your VM (Save Money!)
```batch
@echo off
echo Stopping BECA VM to save costs...
gcloud compute instances stop beca-ollama --zone=us-central1-b
echo.
echo VM stopped successfully!
echo Cost while stopped: ~$0.07/day (storage only)
pause
```

**What it does:**
- Gracefully stops the VM
- Reduces costs to ~$0.07/day (storage only)
- All data is preserved

### 3. `check-beca.bat` - Check Status
```batch
@echo off
echo Checking BECA VM status...
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status, networkInterfaces[0].accessConfigs[0].natIP)"
pause
```

**What it does:**
- Shows if VM is RUNNING or TERMINATED
- Displays the external IP address

---

## 📱 iPad/Tablet Management

You can manage BECA from ANY device using these methods:

### Option 1: Google Cloud Console App
1. Install "Google Cloud Console" app on iPad
2. Navigate to Compute Engine → VM Instances
3. Start/Stop the `beca-ollama` instance with one tap

### Option 2: Browser-Based Management
1. Visit https://console.cloud.google.com
2. Compute Engine → VM Instances → beca-ollama
3. Click START or STOP button

### Option 3: Portainer Web GUI
Once VM is running:
1. Visit http://34.55.204.139:9000 on iPad
2. View/restart containers
3. Monitor resource usage

---

## 🔄 Daily Workflow

### Starting Work on BECA
1. **Double-click `start-beca.bat`** (or start VM from Google Cloud Console on iPad)
2. Wait 60 seconds for containers to start
3. Open browser to http://34.55.204.139:3000
4. Start using BECA!

### Finishing Work
1. **Double-click `stop-beca.bat`** (or stop VM from Google Cloud Console)
2. VM stops and costs drop to ~$0.07/day
3. All data is preserved

### Cost Example
- **Active development (8 hours/day):** $1.36/day = $40/month
- **Stopped when not in use (16 hours/day):** $0.07/day = $2/month
- **Total with smart usage:** ~$42/month

---

## 🐳 Docker Container Architecture

All services run as Docker containers:

```
┌─────────────────────────────────────────────┐
│           beca-ollama VM (GCP)              │
│         External IP: 34.55.204.139          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ beca-frontend (Port 3000)            │  │
│  │ - React UI                           │  │
│  │ - Plan/Act Modes                     │  │
│  │ - File Tree & Code Viewer            │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ beca-backend (Port 8000)             │  │
│  │ - FastAPI                            │  │
│  │ - 39+ AI Tools                       │  │
│  │ - Autonomous Learning                │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ ollama-gpu (Port 11434)              │  │
│  │ - NVIDIA T4 GPU                      │  │
│  │ - llama3.1:8b                        │  │
│  │ - qwen2.5-coder:7b                   │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ mcp-server (Port 8080)               │  │
│  │ - Claude Desktop Integration         │  │
│  │ - Cline Integration                  │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ portainer (Port 9000)                │  │
│  │ - Docker Management GUI              │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔧 Advanced Management

### Manual Docker Commands (SSH into VM)
```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# View all containers
sudo docker ps

# View logs
sudo docker logs beca-frontend
sudo docker logs beca-backend
sudo docker logs ollama-gpu

# Restart a specific container
sudo docker restart beca-frontend
sudo docker restart beca-backend

# Stop all containers
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml down

# Start all containers
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml up -d

# Check GPU usage
sudo docker exec ollama-gpu nvidia-smi
```

### Update BECA Code
```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Navigate to BECA directory
cd /opt/beca

# Pull latest changes (if you have a git repo)
sudo git pull

# Rebuild containers
sudo docker-compose -f docker/docker-compose.yml up -d --build
```

---

## 🛠️ Troubleshooting

### BECA Frontend Not Loading
1. Check VM is running: Run `check-beca.bat`
2. Check containers: SSH in and run `sudo docker ps`
3. Check logs: `sudo docker logs beca-frontend` or `sudo docker logs beca-backend`
4. Restart container: `sudo docker restart beca-frontend` or `sudo docker restart beca-backend`

### GPU Not Working
```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Check GPU is visible
sudo docker exec ollama-gpu nvidia-smi

# Should show Tesla T4 GPU details
```

### Containers Won't Start
```bash
# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# View logs
sudo docker logs <container-name>

# Force recreate
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml up -d --force-recreate
```

### Can't Access Services
1. Check firewall rules allow ports 3000, 8000, 8080, 9000, 11434
2. Verify external IP hasn't changed: Run `check-beca.bat`
3. Check if containers are healthy: `sudo docker ps`

---

## 💾 Data Persistence

All your data is preserved across VM restarts:

- **BECA Memory:** Stored in Docker volume `beca-memory`
- **Workspace Files:** Stored in Docker volume `beca-workspace`
- **AI Models:** Stored in Docker volume `ollama-models` (~10GB)
- **Portainer Config:** Stored in Docker volume `portainer-data`

Even when you stop the VM, all this data remains intact.

---

## 🎯 Next Steps

1. **Try BECA:** Visit http://34.55.204.139:3000
2. **Check API:** Visit http://34.55.204.139:8000/docs
3. **Set Up Portainer:** Visit http://34.55.204.139:9000 and create admin account
4. **Test MCP Integration:** Configure Claude Desktop/Cline to connect to http://34.55.204.139:8080
5. **Cost Optimization:** Remember to run `stop-beca.bat` when you're done for the day!

---

## 📊 SPOT Instance Note

Your VM uses a SPOT (preemptible) instance for 70% cost savings. This means:
- ✅ Runs normally 99% of the time
- ⚠️ Google may stop it with 30-second warning (rare)
- ✅ Auto-restarts with all data preserved
- ✅ Containers start automatically on restart

If Google preempts your VM, simply run `start-beca.bat` again.

---

## 🎉 Success!

You now have a fully containerized, GPU-powered AI development environment that:
- ✅ Works from any device (laptop, desktop, iPad)
- ✅ Costs only ~$0.07/day when stopped
- ✅ Automatically starts containers on VM boot
- ✅ Preserves all data across restarts
- ✅ Provides web-based management (Portainer)
- ✅ Integrates with Claude Desktop and Cline
- ✅ Runs GPU-accelerated AI models

**Enjoy your cloud-based AI development setup! 🚀**
