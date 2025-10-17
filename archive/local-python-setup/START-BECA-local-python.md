# 🚀 How to Start BECA

**Simple, step-by-step instructions to get BECA running.**

---

## Prerequisites (One-Time Setup)

Before starting BECA for the first time:

1. ✅ **Python 3.8+** installed
2. ✅ **Virtual environment** created at `C:\dev\beca-env`
3. ✅ **Dependencies** installed (see First-Time Setup below)
4. ✅ **Google Cloud VM** running with Ollama (see Cloud Setup below)

---

## Quick Start (Every Time)

### 1. Start the Cloud GPU VM

```powershell
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001
```

Wait 30 seconds for the VM to fully start.

### 2. Activate Virtual Environment

```powershell
cd C:\dev
.\beca-env\Scripts\Activate.ps1
```

You should see `(beca-env)` in your prompt.

### 3. Launch BECA

```powershell
python beca_gui.py
```

BECA will automatically open in your browser at **http://127.0.0.1:7860**

**Done!** 🎉

---

## First-Time Setup

Only do this once when setting up BECA on a new machine:

### 1. Create Virtual Environment

```powershell
cd C:\dev
python -m venv beca-env
```

### 2. Activate Environment

```powershell
.\beca-env\Scripts\Activate.ps1
```

### 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs **18 essential packages** (reduced from 109!):
- LangChain framework for AI agents
- Gradio for the web UI
- Google Drive integration
- Code viewer with syntax highlighting
- Memory & knowledge systems

Installation takes ~1-2 minutes (down from 5+ minutes with old bloated requirements).

---

## Cloud GPU Setup

Your BECA uses a Google Cloud VM with GPU for fast AI inference:

### VM Details
- **Instance**: `beca-ollama`
- **Zone**: `us-central1-b`
- **Type**: n1-standard-4 with NVIDIA T4 GPU
- **Pricing**: SPOT instance (~$0.17/hr, saves 74%)
- **Ollama URL**: `http://34.46.140.140:11434`
- **Models**: Llama 3.1 8B + Qwen2.5-Coder 7B

### Quick Commands

```powershell
# Start VM
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# Stop VM (when done to save money)
gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001

# Check VM status
gcloud compute instances list --project=beca-0001

# Test Ollama connection
curl http://34.46.140.140:11434/api/tags
```

### Cost Management

**Always stop the VM when not using BECA!**

- Running (SPOT): ~$0.17/hour (~$4/day if left on 24/7)
- Stopped: ~$0.07/day (only disk storage)
- Monthly if left on: ~$125/month
- Monthly with smart usage: ~$10-20/month ✅

**Best Practice**: Start in morning, stop in evening = ~$3/day savings

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'gradio'"

**Problem**: Wrong Python environment or dependencies not installed

**Solution**:
```powershell
# Make sure you're in the virtual environment
.\beca-env\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ "Connection refused" to Ollama

**Problem**: VM is stopped or Ollama isn't running

**Solution**:
```powershell
# Check VM status
gcloud compute instances list --project=beca-0001

# If stopped, start it
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# Wait 30 seconds, then test
curl http://34.46.140.140:11434/api/tags
```

### ❌ Firewall blocking connection

**Problem**: Your IP address changed (different network)

**Solution**:
```powershell
python setup_firewall.py
```

### ❌ BECA is slow

**Possible causes**:
1. High network latency to VM
2. GPU not being used on VM

**Check GPU usage**:
```powershell
gcloud compute ssh beca-ollama --zone=us-central1-b --command="nvidia-smi"
```

**Check network latency**:
```powershell
ping 34.46.140.140
```

If ping > 100ms, consider switching to a closer region.

---

## Google Drive Integration

BECA can read and write files directly from your Google Drive!

### First-Time Setup

1. Get Google Drive API credentials:
   - Go to: https://console.cloud.google.com/
   - Enable Google Drive API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` in `C:\dev\`

2. First time you use Google Drive with BECA:
   - BECA will open a browser for authentication
   - Grant access to your Drive
   - Token will be saved for future use

### What You Can Do

- Read PDFs, Word docs, Google Docs from Drive
- Process Excel/Sheets files from Drive
- Upload BECA's generated files to Drive
- Sync entire folders

**No need for local file upload libraries** - Google Drive handles everything!

---

## Daily Workflow

### Morning (Starting Work)
```powershell
# 1. Start VM
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001

# 2. Wait 30 seconds, then activate environment
cd C:\dev
.\beca-env\Scripts\Activate.ps1

# 3. Launch BECA
python beca_gui.py
```

### Evening (Ending Work)
```powershell
# 1. Close browser
# 2. Press Ctrl+C in terminal
# 3. Stop VM to save money
gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001
```

**This workflow saves ~$3/day vs leaving VM running 24/7!**

---

## Features

### 🎯 Visual Interface
- **File Tree Panel**: See your project structure
- **Chat Panel**: Talk to BECA
- **Code Viewer**: View files with syntax highlighting
- **Diff Viewer**: Compare before/after changes

### 🧠 Learning Systems
- **Memory**: BECA remembers conversations and preferences
- **Meta-Learning**: Learns from every feature you build
- **Auto-Learning**: Continuously learns from docs and code
- **Knowledge Base**: Stores patterns and lessons

### 🛠️ Capabilities
- Build full applications (React, Flask, FastAPI)
- Debug and fix code
- Analyze codebases
- Remember your preferences
- Work with Google Drive files
- Generate and run tests
- Use 39+ development tools

---

## Quick Reference

```powershell
# Essential Commands
gcloud compute instances start beca-ollama --zone=us-central1-b --project=beca-0001
gcloud compute instances stop beca-ollama --zone=us-central1-b --project=beca-0001
gcloud compute instances list --project=beca-0001
.\beca-env\Scripts\Activate.ps1
python beca_gui.py
```

---

## Need Help?

- Check this guide first
- Review error messages in terminal
- Verify VM is running
- Confirm you're in the virtual environment
- Test Ollama connection

---

**Built with ❤️ for efficient AI-assisted development**
