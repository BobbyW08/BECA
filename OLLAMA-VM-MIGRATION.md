# Ollama VM Migration - Complete

## Summary

Successfully migrated from local Windows Ollama to VM's GPU-enabled Ollama.

## Changes Made

### 1. Local Windows Changes
- ✅ Stopped local Ollama processes (`ollama.exe` and `ollama app.exe`)
- ✅ Removed Ollama from Windows startup folder
- ✅ Local Ollama is now disabled

### 2. Docker Compose Configuration
**File:** `docker/docker-compose.yml`

**Changes:**
- Updated `beca-backend` service to use `OLLAMA_URL=http://host.docker.internal:11434`
- Added `extra_hosts` configuration to enable host network access
- Removed `ollama-gpu` Docker container service (no longer needed)
- Removed `depends_on: ollama-gpu` dependency
- Removed `ollama-models` volume (models stored on VM host)

**Configuration:**
```yaml
beca-backend:
  environment:
    - OLLAMA_URL=http://host.docker.internal:11434
  extra_hosts:
    - "host.docker.internal:host-gateway"
```

### 3. VM Configuration
**Native Ollama Status:**
- Running natively on VM (not in Docker)
- Process ID: 44682
- Port: 11434
- GPU: NVIDIA Tesla T4 (15GB VRAM)
- Available models:
  - `llama3.1:8b` (8.0B parameters, Q4_K_M quantization)
  - `qwen2.5-coder:7b-instruct` (7.6B parameters, Q4_K_M quantization)

## Architecture

```
┌──────────────────────────────────────┐
│  BECA Backend Container              │
│  (beca-backend)                      │
│                                      │
│  OLLAMA_URL=host.docker.internal    │
└────────────────┬─────────────────────┘
                 │
                 │ Connect via host gateway
                 ▼
┌──────────────────────────────────────┐
│  VM Host (beca-ollama)               │
│                                      │
│  Native Ollama (PID 44682)          │
│  Port: 11434                         │
│  GPU: Tesla T4 (15GB VRAM)          │
│                                      │
│  Models:                             │
│  - llama3.1:8b                      │
│  - qwen2.5-coder:7b-instruct        │
└──────────────────────────────────────┘
```

## Benefits

1. **GPU Acceleration**: Using NVIDIA T4 GPU for faster inference
2. **Centralized**: All BECA services on VM
3. **No Local Resource Usage**: Ollama no longer running on Windows
4. **Production Ready**: Same setup for dev and production
5. **Cost Efficient**: Maximizing use of existing VM resources

## Verification

### Backend Status
- Container: `beca-backend` - Running
- Health: Starting up (may show unhealthy during restart)
- API: http://35.239.135.54:8000

### Ollama Status
```bash
# On VM:
curl http://localhost:11434/api/tags
# Returns: {"models":[...]}
```

### GPU Status
```bash
nvidia-smi
# Shows: Tesla T4, 15360 MiB total, 0% utilization (idle)
```

## Testing

To test the setup:

```bash
# Get VM IP
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"

# Test BECA API
curl http://[VM_IP]:8000/api/status

# Send chat message
curl -X POST http://[VM_IP]:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "mode": "act"}'
```

## Deployment Commands

```bash
# Commit changes
git add docker/docker-compose.yml
git commit -m "Configure BECA to use native VM Ollama with GPU"
git push origin main

# Deploy to VM
gcloud compute ssh beca-ollama --zone=us-central1-b
cd /opt/beca
sudo git pull origin main
cd docker
sudo docker-compose restart beca-backend
```

## Troubleshooting

### Backend Can't Connect to Ollama

1. Verify Ollama is running on VM:
   ```bash
   sudo ss -tulpn | grep 11434
   ```

2. Check if backend can resolve host.docker.internal:
   ```bash
   sudo docker exec beca-backend ping -c 1 host.docker.internal
   ```

3. Check backend logs:
   ```bash
   sudo docker logs beca-backend --tail=50
   ```

### Ollama Not Using GPU

1. Check GPU availability:
   ```bash
   nvidia-smi
   ```

2. Restart Ollama service:
   ```bash
   sudo systemctl restart ollama
   ```

## Rollback (if needed)

To rollback to Docker-based Ollama:

1. Revert `docker/docker-compose.yml` changes
2. Stop native Ollama: `sudo systemctl stop ollama`
3. Start Docker Ollama: `sudo docker-compose up -d ollama-gpu`

## Date

Completed: November 10, 2025
