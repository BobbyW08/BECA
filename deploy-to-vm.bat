@echo off
echo ==========================================
echo BECA VM Deployment Script
echo ==========================================
echo.
echo This script will:
echo   1. Check if VM is running
echo   2. Pull latest code from GitHub to VM
echo   3. Rebuild Docker images on VM
echo   4. Restart containers with new images
echo.
pause
echo.

echo [1/5] Checking VM Status...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)" 2^>nul') do set VM_STATUS=%%i

if not "%VM_STATUS%"=="RUNNING" (
    echo ERROR: VM is not running (Status: %VM_STATUS%)
    echo Please start the VM first with: start-beca.bat
    pause
    exit /b 1
)
echo [OK] VM is running
echo.

echo [2/5] Pulling latest code from GitHub to VM...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca && git pull origin main"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to pull code from GitHub
    pause
    exit /b 1
)
echo [OK] Code updated
echo.

echo [3/5] Stopping current containers...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose down"
echo [OK] Containers stopped
echo.

echo [4/5] Rebuilding Docker images...
echo This may take 5-10 minutes...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose build --no-cache"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to rebuild images
    pause
    exit /b 1
)
echo [OK] Images rebuilt
echo.

echo [5/5] Starting containers with new images...
gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose up -d"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)
echo [OK] Containers started
echo.

echo ==========================================
echo Deployment Complete!
echo ==========================================
echo.
echo Waiting 30 seconds for services to start...
timeout /t 30 /nobreak
echo.

echo Getting VM IP...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i
echo.
echo ==========================================
echo Access BECA at: http://%BECA_IP%:3000
echo ==========================================
echo.
echo To check logs:
echo   Backend:  gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs -f beca-backend"
echo   Frontend: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs -f beca-frontend"
echo.
pause
