@echo off
echo.
echo ==========================================
echo Deploying New BECA React Frontend
echo ==========================================
echo.

echo [1/5] Copying updated docker-compose.yml to VM...
gcloud compute scp docker/docker-compose.yml beca-ollama:/opt/beca/docker/ --zone=us-central1-b
echo.

echo [2/5] Copying API files to VM...
gcloud compute scp --recurse api beca-ollama:/opt/beca/ --zone=us-central1-b
echo.

echo [3/5] Copying frontend files to VM...
gcloud compute scp --recurse frontend beca-ollama:/opt/beca/ --zone=us-central1-b
echo.

echo [4/5] Copying src directory to VM...
gcloud compute scp --recurse src beca-ollama:/opt/beca/ --zone=us-central1-b
echo.

echo [5/5] Stopping old containers and starting new ones...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca && sudo docker-compose -f docker/docker-compose.yml down && sudo docker-compose -f docker/docker-compose.yml up -d --build"
echo.

echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Waiting 60 seconds for containers to fully start...
timeout /t 60 /nobreak
echo.

for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i

echo ==========================================
echo New BECA URLs:
echo ==========================================
echo Frontend (React):  http://%BECA_IP%:3000
echo Backend (FastAPI): http://%BECA_IP%:8000/docs
echo Portainer:         http://%BECA_IP%:9000
echo MCP Server:        http://%BECA_IP%:8080
echo.
echo Opening React frontend in browser...
start http://%BECA_IP%:3000
echo.
pause
