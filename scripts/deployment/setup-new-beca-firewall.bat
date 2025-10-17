@echo off
echo.
echo ==========================================
echo Setting up Firewall Rules for New BECA UI
echo ==========================================
echo.

echo [1/2] Creating firewall rule for BECA Frontend (port 3000)...
gcloud compute firewall-rules create allow-beca-frontend --allow=tcp:3000 --source-ranges=0.0.0.0/0 --description="Allow BECA React frontend access" --project=beca-0001
echo.

echo [2/2] Creating firewall rule for BECA Backend API (port 8000)...
gcloud compute firewall-rules create allow-beca-backend --allow=tcp:8000 --source-ranges=0.0.0.0/0 --description="Allow BECA FastAPI backend access" --project=beca-0001
echo.

echo ==========================================
echo Firewall rules created successfully!
echo ==========================================
echo.
echo Frontend (React): Port 3000
echo Backend (FastAPI): Port 8000
echo.
pause
