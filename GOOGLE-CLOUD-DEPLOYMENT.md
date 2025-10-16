# BECA Google Cloud Deployment Guide

This guide walks you through deploying BECA to Google Cloud Run using Docker containers.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed locally (optional, for local testing)
4. **Project ID** - You'll need a Google Cloud project

## Quick Start Deployment

### Option 1: Automated Deployment (Recommended)

Run the deployment script:

```bash
# Make the script executable (Mac/Linux)
chmod +x deploy-to-gcloud.sh
./deploy-to-gcloud.sh

# For Windows, use Git Bash or WSL
bash deploy-to-gcloud.sh
```

This script will:
- ✅ Check if gcloud is installed
- ✅ Enable required Google Cloud APIs
- ✅ Build Docker images for frontend and backend
- ✅ Push images to Google Container Registry
- ✅ Deploy both services to Cloud Run
- ✅ Output the URLs for accessing your deployed BECA

### Option 2: Manual Deployment

#### Step 1: Set up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

#### Step 2: Build and Push Docker Images

**Backend:**
```bash
cd api
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/beca-api:latest .
cd ..
```

**Frontend:**
```bash
cd frontend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/beca-frontend:latest .
cd ..
```

#### Step 3: Deploy to Cloud Run

**Deploy Backend API:**
```bash
gcloud run deploy beca-api \
  --image gcr.io/YOUR_PROJECT_ID/beca-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

**Get the backend URL:**
```bash
BACKEND_URL=$(gcloud run services describe beca-api --region us-central1 --format 'value(status.url)')
echo $BACKEND_URL
```

**Deploy Frontend:**
```bash
gcloud run deploy beca-frontend \
  --image gcr.io/YOUR_PROJECT_ID/beca-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 80 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

**Get the frontend URL:**
```bash
FRONTEND_URL=$(gcloud run services describe beca-frontend --region us-central1 --format 'value(status.url)')
echo $FRONTEND_URL
```

## Local Docker Testing (Optional)

Test the containers locally before deploying:

```bash
# Build and run with docker-compose
docker-compose up --build

# Access at:
# Frontend: http://localhost:80
# Backend: http://localhost:8000
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Google Cloud Run                │
│                                         │
│  ┌──────────────┐    ┌───────────────┐ │
│  │              │    │               │ │
│  │   Frontend   │───▶│   Backend     │ │
│  │   (Nginx)    │    │   (FastAPI)   │ │
│  │   Port 80    │    │   Port 8000   │ │
│  │              │    │               │ │
│  └──────────────┘    └───────────────┘ │
│         │                    │          │
└─────────┼────────────────────┼──────────┘
          │                    │
          ▼                    ▼
     User Browser          API Calls
```

## Configuration Files

- `api/Dockerfile` - Backend container configuration
- `frontend/Dockerfile` - Frontend multi-stage build
- `frontend/nginx.conf` - Nginx proxy configuration
- `docker-compose.yml` - Local development setup
- `cloudbuild.yaml` - CI/CD pipeline configuration
- `deploy-to-gcloud.sh` - Automated deployment script

## Features

### Backend (FastAPI)
- RESTful API endpoints
- WebSocket support for real-time chat
- CORS enabled for cross-origin requests
- Plan/Act mode context injection
- File system operations

### Frontend (React + TypeScript)
- Three-panel VS Code-inspired interface
- Plan/Act mode toggle
- File tree navigation
- Code viewer with syntax highlighting
- Diff viewer for changes
- Real-time status indicators

## Cost Estimation

Google Cloud Run pricing (approximate):
- **Backend:** ~$5-20/month (1 GB RAM, light usage)
- **Frontend:** ~$2-10/month (512 MB RAM, light usage)
- **Container Registry:** ~$0.10/GB/month for storage
- **Free Tier:** 2 million requests/month included

## Scaling

Cloud Run automatically scales based on traffic:
- **Minimum instances:** 0 (scales to zero when not in use)
- **Maximum instances:** 10 (configurable)
- **Concurrent requests:** Up to 1000 per instance

## Monitoring

View logs and metrics:

```bash
# View backend logs
gcloud run services logs read beca-api --region us-central1

# View frontend logs
gcloud run services logs read beca-frontend --region us-central1

# Open Cloud Console
gcloud console
```

## Updating the Deployment

To update after making changes:

```bash
# Re-run the deployment script
./deploy-to-gcloud.sh

# Or manually rebuild and redeploy
cd api
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/beca-api:latest .
gcloud run deploy beca-api --image gcr.io/YOUR_PROJECT_ID/beca-api:latest --region us-central1
```

## Troubleshooting

### Issue: CORS errors
**Solution:** Update the CORS origins in `api/main.py` to include your Cloud Run frontend URL.

### Issue: Build fails
**Solution:** Check that all files are present and Docker is working locally first.

### Issue: Service won't start
**Solution:** Check logs with `gcloud run services logs read SERVICE_NAME --region us-central1`

### Issue: 503 errors
**Solution:** Increase memory or CPU allocation in the deployment command.

## Security Considerations

1. **Authentication:** Currently allows unauthenticated access. Add Cloud Run IAM for production.
2. **HTTPS:** Automatically enabled by Cloud Run
3. **Secrets:** Use Google Secret Manager for sensitive data
4. **CORS:** Configure properly for your domain

## Next Steps

1. Set up a custom domain
2. Configure Cloud Build triggers for CI/CD
3. Add authentication with Cloud IAM
4. Set up monitoring alerts
5. Configure backup for persistent data

## Support

For issues or questions:
- Google Cloud Run Docs: https://cloud.google.com/run/docs
- Docker Documentation: https://docs.docker.com
- FastAPI Documentation: https://fastapi.tiangolo.com
- React Documentation: https://react.dev
