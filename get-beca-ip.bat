@echo off
echo.
echo ==========================================
echo Getting BECA VM External IP Address...
echo ==========================================
echo.
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i
echo.
echo ==========================================
echo Current BECA External IP: %BECA_IP%
echo ==========================================
echo.
echo Access BECA at:
echo.
echo   Theia IDE: http://%BECA_IP%:3000
echo   Backend:   http://%BECA_IP%:8000
echo   Portainer: http://%BECA_IP%:9000
echo   MCP:       http://%BECA_IP%:8080
echo   Ollama:    http://%BECA_IP%:11434
echo.
echo ==========================================
echo Press any key to close this window...
pause >nul
