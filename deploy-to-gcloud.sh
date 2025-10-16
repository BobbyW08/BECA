#!/bin/bash

# BECA Google Cloud Deployment Script
# This script deploys BECA frontend and backend to Google Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 BECA Google Cloud Deployment${NC}"
echo "================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}No project configured. Please set your project:${NC}"
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}Project ID: $PROJECT_ID${NC}"
echo ""

# Enable required APIs
echo -e "${YELLOW}Enabling required Google Cloud APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com

echo ""
echo -e "${YELLOW}Building and pushing Docker images...${NC}"

# Build and push backend image
echo -e "${GREEN}Building backend image...${NC}"
cd api
gcloud builds submit --tag gcr.io/$PROJECT_ID/beca-api:latest .
cd ..

# Build and push frontend image  
echo -e "${GREEN}Building frontend image...${NC}"
cd frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/beca-frontend:latest .
cd ..

echo ""
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"

# Deploy backend
echo -e "${GREEN}Deploying backend API...${NC}"
gcloud run deploy beca-api \
    --image gcr.io/$PROJECT_ID/beca-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8000 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10

# Get backend URL
BACKEND_URL=$(gcloud run services describe beca-api --region us-central1 --format 'value(status.url)')
echo -e "${GREEN}Backend deployed at: $BACKEND_URL${NC}"

# Deploy frontend
echo -e "${GREEN}Deploying frontend...${NC}"
gcloud run deploy beca-frontend \
    --image gcr.io/$PROJECT_ID/beca-frontend:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 80 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars REACT_APP_API_URL=$BACKEND_URL

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe beca-frontend --region us-central1 --format 'value(status.url)')

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${GREEN}Frontend URL: $FRONTEND_URL${NC}"
echo -e "${GREEN}Backend API URL: $BACKEND_URL${NC}"
echo ""
echo -e "${YELLOW}Note: You may need to update CORS settings in the backend${NC}"
echo -e "${YELLOW}to allow requests from the frontend URL.${NC}"
echo ""
