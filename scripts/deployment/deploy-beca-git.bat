@echo off
echo.
echo ==========================================
echo Deploying BECA via Git (Fast Method)
echo ==========================================
echo.

echo [1/4] Checking for uncommitted changes...
git status --short
echo.

echo [2/4] Pushing latest changes to GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo Error: Failed to push to GitHub. Please commit your changes first.
    echo Run: git add -A && git commit -m "Your message" && git push
    pause
    exit /b 1
)
echo.

echo [3/4] Pulling latest code on VM and rebuilding...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca && sudo git pull origin main && sudo docker-compose -f docker/docker-compose.yml up -d --build"
echo.

echo [4/4] Getting VM IP and opening browser...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i
echo.

echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Waiting 60 seconds for containers to fully start...
timeout /t 60 /nobreak
echo.
echo New BECA URLs:
echo Frontend (React):  http://%BECA_IP%:3000
echo Backend (FastAPI): http://%BECA_IP%:8000/docs
echo Portainer:         http://%BECA_IP%:9000
echo.
echo Opening React frontend...
start http://%BECA_IP%:3000
echo.
pause
