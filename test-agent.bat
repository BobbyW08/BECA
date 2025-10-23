@echo off
REM Test BECA Agent - Verify timeout fix and functionality
echo ==========================================
echo BECA Agent Test Script
echo ==========================================
echo.

REM Get VM IP
echo [1/3] Getting BECA VM IP...
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i

if "%BECA_IP%"=="" (
    echo ERROR: Could not get VM IP
    pause
    exit /b 1
)

echo VM IP: %BECA_IP%
echo.

REM Check backend is accessible
echo [2/3] Checking BECA backend...
curl -s -f http://%BECA_IP%:8000/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Backend not responding at http://%BECA_IP%:8000/health
    echo Please ensure BECA is started with start-beca.bat
    pause
    exit /b 1
)
echo Backend is healthy!
echo.

REM Test agent with a simple task
echo [3/3] Testing agent with simple task...
echo.
echo Sending test request to agent...
echo Task: "List the files in the src directory"
echo.

curl -s -X POST http://%BECA_IP%:8000/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"List the files in the src directory\",\"mode\":\"act\",\"history\":[]}"

echo.
echo.
echo ==========================================
echo Test Complete
echo ==========================================
echo.
echo If you saw a JSON response above with file listings, the agent is working!
echo.
echo To test a more complex task, access: http://%BECA_IP%:3000
echo.
pause
