@echo off
echo.
echo ==========================================
echo Starting BECA VM...
echo ==========================================
echo.
gcloud compute instances start beca-ollama --zone=us-central1-b
echo.
echo ==========================================
echo Getting VM External IP...
echo ==========================================
echo.
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i
echo Current IP: %BECA_IP%
echo.
echo ==========================================
echo Waiting 90 seconds for containers to start...
echo ==========================================
timeout /t 90 /nobreak
echo.
echo ==========================================
echo Opening BECA in your browser...
echo ==========================================
echo.
start http://%BECA_IP%:7860
echo.
echo Browser should be opening to: http://%BECA_IP%:7860
echo If it doesn't open automatically, copy and paste the URL above.
echo.
echo BECA GUI: http://%BECA_IP%:7860
echo Portainer: http://%BECA_IP%:9000
echo MCP Server: http://%BECA_IP%:8080
echo.
echo Press any key to close this window...
pause >nul
