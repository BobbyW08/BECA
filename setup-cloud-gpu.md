# BECA Cloud GPU Setup Guide

## Step 1: Enable APIs and Billing (PowerShell)

```powershell
# Set the project
gcloud config set project beca-0001

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

# Check billing status
gcloud beta billing projects describe beca-0001
```

**If billing is not attached**, you need to link a billing account:
1. Go to: https://console.cloud.google.com/billing/linkedaccount?project=beca-0001
2. Link a billing account
3. OR run: `gcloud beta billing projects link beca-0001 --billing-account=BILLING_ACCOUNT_ID`

---

## Step 2: Request GPU Quota (IMPORTANT!)

By default, Google Cloud gives you 0 GPU quota. You must request it:

1. Go to: https://console.cloud.google.com/iam-admin/quotas?project=beca-0001
2. Search for: "GPUs (all regions)"
3. Click the checkbox next to it
4. Click "EDIT QUOTAS" at the top
5. Request increase to: **1**
6. Fill out the form explaining you want to test AI development
7. Submit (usually approved within minutes to hours)

**OR use this direct link:**
https://console.cloud.google.com/apis/api/compute.googleapis.com/quotas?project=beca-0001

---

## Step 3: Create the Spot VM with T4 GPU (PowerShell)

**After quota is approved**, run this command:

```powershell
gcloud compute instances create beca-ollama `
  --project=beca-0001 `
  --zone=us-central1-a `
  --machine-type=n1-standard-2 `
  --accelerator=type=nvidia-tesla-t4,count=1 `
  --provisioning-model=SPOT `
  --instance-termination-action=DELETE `
  --maintenance-policy=TERMINATE `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --boot-disk-size=30GB `
  --boot-disk-type=pd-standard `
  --tags=ollama-server
```

**Expected output:** Instance created successfully with external IP

---

## Step 4: Install Ollama on the VM

```powershell
# SSH into the VM
gcloud compute ssh beca-ollama --zone=us-central1-a --project=beca-0001
```

**Once inside the VM**, run these commands:

```bash
# Update system
sudo apt-get update

# Install NVIDIA drivers (this takes 2-3 minutes)
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service to accept remote connections
sudo systemctl stop ollama
sudo systemctl disable ollama

# Create systemd override to allow remote access
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Verify Ollama is running
sudo systemctl status ollama

# Pull the model (this takes 3-5 minutes for llama3.1:8b)
ollama pull llama3.1:8b

# Verify GPU is detected
nvidia-smi

# Test Ollama locally
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Hello",
  "stream": false
}'

# Exit SSH
exit
```

---

## Step 5: Set Up Firewall Rule (PowerShell)

```powershell
# Get your public IP
$MY_IP = (Invoke-WebRequest -Uri "https://api.ipify.org").Content

# Create firewall rule to allow Ollama access from your IP only
gcloud compute firewall-rules create allow-ollama-from-home `
  --project=beca-0001 `
  --direction=INGRESS `
  --priority=1000 `
  --network=default `
  --action=ALLOW `
  --rules=tcp:11434 `
  --source-ranges="$MY_IP/32" `
  --target-tags=ollama-server `
  --description="Allow Ollama API access from home IP"

# Verify firewall rule
gcloud compute firewall-rules list --project=beca-0001 --filter="name=allow-ollama-from-home"
```

---

## Step 6: Get the VM's External IP

```powershell
gcloud compute instances describe beca-ollama `
  --zone=us-central1-a `
  --project=beca-0001 `
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

**Copy this IP address!** You'll need it for the next step.

---

## Step 7: Test Connection from Your Laptop (PowerShell)

```powershell
# Replace with your VM's IP
$VM_IP = "YOUR_VM_EXTERNAL_IP"

# Test connection
curl "http://${VM_IP}:11434/api/generate" -Method POST -Body '{"model":"llama3.1:8b","prompt":"Hello","stream":false}' -ContentType "application/json"
```

**Expected:** You should get a JSON response with text generation.

---

## Step 8: Update BECA Configuration

Edit `c:\dev\src\langchain_agent.py` line 27:

**Change from:**
```python
OLLAMA_URL = "http://127.0.0.1:11434"
```

**To:**
```python
OLLAMA_URL = "http://YOUR_VM_EXTERNAL_IP:11434"
```

---

## Step 9: Start BECA and Test

```powershell
cd c:\dev
.venv\Scripts\activate
python beca_gui.py
```

Open the browser and test BECA. It should now be using the cloud GPU!

---

## Managing Your VM

### Start VM (when you need it):
```powershell
gcloud compute instances start beca-ollama --zone=us-central1-a --project=beca-0001
```

### Stop VM (to save money):
```powershell
gcloud compute instances stop beca-ollama --zone=us-central1-a --project=beca-0001
```

### Delete VM (when done completely):
```powershell
gcloud compute instances delete beca-ollama --zone=us-central1-a --project=beca-0001
```

### Check VM status:
```powershell
gcloud compute instances list --project=beca-0001
```

### View estimated costs:
Go to: https://console.cloud.google.com/billing?project=beca-0001

---

## Cost Estimates

- **T4 GPU Spot VM**: ~$0.10-0.20/hour
- **Storage (30GB)**: ~$1.20/month (even when stopped)
- **Network egress**: Usually minimal for this use case

**Total if running 8 hours/day**: ~$40-50/month
**Total if running 24/7**: ~$150-200/month

---

## Troubleshooting

### "Quota exceeded" error:
- You need to request GPU quota (Step 2)
- Wait for approval (usually 1-24 hours)

### Can't connect to Ollama:
- Check firewall rule includes your IP: `gcloud compute firewall-rules list`
- Update your IP if it changed: Run Step 5 again
- Verify Ollama is running: SSH in and run `sudo systemctl status ollama`

### VM terminated (spot preemption):
- Just restart it: `gcloud compute instances start beca-ollama`
- Model will still be there on the disk

### Slow responses:
- Check GPU is being used: SSH in and run `nvidia-smi` while making requests
- Verify T4 GPU is attached: `gcloud compute instances describe beca-ollama --zone=us-central1-a`

---

## Next Steps After Testing

1. **Set up budget alerts** to avoid surprise charges
2. **Create snapshots** of your VM disk for quick recreation
3. **Consider reserved instances** if you end up using it 24/7 (much cheaper)
4. **Upgrade to larger models** once you're comfortable (70B models, etc.)
