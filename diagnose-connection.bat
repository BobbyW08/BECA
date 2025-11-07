@echo off
echo.
echo ==========================================
echo BECA Connection Diagnostics
echo ==========================================
echo.

REM Get the current IP
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i

echo [1/5] Current External IP: %BECA_IP%
echo.

echo [2/5] Checking VM Status...
gcloud compute instances list --filter="name=beca-ollama" --format="table(name,status,EXTERNAL_IP)"
echo.

echo [3/5] Checking if Docker containers are running...
echo (SSHing into VM to check Docker status)
echo.
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" 2>nul
if errorlevel 1 (
    echo ERROR: Could not SSH into VM or check Docker containers
    echo The VM might not be fully started yet.
)
echo.

echo [4/5] Checking firewall rules for port 3000 (Theia IDE)...
gcloud compute firewall-rules list --filter="name:beca" --format="table(name,allowed[].ports,sourceRanges)" 2>nul

echo.
echo [5/5] Testing connection to Theia IDE (port 3000)...
echo Attempting to connect to %BECA_IP%:3000...
curl -v -m 5 http://%BECA_IP%:3000 2>&1 | findstr /C:"Connected" /C:"refused" /C:"timeout"
echo.

echo.
echo ==========================================
echo Summary and Next Steps:
echo ==========================================
echo.
echo If Docker shows no containers running:
echo   - Wait another 60 seconds and try again
echo   - Containers may still be starting up
echo.
echo If firewall doesn't show port 3000:
echo   - Run: gcloud compute firewall-rules create beca-frontend --allow=tcp:3000 --source-ranges=0.0.0.0/0 --target-tags=beca
echo.
echo If curl shows "Connection refused":
echo   - SSH into VM and check logs: sudo docker logs beca-frontend
echo   - Check if frontend container is running: sudo docker ps
echo.
echo If you see a VPN icon in your browser:
echo   - Try disabling your VPN temporarily
echo   - VPNs can sometimes block GCP connections
echo.
echo Try accessing Theia IDE at: http://%BECA_IP%:3000
echo.
pause
