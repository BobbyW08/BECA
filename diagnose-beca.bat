@echo off
echo.
echo ==========================================
echo BECA Diagnostics
echo ==========================================
echo.
echo [1/4] Checking VM Status...
echo.
gcloud compute instances list --filter="name=beca-ollama" --format="table(name,status,EXTERNAL_IP,zone)"
echo.
echo.
echo [2/4] Getting External IP...
echo.
for /f "tokens=*" %%i in ('gcloud compute instances describe beca-ollama --zone=us-central1-b --format="value(networkInterfaces[0].accessConfigs[0].natIP)"') do set BECA_IP=%%i
echo Current External IP: %BECA_IP%
echo.
echo.
echo [3/4] Testing Connection...
echo.
ping -n 2 %BECA_IP%
echo.
echo.
echo [4/4] Checking if Docker containers are running...
echo (This requires SSH access to VM)
echo.
gcloud compute ssh beca-ollama --zone=us-central1-b --command="sudo docker ps"
echo.
echo.
echo ==========================================
echo Summary:
echo ==========================================
echo If VM STATUS = RUNNING, continue...
echo If EXTERNAL_IP changed, we need to update batch files
echo If ping fails, network issue
echo If docker ps shows no containers, containers didn't start
echo.
echo Try accessing: http://%BECA_IP%:7860
echo.
pause
