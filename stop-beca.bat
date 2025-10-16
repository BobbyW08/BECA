@echo off
echo.
echo ==========================================
echo Stopping BECA VM to Save Costs...
echo ==========================================
echo.
gcloud compute instances stop beca-ollama --zone=us-central1-b
echo.
echo ==========================================
echo VM Stopped Successfully!
echo Costs reduced to ~$0.07/day (disk only)
echo ==========================================
echo.
pause
