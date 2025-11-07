@echo off
REM BECA Startup Validator - Check all services are healthy
echo ==========================================
echo BECA Startup Validator
echo ==========================================
echo.

REM Get VM IP
echo [1/6] Getting BECA VM IP...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i

if "%BECA_IP%"=="" (
    echo [FAIL] Could not get VM IP
    exit /b 1
)
echo [OK] VM IP: %BECA_IP%
echo.

REM Check VM is running
echo [2/6] Checking VM status...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)"') do set VM_STATUS=%%i
if "%VM_STATUS%"=="RUNNING" (
    echo [OK] VM is RUNNING
) else (
    echo [FAIL] VM status: %VM_STATUS%
    exit /b 1
)
echo.

REM Check Backend with retries
echo [3/6] Checking BECA Backend (http://%BECA_IP%:8000/health)...
set RETRY=0
:BACKEND_RETRY
set /a RETRY+=1
if %RETRY% gtr 30 (
    echo [FAIL] Backend not responding after 30 attempts
    echo Try: gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps"
    exit /b 1
)

curl -s -f http://%BECA_IP%:8000/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo   Attempt %RETRY%/30 - Backend not ready yet, waiting 2 seconds...
    timeout /t 2 /nobreak >nul
    goto BACKEND_RETRY
)
echo [OK] Backend is healthy (responded in %RETRY% attempts)
echo.

REM Check Frontend with retries
echo [4/6] Checking BECA Frontend (http://%BECA_IP%:3000)...
set RETRY=0
:FRONTEND_RETRY
set /a RETRY+=1
if %RETRY% gtr 30 (
    echo [FAIL] Frontend not responding after 30 attempts
    exit /b 1
)

curl -s -f http://%BECA_IP%:3000 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo   Attempt %RETRY%/30 - Frontend not ready yet, waiting 2 seconds...
    timeout /t 2 /nobreak >nul
    goto FRONTEND_RETRY
)
echo [OK] Frontend is healthy (responded in %RETRY% attempts)
echo.

REM Check Ollama
echo [5/6] Checking Ollama API (http://%BECA_IP%:11434)...
curl -s -f http://%BECA_IP%:11434 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARN] Ollama may not be fully ready
) else (
    echo [OK] Ollama is responding
)
echo.

REM Check Portainer
echo [6/6] Checking Portainer (http://%BECA_IP%:9000)...
curl -s -f http://%BECA_IP%:9000 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARN] Portainer may not be ready
) else (
    echo [OK] Portainer is responding
)
echo.

echo ==========================================
echo [SUCCESS] All critical services are healthy!
echo ==========================================
echo.
echo Access URLs:
echo   Theia IDE:      http://%BECA_IP%:3000
echo   BECA Backend:   http://%BECA_IP%:8000/docs
echo   Portainer:      http://%BECA_IP%:9000
echo   MCP Server:     http://%BECA_IP%:8080
echo.
echo BECA is ready to use!
echo.
