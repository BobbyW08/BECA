# BECA Startup Instructions

## TL;DR - Simple Steps

```bash
# 1. Start the VM
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# 2. Wait 30 seconds, then activate Python environment
cd C:\dev
.\.venv\Scripts\Activate.ps1

# 3. Launch BECA
python beca_gui.py

# 4. Open browser to http://127.0.0.1:7860
```

**Done!** BECA will open in your browser automatically.

---

## Prerequisites (One-Time Setup)

Before starting BECA, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Virtual environment created at `C:\dev\.venv`
- ✅ Dependencies installed (see below)
- ✅ Cloud GPU VM created and running (SPOT VM for cost savings!)

---

## Detailed Steps (Every Time)

### 1. Start the Cloud GPU VM (if stopped)

```bash
# Check if VM is running
gcloud compute instances list --project=beca-0001

# If status is TERMINATED, start it (SPOT VM auto-finds available zone!)
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# Wait 30 seconds for VM to fully start (on Windows: timeout /t 30, on Unix: sleep 30)
```

**Note:** Your VM is running as a SPOT instance in zone `us-central1-b`. If Google preempts it, just restart - your data persists on disk!

### 2. Verify Ollama is Running

```bash
# Test connection to Ollama
curl http://34.46.140.140:11434/api/tags
```

**Expected output:** JSON with model info for `llama3.1:8b`

If you get an error:
- Wait 30 more seconds and try again
- Check VM status: `gcloud compute instances list --project=beca-0001`
- SSH in and restart Ollama: `gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo systemctl restart ollama"`

### 3. Activate Python Environment

Open PowerShell in VS Code or standalone:

```bash
# Navigate to project
cd C:\dev

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your prompt.

### 4. Launch BECA GUI

```bash
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

```bash
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

```bash
# Check the Ollama URL in config
grep "OLLAMA_URL" src/langchain_agent.py
```

**Should show:** `OLLAMA_URL = "http://34.46.140.140:11434"  # SPOT VM in us-central1-b`

---

## Troubleshooting

### Error: "Connection refused" or "Cannot connect to Ollama"

**Problem:** VM is stopped or Ollama isn't running

**Solution:**
```bash
# 1. Check VM status
gcloud compute instances list --project=beca-0001

# 2. Start VM if stopped
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# 3. Wait and test (30 seconds)
curl http://34.46.140.140:11434/api/tags
```

### Error: "ModuleNotFoundError"

**Problem:** Dependencies not installed or wrong Python environment

**Solution:**
```bash
# Make sure you're in the virtual environment
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: Firewall blocking connection

**Problem:** Your IP address changed (if on different network)

**Solution:**
```bash
# Update firewall rule with your new IP
python setup_firewall.py
```

### BECA is responding slowly

**Problem:** Model might not be using GPU or network latency

**Solutions:**
1. Check GPU is being used on VM:
   ```bash
   gcloud compute ssh beca-ollama --zone=us-central1-b --command="nvidia-smi"
   ```

2. Check network latency:
   ```bash
   ping 34.46.140.140
   ```

3. If ping is >100ms, consider switching to a closer region

---

## Stopping BECA

### Stop the GUI
Press `Ctrl+C` in the PowerShell terminal running `beca_gui.py`

### Stop the Cloud VM (to save money)
```bash
# Stop VM when not in use
gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001
```

**Important:** Always stop the VM when not using BECA to avoid charges. With SPOT pricing: ~$0.17/hour = $125/month if left running 24/7 (vs ~$330 standard!)

---

## Cost Management

### Check Current VM Status
```bash
gcloud compute instances list --project=beca-0001 --format="table(name,zone,status,creationTimestamp)"
```

### View Costs
Visit: https://console.cloud.google.com/billing?project=beca-0001

### Estimated Costs (SPOT VM - 70% Savings!)
- **Running (SPOT):** ~$0.17/hour (~$4/day if running 24/7)
- **Stopped:** ~$0.07/day (disk storage only)
- **Network:** ~$0.01/GB (usually minimal)
- **Total with SPOT:** ~$125/month (24/7) vs ~$330 standard

**Best Practice:** Stop the VM every night or when not in use to save even more!

---

## Quick Reference Commands

```bash
# Start VM
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# Stop VM
gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001

# Check VM status
gcloud compute instances list --project=beca-0001

# Test Ollama connection
curl http://34.46.140.140:11434/api/tags

# Activate Python env
cd C:\dev && .\.venv\Scripts\Activate.ps1

# Start BECA
python beca_gui.py

# Update firewall for new IP
python setup_firewall.py

# SSH into VM
gcloud compute ssh beca-ollama --zone=us-central1-b --project=beca-0001
```

---

## Daily Workflow

**Morning (Starting work):**
1. `gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001`
2. Wait 30 seconds
3. `cd C:\dev && .\.venv\Scripts\Activate.ps1`
4. `python beca_gui.py`
5. Open browser to http://127.0.0.1:7860

**Evening (Ending work):**
1. Close browser
2. Press `Ctrl+C` in PowerShell
3. `gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001`

This workflow will save you ~$3/day compared to leaving your SPOT VM running 24/7! (And ~$205/month vs standard pricing!)
