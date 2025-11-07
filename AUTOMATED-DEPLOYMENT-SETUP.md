# BECA Automated Deployment Setup

This guide explains how to set up the automated CI/CD pipeline using GitHub Actions and Watchtower.

## 🎯 How It Works

```
Developer                GitHub Actions              GCR                VM (Watchtower)
    |                          |                      |                        |
    |-- git push ----------->  |                      |                        |
    |                          |                      |                        |
    |                          |-- Build Images ----> |                        |
    |                          |-- Push Images -----> |                        |
    |                          |                      |                        |
    |                          |                      |<-- Poll every 5 min ---|
    |                          |                      |                        |
    |                          |                      |-- New image detected ->|
    |                          |                      |                        |
    |                          |                      |<-- Pull & Deploy ------|
    |                          |                      |                        |
    |                          |                      |                 ✅ Updated
```

**Workflow:**
1. You push code to GitHub
2. GitHub Actions automatically builds Docker images
3. Images are pushed to Google Container Registry (GCR)
4. Watchtower on VM checks GCR every 5 minutes
5. When new images are found, Watchtower automatically updates containers
6. Old images are cleaned up automatically

## 📋 Prerequisites

- GCP Project: `beca-0001` (already set up)
- VM: `beca-ollama` in `us-central1-b` (already running)
- Docker installed on VM (already set up)
- GitHub repository with BECA code

## 🔧 Setup Instructions

### Step 1: Create GCP Service Account

1. **Create Service Account:**
```bash
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions" \
    --project=beca-0001
```

2. **Grant Permissions:**
```bash
# Allow pushing to GCR
gcloud projects add-iam-policy-binding beca-0001 \
    --member="serviceAccount:github-actions@beca-0001.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Allow Cloud Build (optional)
gcloud projects add-iam-policy-binding beca-0001 \
    --member="serviceAccount:github-actions@beca-0001.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"
```

3. **Create and Download Key:**
```bash
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions@beca-0001.iam.gserviceaccount.com
```

**⚠️ IMPORTANT:** Keep `github-actions-key.json` secure! Don't commit it to Git.

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

**Secret Name:** `GCP_SA_KEY`
**Secret Value:** Paste the entire contents of `github-actions-key.json`

```json
{
  "type": "service_account",
  "project_id": "beca-0001",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  ...
}
```

### Step 3: Configure VM to Pull from GCR

SSH into your VM and configure Docker to authenticate with GCR:

```bash
# SSH to VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Configure Docker for GCR
gcloud auth configure-docker gcr.io

# Update docker-compose.yml on VM
cd /home/robwa/BECA
git pull origin main

# Start Watchtower (will auto-start with docker-compose)
cd docker
sudo docker-compose up -d watchtower
```

### Step 4: Initial Image Build (One-Time)

Since the VM now expects GCR images, we need to build and push initial images:

**Option A: Using GitHub Actions (Recommended)**
1. Push any change to the main branch (even just updating README.md)
2. GitHub Actions will build and push images automatically
3. Check progress at: `https://github.com/YOUR_USERNAME/BECA/actions`

**Option B: Manual Build**
```bash
# Authenticate
gcloud auth configure-docker gcr.io

# Build and push from your local machine
cd c:\dev

docker build -t gcr.io/beca-0001/beca-backend:latest api
docker push gcr.io/beca-0001/beca-backend:latest

docker build -t gcr.io/beca-0001/beca-frontend:latest frontend-theia
docker push gcr.io/beca-0001/beca-frontend:latest

docker build -t gcr.io/beca-0001/beca-mcp:latest -f docker/Dockerfile.mcp .
docker push gcr.io/beca-0001/beca-mcp:latest
```

### Step 5: Deploy to VM

Once images are in GCR, deploy them to the VM:

```bash
# SSH to VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Pull latest docker-compose.yml
cd /home/robwa/BECA
git pull origin main

# Pull images from GCR
cd docker
sudo docker-compose pull

# Start services
sudo docker-compose up -d

# Verify Watchtower is running
sudo docker ps | grep watchtower
```

## 🚀 Usage

### Deploying Changes

Simply push to the main branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

**What happens next:**
1. GitHub Actions builds new images (~5-10 minutes)
2. Images are pushed to GCR
3. Watchtower detects new images (within 5 minutes)
4. Containers are automatically updated on VM
5. Old images are cleaned up

**Total time:** ~10-15 minutes from push to deployment

### Monitoring Deployments

**GitHub Actions:**
- View build progress: `https://github.com/YOUR_USERNAME/BECA/actions`
- Each workflow run shows:
  - Build status for each image
  - Build logs
  - Deployment summary

**VM Logs:**
```bash
# SSH to VM
gcloud compute ssh beca-ollama --zone=us-central1-b

# Check Watchtower logs
sudo docker logs watchtower -f

# Check if containers updated
sudo docker ps

# Check when image was pulled
sudo docker images | grep beca
```

### Manual Deployment Trigger

You can manually trigger a deployment without code changes:

1. Go to GitHub: **Actions** → **Build and Deploy BECA**
2. Click **Run workflow** → **Run workflow**
3. Wait for build to complete
4. Watchtower will auto-deploy within 5 minutes

## 🔍 Verification

After deployment, verify everything works:

```bash
# Check all containers are running
sudo docker ps

# Expected containers:
# - beca-backend
# - beca-frontend
# - ollama-gpu
# - mcp-server
# - portainer
# - watchtower

# Check container health
sudo docker-compose ps

# View logs
sudo docker-compose logs beca-frontend
sudo docker-compose logs beca-backend
```

**Test the application:**
- Frontend: `http://34.68.179.152:3000`
- Backend: `http://34.68.179.152:8000/docs`
- Portainer: `http://34.68.179.152:9000`

## 🛠️ Troubleshooting

### Images Not Updating

**Check Watchtower logs:**
```bash
sudo docker logs watchtower
```

**Common issues:**
- GCR authentication failed → Re-run `gcloud auth configure-docker`
- Wrong image names → Check docker-compose.yml uses `gcr.io/beca-0001/...`
- Network issues → Check VM has internet access

**Force manual update:**
```bash
cd /home/robwa/BECA/docker
sudo docker-compose pull
sudo docker-compose up -d --force-recreate
```

### GitHub Actions Failing

**Check build logs:**
1. Go to Actions tab in GitHub
2. Click on failed workflow
3. Expand failed step

**Common issues:**
- `GCP_SA_KEY` secret not set → Add secret in GitHub settings
- Service account lacks permissions → Grant roles (see Step 1)
- Dockerfile errors → Fix syntax in Dockerfile

### Container Won't Start

**Check logs:**
```bash
sudo docker logs beca-frontend
sudo docker logs beca-backend
```

**Common issues:**
- Port already in use → Stop conflicting services
- Missing environment variables → Check .env file
- Image pull failed → Check GCR permissions

### Cleanup Old Resources

Watchtower auto-cleans images, but you can manually clean:

```bash
# Remove unused containers
sudo docker container prune -f

# Remove unused images
sudo docker image prune -a -f

# Remove unused volumes
sudo docker volume prune -f

# Remove unused networks
sudo docker network prune -f
```

## ⚙️ Configuration

### Watchtower Settings

Edit `docker-compose.yml` to adjust Watchtower behavior:

```yaml
watchtower:
  environment:
    - WATCHTOWER_POLL_INTERVAL=300  # Check every 5 minutes (default)
    # Change to 60 for 1 minute, 3600 for 1 hour, etc.
    
    - WATCHTOWER_CLEANUP=true  # Remove old images
    - WATCHTOWER_ROLLING_RESTART=true  # Update one at a time
    
    # Add email notifications (optional)
    - WATCHTOWER_NOTIFICATIONS=email
    - WATCHTOWER_NOTIFICATION_EMAIL_TO=your@email.com
    - WATCHTOWER_NOTIFICATION_EMAIL_FROM=watchtower@beca.com
    - WATCHTOWER_NOTIFICATION_EMAIL_SERVER=smtp.gmail.com
```

### GitHub Actions Triggers

Edit `.github/workflows/deploy.yml` to change when builds trigger:

```yaml
on:
  push:
    branches:
      - main          # Deploy on main branch pushes
      - staging       # Add more branches
    paths:            # Only build when these paths change
      - 'api/**'
      - 'frontend-theia/**'
      - 'docker/**'
      - 'src/**'
```

## 📊 Cost Optimization

**GitHub Actions:**
- Free tier: 2,000 minutes/month (plenty for BECA)
- Each build: ~5-10 minutes
- Monthly builds: 200-400 (assuming 10 deployments/day)

**GCR Storage:**
- Free tier: 5GB
- Each image set: ~2GB (backend + frontend + mcp)
- Keep 2-3 versions: ~6GB
- Watchtower auto-cleans old images

**VM Runtime:**
- Already running 24/7 for BECA
- Watchtower: Negligible CPU/memory (~20MB)
- No additional cost

## 🔐 Security Best Practices

1. **Never commit** `github-actions-key.json` to Git
2. **Rotate service account keys** every 90 days
3. **Use least privilege** - only grant necessary roles
4. **Enable branch protection** on main branch
5. **Review deployment logs** regularly
6. **Keep Watchtower updated** - it auto-updates itself!

## 📚 Additional Resources

- [Watchtower Documentation](https://containrrr.dev/watchtower/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GCR Documentation](https://cloud.google.com/container-registry/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🎉 Success!

Your automated deployment pipeline is now set up! From now on:

```bash
git commit -m "Fix bug in chat widget"
git push origin main
# ☕ Wait 10-15 minutes
# ✅ Deployed automatically!
```

No more manual SSH, no more forgetting to deploy, no more copying files. Just push and go! 🚀
