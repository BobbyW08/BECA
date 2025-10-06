# BECA Startup Instructions

Complete guide to start BECA from your Windows laptop with cloud GPU.

## Prerequisites (One-Time Setup)

Before starting BECA, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Virtual environment created at `C:\dev\.venv`
- ✅ Dependencies installed (see below)
- ✅ Cloud GPU VM created and running

---

## Quick Start (Every Time)

### 1. Start the Cloud GPU VM (if stopped)

```powershell
# Check if VM is running
gcloud compute instances list --project=beca-0001

# If status is TERMINATED, start it
gcloud compute instances start beca-ollama --zone=us-central1-c --project=beca-0001

# Wait 30 seconds for VM to fully start
Start-Sleep -Seconds 30
```

### 2. Verify Ollama is Running

```powershell
# Test connection to Ollama
curl http://34.28.62.86:11434/api/tags
```

**Expected output:** JSON with model info for `llama3.1:8b`

If you get an error:
- Wait 30 more seconds and try again
- Check VM status: `gcloud compute instances list --project=beca-0001`
- SSH in and restart Ollama: `gcloud compute ssh beca-ollama --zone=us-central1-c --command="sudo systemctl restart ollama"`

### 3. Activate Python Environment

Open PowerShell in VS Code or standalone:

```powershell
# Navigate to project
cd C:\dev

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your prompt.

### 4. Launch BECA GUI

```powershell
python beca_gui.py
```

### 5. Open in Browser

BECA will automatically open in your default browser at:
```
http://127.0.0.1:7860
```

If it doesn't open automatically, click the link in the terminal.

---

## Full Setup (First Time Only)

If this is your first time setting up BECA on your laptop:

### 1. Install Python Dependencies

```powershell
cd C:\dev

# Create virtual environment (if not exists)
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 2. Verify Cloud VM Configuration

Check that BECA is configured to use the cloud GPU:

```powershell
# Check the Ollama URL in config
Get-Content src\langchain_agent.py | Select-String "OLLAMA_URL"
```

**Should show:** `OLLAMA_URL = "http://34.28.62.86:11434"`

If it shows `127.0.0.1`, update it:
```powershell
(Get-Content src\langchain_agent.py) -replace 'http://127.0.0.1:11434', 'http://34.28.62.86:11434' | Set-Content src\langchain_agent.py
```

---

## Troubleshooting

### Error: "Connection refused" or "Cannot connect to Ollama"

**Problem:** VM is stopped or Ollama isn't running

**Solution:**
```powershell
# 1. Check VM status
gcloud compute instances list --project=beca-0001

# 2. Start VM if stopped
gcloud compute instances start beca-ollama --zone=us-central1-c --project=beca-0001

# 3. Wait and test
Start-Sleep -Seconds 30
curl http://34.28.62.86:11434/api/tags
```

### Error: "ModuleNotFoundError"

**Problem:** Dependencies not installed or wrong Python environment

**Solution:**
```powershell
# Make sure you're in the virtual environment
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: Firewall blocking connection

**Problem:** Your IP address changed (if on different network)

**Solution:**
```powershell
# Update firewall rule with your new IP
.\setup-firewall.ps1
```

### BECA is responding slowly

**Problem:** Model might not be using GPU or network latency

**Solutions:**
1. Check GPU is being used on VM:
   ```powershell
   gcloud compute ssh beca-ollama --zone=us-central1-c --command="nvidia-smi"
   ```

2. Check network latency:
   ```powershell
   ping 34.28.62.86
   ```

3. If ping is >100ms, consider switching to a closer region

---

## Stopping BECA

### Stop the GUI
Press `Ctrl+C` in the PowerShell terminal running `beca_gui.py`

### Stop the Cloud VM (to save money)
```powershell
# Stop VM when not in use
gcloud compute instances stop beca-ollama --zone=us-central1-c --project=beca-0001
```

**Important:** Always stop the VM when not using BECA to avoid charges (~$0.30/hour = $220/month if left running)

---

## Cost Management

### Check Current VM Status
```powershell
gcloud compute instances list --project=beca-0001 --format="table(name,zone,status,creationTimestamp)"
```

### View Costs
Visit: https://console.cloud.google.com/billing?project=beca-0001

### Estimated Costs
- **Running:** $0.30/hour (~$7.20/day if running 24/7)
- **Stopped:** $0.04/day (disk storage only)
- **Network:** ~$0.01/GB (usually minimal)

**Best Practice:** Stop the VM every night or when not in use!

---

## Quick Reference Commands

```powershell
# Start VM
gcloud compute instances start beca-ollama --zone=us-central1-c --project=beca-0001

# Stop VM
gcloud compute instances stop beca-ollama --zone=us-central1-c --project=beca-0001

# Check VM status
gcloud compute instances list --project=beca-0001

# Test Ollama connection
curl http://34.28.62.86:11434/api/tags

# Activate Python env
cd C:\dev && .\.venv\Scripts\Activate.ps1

# Start BECA
python beca_gui.py

# Update firewall for new IP
.\setup-firewall.ps1

# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-c --project=beca-0001
```

---

## Daily Workflow

**Morning (Starting work):**
1. `gcloud compute instances start beca-ollama --zone=us-central1-c --project=beca-0001`
2. Wait 30 seconds
3. `cd C:\dev && .\.venv\Scripts\Activate.ps1`
4. `python beca_gui.py`
5. Open browser to http://127.0.0.1:7860

**Evening (Ending work):**
1. Close browser
2. Press `Ctrl+C` in PowerShell
3. `gcloud compute instances stop beca-ollama --zone=us-central1-c --project=beca-0001`

This workflow will save you ~$5/day compared to leaving it running 24/7!
