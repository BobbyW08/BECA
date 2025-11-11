# BECA Routing Configuration

## Complete Data Flow Architecture

### External Access
```
User Device (Laptop/iPad/Phone)
    ↓
http://VM_EXTERNAL_IP:3000
```

### Container Network Architecture
```
┌─────────────────────────────────────────────────────┐
│ GCP VM: beca-ollama (us-central1-b)                 │
│ External IP: Dynamic (changes on restart)           │
├─────────────────────────────────────────────────────┤
│                                                      │
│  PORT 3000 → beca-frontend (Theia IDE)             │
│    └─ Detects VM IP dynamically from browser        │
│    └─ Connects to: http://VM_IP:8000               │
│                                                      │
│  PORT 8000 → beca-backend (FastAPI)                │
│    └─ Ollama connection: http://host.docker.internal:11434 │
│                                                      │
│  HOST PORT 11434 → Native Ollama (on VM host)      │
│    └─ Models: qwen2.5-coder:7b, llama3.1:8b       │
│                                                      │
│  PORT 8080 → mcp-server (optional)                 │
│  PORT 9000 → portainer (optional)                  │
│                                                      │
│  Docker Network: beca-network (172.28.0.0/16)      │
│    └─ All containers communicate via hostnames      │
│       (beca-frontend, beca-backend, mcp-server)     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Configuration Summary

### docker-compose.yml
**Location:** `/opt/beca/docker/docker-compose.yml`

**Image Sources:**
- ✅ beca-backend:latest (local image)
- ✅ beca-frontend:latest (local image)
- ✅ beca-mcp:latest (local image)

**Backend Environment:**
```yaml
OLLAMA_URL=http://host.docker.internal:11434  # Connects to VM host
PYTHONUNBUFFERED=1
API_PORT=8000
```

**Frontend Environment:**
```yaml
BECA_API_URL=http://beca-backend:8000  # Internal Docker network
NODE_ENV=production
```

**Volume Mounts:**
```yaml
backend:
  - ../src:/app/src              # Live code updates
  - beca-memory:/app/data        # Persistent memory
  - beca-workspace:/app/workspace # Workspace files

frontend:
  - beca-workspace:/workspace    # Shared workspace
```

### Frontend API Service
**Location:** `/opt/beca/frontend-theia/beca-extension/src/browser/beca-api-service.ts`

**Dynamic API URL Detection:**
```typescript
const protocol = window.location.protocol; // http:
const hostname = window.location.hostname; // VM_IP
this.apiUrl = `${protocol}//${hostname}:8000`;
```

**Why this works:**
1. User opens http://34.123.235.181:3000
2. Browser loads Theia frontend from VM
3. JavaScript detects hostname = "34.123.235.181"
4. Connects to API at http://34.123.235.181:8000
5. Works from any device without configuration!

### Backend API (main.py)
**Location:** `/opt/beca/api/main.py`

**Ollama Connection:**
```python
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
```

**Path Security:**
```python
# Docker/VM: /workspace
# Local Windows: C:/dev
ALLOWED_BASE_PATH = Path("/workspace").resolve()
```

## Network Flow

### User → Frontend (Port 3000)
```
User Browser (iPad/Laptop)
  → VM_IP:3000
  → nginx in frontend container
  → Theia application serves
  → Returns HTML/JS/CSS
```

### Frontend → Backend (Port 8000)
```
Browser JavaScript
  → Detects VM_IP from window.location
  → Makes AJAX request to http://VM_IP:8000/api/chat
  → Backend receives and processes
  → Returns JSON response
```

### Backend → Ollama (Port 11434)
```
Backend Container
  → host.docker.internal:11434
  → (Docker translates to VM host IP)
  → Native Ollama on VM
  → Returns LLM response
```

### Container-to-Container Communication
```
Frontend → Backend
  Uses Docker network: http://beca-backend:8000
  
MCP → Backend
  Uses Docker network: http://beca-backend:8000
```

## Firewall Rules Required

**GCP Firewall (already configured):**
- TCP 3000: Frontend (Theia IDE)
- TCP 8000: Backend API
- TCP 9000: Portainer (optional)
- TCP 8080: MCP Server (optional)

**Ollama Port 11434:**
- NOT exposed externally (security)
- Only accessible from Docker containers via host.docker.internal

## Development Workflow

### Making Code Changes

**1. Backend Changes (Python):**
```bash
# On laptop: Edit files in c:\dev\src\
git add .
git commit -m "Updated feature"
git push

# SSH to VM:
gcloud compute ssh beca-ollama --zone=us-central1-b
cd /opt/beca
sudo git pull
sudo docker-compose restart beca-backend

# Done! (No rebuild needed - code is mounted)
```

**2. Frontend Changes (TypeScript/React):**
```bash
# Requires image rebuild
# SSH to VM:
cd /opt/beca
sudo git pull
sudo docker-compose build beca-frontend
sudo docker-compose up -d beca-frontend
```

**3. Dependency Changes:**
```bash
# Backend: Update requirements.txt
# Frontend: Update package.json
# Then rebuild respective image
```

## IP Address Management

### Dynamic External IP
- VM uses Spot instance (cheaper)
- External IP changes each time VM starts
- Use `get-beca-ip.bat` to get current IP
- Or check GCP Console

### Internal Docker Network
- Fixed subnet: 172.28.0.0/16
- Container hostnames resolve automatically
- No IP changes needed internally

## Verification Commands

### Check VM Status
```bash
gcloud compute instances list --filter="name=beca-ollama"
```

### Get Current IP
```bash
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### Check Containers Running
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps"
```

### Check Container Logs
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-frontend"
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-backend"
```

### Test Backend Health
```bash
curl http://VM_IP:8000/health
```

### Test Frontend
```bash
curl http://VM_IP:3000
```

### Check Ollama
```bash
gcloud compute ssh beca-ollama --zone=us-central1-b --command="curl http://localhost:11434/api/tags"
```

## Troubleshooting

### Frontend Can't Connect to Backend
**Symptom:** Browser console shows connection refused to port 8000

**Check:**
1. Is backend container running? `sudo docker ps | grep beca-backend`
2. Is port 8000 exposed? `sudo docker port beca-backend`
3. Is firewall open? Check GCP console
4. Check backend logs: `sudo docker logs beca-backend`

### Backend Can't Connect to Ollama
**Symptom:** Backend logs show Ollama connection failed

**Check:**
1. Is Ollama running on host? `systemctl status ollama`
2. Is Ollama accessible? `curl http://localhost:11434/api/tags`
3. Check backend env: `sudo docker exec beca-backend printenv | grep OLLAMA`

### Can't Access from External Device
**Symptom:** iPad/phone can't reach VM_IP:3000

**Check:**
1. Is VM running? Check GCP Console
2. Is correct IP? Run `get-beca-ip.bat`
3. Is firewall open? Check GCP firewall rules
4. Can you ping VM? (May be blocked by GCP)
5. Try from laptop first to isolate network issues

## Summary

✅ **Frontend:** Dynamically detects VM IP, always connects correctly  
✅ **Backend:** Uses host.docker.internal for Ollama, works in any Docker environment  
✅ **Ollama:** Runs natively on VM host, not in container (better GPU access)  
✅ **Volumes:** Code mounted for hot reloading, no rebuild for Python changes  
✅ **Network:** Containers use Docker network, external uses VM IP  
✅ **Security:** Path validation, only /workspace accessible, Ollama not exposed  

**Access Pattern:** User → VM_IP:3000 → Frontend → VM_IP:8000 → Backend → host:11434 → Ollama
