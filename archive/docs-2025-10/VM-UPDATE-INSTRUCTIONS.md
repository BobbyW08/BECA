# BECA VM Update Instructions - October 23, 2025

## Overview

This document provides step-by-step instructions for updating the BECA VM with the latest codebase changes.

**What was updated:**
- ✅ Documentation updated to reflect Docker/React architecture
- ✅ Comprehensive codebase review completed
- ✅ All configurations verified as uniform and functional

**What needs to be updated on VM:**
- Pull latest code from GitHub
- Rebuild Docker containers (no code changes, just documentation)
- Verify all services are running

---

## Quick Update (Recommended)

### Option 1: Using Windows Scripts (Easiest)

```batch
# 1. Stop the VM
stop-beca.bat

# 2. Wait 30 seconds for graceful shutdown

# 3. Start the VM (will automatically pull latest changes if configured)
start-beca.bat
```

**Note**: If the VM is configured with auto-pull on startup, this is all you need.

---

## Manual Update (If Auto-Pull Not Configured)

### Step 1: SSH to the VM

```bash
# Windows Command Prompt or PowerShell
gcloud compute ssh beca-ollama --zone=us-central1-b --project=beca-0001
```

### Step 2: Navigate to BECA Directory

```bash
cd /opt/beca
```

### Step 3: Pull Latest Changes

```bash
# Stash any local changes (if any)
sudo git stash

# Pull from main branch
sudo git pull origin main

# Check status
sudo git status
```

**Expected Output:**
```
Already on 'main'
Your branch is up to date with 'origin/main'.
```

### Step 4: Rebuild Docker Containers (Optional)

**Note**: Since only documentation was updated, rebuilding is not strictly necessary. However, if you want to ensure everything is fresh:

```bash
# Stop containers
sudo docker-compose -f docker/docker-compose.yml down

# Rebuild and start (this will take a few minutes)
sudo docker-compose -f docker/docker-compose.yml up -d --build

# Wait 60 seconds for containers to start
sleep 60
```

### Step 5: Verify All Services Running

```bash
# Check container status
sudo docker ps

# Expected output should show all containers running:
# - beca-frontend
# - beca-backend
# - ollama-gpu
# - mcp-server
# - portainer

# Check logs if needed
sudo docker-compose -f docker/docker-compose.yml logs --tail=50
```

### Step 6: Verify Services are Accessible

```bash
# Get VM external IP
curl -s ifconfig.me

# Test backend health
curl http://localhost:8000/health

# Expected: {"status":"healthy","agent_available":true,...}
```

### Step 7: Exit SSH

```bash
exit
```

---

## Verification from Windows

### Check from Your Local Machine

```batch
# 1. Get the VM IP
get-beca-ip.bat

# 2. Open browser and test:
# - Frontend: http://[VM-IP]:3000
# - Backend API Docs: http://[VM-IP]:8000/docs
# - Portainer: http://[VM-IP]:9000
```

### Expected Results

**Frontend (Port 3000):**
- ✅ React app loads
- ✅ Chat interface visible
- ✅ File tree panel on left
- ✅ Code viewer panel on right
- ✅ Plan/Act toggle working

**Backend (Port 8000):**
- ✅ API docs load (Swagger UI)
- ✅ All endpoints listed
- ✅ Health check returns success

---

## Troubleshooting

### Issue: Git Pull Fails (Permission Denied)

```bash
# Switch to root or use sudo
sudo git pull origin main
```

### Issue: Containers Won't Start

```bash
# Check Docker status
sudo systemctl status docker

# Restart Docker service
sudo systemctl restart docker

# Try starting containers again
sudo docker-compose -f docker/docker-compose.yml up -d
```

### Issue: Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Stop and remove all containers
sudo docker-compose -f docker/docker-compose.yml down

# Start fresh
sudo docker-compose -f docker/docker-compose.yml up -d
```

### Issue: Models Not Found

```bash
# Pull models manually
sudo docker exec ollama-gpu ollama pull llama3.1:8b
sudo docker exec ollama-gpu ollama pull qwen2.5-coder:7b-instruct

# List models to verify
sudo docker exec ollama-gpu ollama list
```

### Issue: Frontend Shows Connection Error

**Possible causes:**
1. Backend not running → Check `sudo docker ps`
2. Wrong API URL → Check browser console and Settings panel
3. Firewall blocking → Check firewall rules with `gcloud compute firewall-rules list`

**Solutions:**
```bash
# Restart backend container
sudo docker restart beca-backend

# Check backend logs
sudo docker logs beca-backend --tail=100

# Verify backend is accessible
curl http://localhost:8000/health
```

---

## What Changed in This Update

### Documentation Updates
- ✅ `readme.md` - Updated to reflect current Docker/React architecture
- ✅ `CODEBASE-REVIEW-2025-10-23.md` - Comprehensive review document added

### No Code Changes
- ✅ All Python code unchanged
- ✅ All Docker configurations unchanged
- ✅ All frontend code unchanged
- ✅ All deployment scripts unchanged

**This means**: The VM doesn't strictly need updating unless you want the latest documentation on the VM itself.

---

## Summary of Review Findings

### ✅ What's Working Well

1. **Model Configuration**
   - llama3.1:8b (primary) for general tasks
   - qwen2.5-coder:7b-instruct for coding tasks
   - Intelligent routing based on task type

2. **Dynamic IP Setup**
   - Frontend auto-detects hostname
   - Backend configurable via environment variables
   - Startup scripts fetch current IP automatically

3. **Frontend**
   - All buttons functional
   - Modern React UI with Plan/Act modes
   - File tree, code viewer, diff viewer working

4. **Docker Configuration**
   - All services properly configured
   - Health checks in place
   - Persistent volumes for data

5. **Code Uniformity**
   - Consistent patterns throughout
   - Proper error handling
   - Clean architecture

### ⚠️ Minor Notes

- Documentation was outdated (now fixed)
- One deprecated deployment script still in docker/ folder (harmless)
- No functional issues found

---

## Post-Update Checklist

After updating, verify:

- [ ] VM starts successfully
- [ ] All 5 Docker containers running
- [ ] Frontend loads at http://[VM-IP]:3000
- [ ] Backend API docs load at http://[VM-IP]:8000/docs
- [ ] Can send a test message in chat interface
- [ ] File tree displays project files
- [ ] Code viewer can open files
- [ ] Plan/Act toggle switches modes

---

## Cost Reminder

**Don't forget to stop the VM when done:**

```batch
# Windows
stop-beca.bat

# Or via gcloud
gcloud compute instances stop beca-ollama --zone=us-central1-b
```

**Current costs:**
- Running: ~$0.17/hour (SPOT instance)
- Stopped: ~$0.07/day (disk storage only)

---

## Questions or Issues?

If you encounter any issues during the update:

1. Check the logs: `sudo docker-compose -f docker/docker-compose.yml logs`
2. Review `CODEBASE-REVIEW-2025-10-23.md` for detailed findings
3. Consult `readme.md` for troubleshooting section

---

**Update Date**: October 23, 2025  
**Reviewed By**: Cline AI Assistant  
**Status**: ✅ Ready for deployment
