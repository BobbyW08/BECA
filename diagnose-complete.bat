@echo off
echo ==========================================
echo BECA Complete Diagnostic Tool
echo ==========================================
echo.

echo [1/8] Checking Google Cloud CLI...
where gcloud >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] gcloud found
    gcloud --version
) else (
    echo [ERROR] gcloud not found - please install Google Cloud SDK
    pause
    exit /b 1
)
echo.

echo [2/8] Checking VM Status...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)" 2^>nul') do set VM_STATUS=%%i
echo VM Status: %VM_STATUS%
if "%VM_STATUS%"=="RUNNING" (
    echo [OK] VM is running
) else if "%VM_STATUS%"=="TERMINATED" (
    echo [WARNING] VM is stopped - run start-beca.bat to start it
) else (
    echo [ERROR] Unexpected VM status or VM not found
)
echo.

echo [3/8] Checking VM External IP...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)" 2^>nul') do set BECA_IP=%%i
if "%BECA_IP%"=="" (
    echo [ERROR] Could not get VM IP - VM may not be running
    echo Run: start-beca.bat
) else (
    echo [OK] VM External IP: %BECA_IP%
)
echo.

if "%BECA_IP%"=="" (
    echo Cannot continue without VM IP. Exiting...
    pause
    exit /b 1
)

echo [4/8] Checking Network Connectivity...
ping -n 1 -w 1000 %BECA_IP% >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Can ping VM
) else (
    echo [WARNING] Cannot ping VM - firewall may be blocking
)
echo.

echo [5/8] Checking BECA Backend (Port 8000)...
curl -s -f -m 5 http://%BECA_IP%:8000/health >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Backend is responding
    curl -s http://%BECA_IP%:8000/health
) else (
    echo [ERROR] Backend not responding
    echo Try: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-backend"
)
echo.

echo [6/8] Checking BECA Frontend (Port 3000)...
curl -s -f -m 5 http://%BECA_IP%:3000 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [OK] Frontend is responding
) else (
    echo [ERROR] Frontend not responding
    echo Try: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-frontend"
)
echo.

echo [7/8] Checking Docker Containers...
echo Running: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
echo.

echo [8/8] Checking Firewall Rules...
gcloud compute firewall-rules list --filter="name~beca" --format="table(name,allowed[].ports,sourceRanges.list())"
echo.

echo ==========================================
echo Diagnostic Summary
echo ==========================================
echo VM IP: %BECA_IP%
echo.
echo Access URLs:
echo   Frontend:  http://%BECA_IP%:3000
echo   Backend:   http://%BECA_IP%:8000/health
echo   Portainer: http://%BECA_IP%:9000
echo.
echo Common Issues:
echo   1. Backend not responding: Check Docker logs
echo   2. Frontend not connecting: Check browser console (F12)
echo   3. Chat not working: Verify backend URL in browser console
echo.
echo Useful Commands:
echo   View backend logs:  gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-backend"
echo   View frontend logs: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-frontend"
echo   Restart containers: gcloud compute ssh beca-ollama --zone=us-central1-b --command="cd /opt/beca/docker && sudo docker-compose restart"
echo.
pause
