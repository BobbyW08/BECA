@echo off
echo.
echo ==========================================
echo Starting BECA VM...
echo ==========================================
echo.

REM Check if VM is already running
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)" 2^>nul') do set VM_STATUS=%%i

if "%VM_STATUS%"=="RUNNING" (
    echo VM is already RUNNING
    echo.
) else if "%VM_STATUS%"=="TERMINATED" (
    echo VM is stopped. Starting now...
    gcloud compute instances start beca-ollama --zone=us-central1-b
    echo.
    echo Waiting 30 seconds for VM to boot...
    timeout /t 30 /nobreak
    echo.
) else (
    echo ERROR: Unexpected VM status: %VM_STATUS%
    echo Please check VM status manually with: gcloud compute instances list
    pause
    exit /b 1
)

echo ==========================================
echo Getting VM External IP...
echo ==========================================
echo.
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i

if "%BECA_IP%"=="" (
    echo ERROR: Could not get VM IP address
    pause
    exit /b 1
)

echo Current IP: %BECA_IP%
echo.

echo ==========================================
echo Checking BECA Services...
echo ==========================================
echo.
echo This will wait until all services are ready...
echo (Usually takes 30-90 seconds after VM start)
echo.

REM Check Backend with retries (up to 2 minutes)
echo [1/2] Waiting for BECA Backend...
set RETRY=0
:BACKEND_RETRY
set /a RETRY+=1
if %RETRY% gtr 60 (
    echo.
    echo [WARNING] Backend did not respond after 60 attempts ^(2 minutes^)
    echo.
    echo This could mean:
    echo   1. Containers are still starting up ^(wait a bit longer^)
    echo   2. There's an issue with the Docker containers
    echo.
    echo To check container status:
    echo   gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps"
    echo.
    echo To view backend logs:
    echo   gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-backend"
    echo.
    set /p CONTINUE="Continue anyway and open browser? (Y/N): "
    if /i "%CONTINUE%"=="Y" goto OPEN_BROWSER
    exit /b 1
)

curl -s -f -m 5 http://%BECA_IP%:8000/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo   Attempt %RETRY%/60 - Backend starting... ^(waiting 2 seconds^)
    timeout /t 2 /nobreak >nul
    goto BACKEND_RETRY
)
echo [OK] Backend is healthy! ^(responded after %RETRY% checks^)
echo.

REM Check Frontend with retries
echo [2/2] Waiting for BECA Frontend...
set RETRY=0
:FRONTEND_RETRY
set /a RETRY+=1
if %RETRY% gtr 60 (
    echo.
    echo [WARNING] Frontend did not respond after 60 attempts
    echo.
    echo To check frontend status:
    echo   gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker logs beca-frontend"
    echo.
    set /p CONTINUE="Continue anyway and open browser? (Y/N): "
    if /i "%CONTINUE%"=="Y" goto OPEN_BROWSER
    exit /b 1
)

curl -s -f -m 5 http://%BECA_IP%:3000 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo   Attempt %RETRY%/60 - Frontend starting... ^(waiting 2 seconds^)
    timeout /t 2 /nobreak >nul
    goto FRONTEND_RETRY
)
echo [OK] Frontend is healthy! ^(responded after %RETRY% checks^)
echo.

:OPEN_BROWSER
echo ==========================================
echo [SUCCESS] BECA is Ready!
echo ==========================================
echo.
echo Opening BECA in your browser...
echo.
start http://%BECA_IP%:3000
echo.

echo ==========================================
echo Access URLs:
echo ==========================================
echo   BECA Frontend:  http://%BECA_IP%:3000
echo   BECA Backend:   http://%BECA_IP%:8000/docs
echo   Portainer:      http://%BECA_IP%:9000
echo   MCP Server:     http://%BECA_IP%:8080
echo   Ollama:         http://%BECA_IP%:11434
echo.
echo ==========================================
echo Useful Commands:
echo ==========================================
echo   Stop VM (save costs):  stop-beca.bat
echo   Get current IP:        get-beca-ip.bat
echo   Check status:          validate-startup.bat
echo   Test agent:            test-agent.bat
echo   Diagnose issues:       diagnose-beca.bat
echo.
echo Press any key to close this window...
pause >nul
