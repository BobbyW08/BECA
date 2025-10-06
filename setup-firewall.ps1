# Script to set up firewall for BECA Ollama VM

$env:PATH = "$env:PATH;C:\dev\google-cloud-sdk\bin"

Write-Host "Getting your public IP..." -ForegroundColor Cyan
$MY_IP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
Write-Host "Your IP: $MY_IP" -ForegroundColor Yellow

Write-Host ""
Write-Host "Creating firewall rule..." -ForegroundColor Cyan

gcloud compute firewall-rules create allow-ollama-from-home `
  --project=beca-0001 `
  --direction=INGRESS `
  --priority=1000 `
  --network=default `
  --action=ALLOW `
  --rules=tcp:11434 `
  --source-ranges="$MY_IP/32" `
  --target-tags=ollama-server `
  --description="Allow Ollama API access from home IP"

Write-Host ""
Write-Host "Firewall rule created! Ollama port 11434 is now accessible from your IP." -ForegroundColor Green
