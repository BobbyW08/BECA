@echo off
echo.
echo ==========================================
echo Starting BECA VM...
echo ==========================================
echo.
gcloud compute instances start beca-ollama --zone=us-central1-b
echo.
echo Waiting 60 seconds for Docker containers to start...
timeout /t 60 /nobreak
echo.
echo ==========================================
echo Getting VM IP Address...
echo ==========================================
gcloud compute instances list --filter="name=beca-ollama" --format="table(name,EXTERNAL_IP,status)"
echo.
echo ==========================================
echo BECA should be ready in ~2 minutes at:
echo   GUI:      http://YOUR_IP:7860
echo   MCP:      http://YOUR_IP:8080
echo   Portainer: http://YOUR_IP:9000
echo ==========================================
echo.
pause
