@echo off
echo.
echo ==========================================
echo Checking BECA Status...
echo ==========================================
echo.
gcloud compute instances list --filter="name=beca-ollama" --format="table(name,EXTERNAL_IP,status)"
echo.
echo Note the IP address above, then access:
echo   Theia IDE:     http://IP_ADDRESS:3000
echo   BECA Backend:  http://IP_ADDRESS:8000
echo   MCP Server:    http://IP_ADDRESS:8080
echo   Portainer:     http://IP_ADDRESS:9000
echo.
pause
