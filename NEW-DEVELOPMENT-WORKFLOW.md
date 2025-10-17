# BECA New Development Workflow Guide

## 🎯 Overview

Your BECA system now uses a **Git-based deployment workflow** instead of copying files with SCP. This is faster, cleaner, and works perfectly with BECA's self-improvement capabilities.

---

## 🏗️ Architecture

### What Runs Where:
```
┌─────────────────────────────────────────────────┐
│  Your Local Machine (c:\dev)                    │
│  - Edit code                                    │
│  - Commit changes                               │
│  - Push to GitHub                               │
└─────────────────┬───────────────────────────────┘
                  │
                  │ git push/pull
                  ▼
┌─────────────────────────────────────────────────┐
│  GitHub (https://github.com/BobbyW08/BECA.git)  │
│  - Version control                              │
│  - Backup                                       │
│  - BECA can push her improvements               │
└─────────────────┬───────────────────────────────┘
                  │
                  │ git pull
                  ▼
┌─────────────────────────────────────────────────┐
│  Google Cloud VM (beca-ollama)                  │
│  /opt/beca/ ← Git repository                    │
│  - Docker containers                            │
│  - React frontend (port 3000)                   │
│  - FastAPI backend (port 8000)                  │
│  - BECA can modify & commit code                │
└─────────────────────────────────────────────────┘
```

---

## 📁 Key Files & Their Roles

### Deployment Scripts:
- **`deploy-beca-git.bat`** ✅ NEW! Use this for deployments
  - Fast Git-based deployment
  - Only transfers changed files
  - Rebuilds containers automatically
  
- ~~`deploy-new-beca-ui.bat`~~ ❌ OLD! Don't use anymore
  - Used SCP to copy ALL files (slow)
  - Deprecated

### Container Configuration:
- **`docker/docker-compose.yml`** - Defines all services:
  - `beca-frontend` - React UI (port 3000)
  - `beca-backend` - FastAPI (port 8000)
  - `ollama-gpu` - AI models with GPU
  - `mcp-server` - Claude integration
  - `portainer` - Docker management

### Frontend Files:
- **`frontend/Dockerfile`** - Builds React app
- **`frontend/package.json`** - Node dependencies
- **`frontend/src/`** - React components

### Backend Files:
- **`api/Dockerfile`** - Builds FastAPI app
- **`api/main.py`** - FastAPI server
- **`api/requirements.txt`** - Python dependencies

### VM Management:
- **`start-beca.bat`** - Start VM & open React UI
- **`stop-beca.bat`** - Stop VM
- **`diagnose-beca.bat`** - Troubleshoot issues
- **`setup-new-beca-firewall.bat`** - Firewall rules (one-time)

---

## 🚀 Daily Development Workflow

### Making Changes Locally:

```bash
# 1. Edit your code (e.g., modify React components)

# 2. Test locally if needed (optional)
cd frontend
npm start  # Opens localhost:3000

# 3. Commit your changes
git add -A
git commit -m "Your change description"
git push origin main

# 4. Deploy to VM (fast!)
.\deploy-beca-git.bat
```

**That's it!** The script will:
- ✅ Push to GitHub
- ✅ Pull on VM
- ✅ Rebuild only changed containers
- ✅ Start everything
- ✅ Open browser to your React UI

### Time Comparison:

**OLD Method** (SCP):
- Copy ALL files: 10-15 minutes
- 400MB+ transferred every time
- Slow and wasteful

**NEW Method** (Git):
- Transfer only changes: 30 seconds
- Small commits: ~1MB
- Fast and efficient!

---

## 🤖 BECA Self-Improvement Workflow

When BECA improves herself:

```
BECA running on VM
    ↓
Modifies her own code (/opt/beca/src/...)
    ↓
Commits to Git (from VM)
    ↓
Pushes to GitHub
    ↓
You review on GitHub (any device!)
    ↓
Pull to local machine (optional)
```

### How BECA Commits:
```bash
# BECA can run these commands on the VM:
cd /opt/beca
sudo git add .
sudo git commit -m "BECA: Improved feature X"
sudo git push origin main
```

You'll see her commits on GitHub with timestamps!

---

## 📱 Accessing BECA

### From Any Device:

1. **Get current VM IP:**
   ```bash
   .\diagnose-beca.bat
   ```
   Shows: `Current IP: 136.114.128.9`

2. **Access URLs:**
   - **React UI**: `http://[IP]:3000` ← Use this!
   - **Backend API**: `http://[IP]:8000/docs`
   - **Portainer**: `http://[IP]:9000`

3. **From iPad/Phone:**
   - Open browser
   - Navigate to `http://[IP]:3000`
   - Full functionality!

---

## 🔧 Common Operations

### Starting BECA:
```bash
.\start-beca.bat
```
- Starts VM
- Waits for containers
- Opens React UI automatically

### Stopping BECA (Save Money!):
```bash
.\stop-beca.bat
```
- Stops VM
- Costs drop to ~$0.07/day

### Deploying Changes:
```bash
.\deploy-beca-git.bat
```
- Fast Git-based deployment
- Only rebuilds what changed

### Troubleshooting:
```bash
.\diagnose-beca.bat
```
- Checks VM status
- Shows current IP
- Tests connection
- Lists running containers

---

## 🐛 Troubleshooting

### "Containers not starting"
```bash
# SSH to VM and check logs:
gcloud compute ssh beca-ollama --zone=us-central1-b

# View container logs:
sudo docker-compose -f docker/docker-compose.yml logs beca-frontend
sudo docker-compose -f docker/docker-compose.yml logs beca-backend

# Restart all containers:
cd /opt/beca
sudo docker-compose -f docker/docker-compose.yml restart
```

### "Can't access React UI"
1. Check VM is running: `.\diagnose-beca.bat`
2. Check IP hasn't changed
3. Verify firewall rules exist (ports 3000, 8000)
4. Wait 90 seconds after starting VM

### "Need to update VM code"
```bash
# SSH to VM and pull latest:
gcloud compute ssh beca-ollama --zone=us-central1-b
cd /opt/beca
sudo git pull origin main
sudo docker-compose -f docker/docker-compose.yml up -d --build
```

---

## 📊 Cost Management

### Running Costs:
- **VM Running**: ~$0.17/hour (~$4/day if left on 24/7)
- **VM Stopped**: ~$0.07/day (storage only)

### Best Practice:
**Stop VM when not in use!**
```bash
.\stop-beca.bat  # Run this at end of day
```

### Monthly Costs:
- Smart usage (8 hrs/day): **~$10-20/month** ✅
- Left on 24/7: **~$125/month** ⚠️

---

## 🎓 Key Concepts

### Why Git-Based Deployment?
1. **Efficient**: Only changed files transfer
2. **Version Controlled**: Every change tracked
3. **Collaborative**: BECA can commit improvements
4. **Device Agnostic**: Works from anywhere
5. **Fast**: 30 seconds vs 15 minutes

### Why Everything on VM?
1. **GPU Access**: AI models need NVIDIA T4
2. **Always Available**: Access from any device
3. **Self-Improvement**: BECA can modify her code
4. **Consistent**: Same environment everywhere

### Docker Advantages:
1. **Isolated**: Each service in own container
2. **Reproducible**: Same setup every time
3. **Easy Updates**: Just rebuild containers
4. **Persistent**: Data survives container restarts

---

## 📝 Quick Reference Card

```bash
# Daily Commands:
.\start-beca.bat              # Start VM & open UI
.\stop-beca.bat               # Stop VM (save money!)
.\deploy-beca-git.bat         # Deploy after making changes

# Development:
git add -A                    # Stage changes
git commit -m "Message"       # Commit changes
git push origin main          # Push to GitHub
.\deploy-beca-git.bat         # Deploy to VM

# Troubleshooting:
.\diagnose-beca.bat           # Check status & IP
gcloud compute ssh beca-ollama --zone=us-central1-b  # SSH to VM

# Access URLs:
http://[VM-IP]:3000           # React UI (main)
http://[VM-IP]:8000/docs      # Backend API
http://[VM-IP]:9000           # Portainer
```

---

## ✅ Summary

You now have:
- ✅ Modern React frontend (replacing old Gradio)
- ✅ Git-based deployment (fast & efficient)
- ✅ Self-improvement capabilities (BECA can commit)
- ✅ Multi-device access (iPad, laptop, etc.)
- ✅ Professional development workflow
- ✅ All changes backed up to GitHub

**Next Steps:**
1. Run `.\deploy-beca-git.bat` to deploy the React frontend
2. Access your new UI at `http://[VM-IP]:3000`
3. Start developing!

---

**Last Updated**: October 16, 2025
**Repository**: https://github.com/BobbyW08/BECA.git
