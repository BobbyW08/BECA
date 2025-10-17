@echo off
echo.
echo ==========================================
echo Stopping BECA VM to Save Costs...
echo ==========================================
echo.
gcloud compute instances stop beca-ollama --zone=us-central1-b
echo.
echo ==========================================
echo Verifying VM Status...
echo ==========================================
echo.
gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(status)"
echo.
echo ==========================================
echo BECA VM Status Check:
echo ==========================================
gcloud compute instances list --filter="name=beca-ollama" --format="table(name,status,zone)"
echo.
echo ==========================================
echo If status shows TERMINATED, BECA is stopped!
echo Costs reduced to ~$0.07/day (disk only)
echo ==========================================
echo.
pause
