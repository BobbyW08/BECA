# 🔧 BECA Connection Issue - HTTPS/HTTP Problem

## The Problem

Your browser is trying to use HTTPS when BECA only runs on HTTP (without SSL certificates). This causes the "connection not secure" error.

## ✅ Quick Fix

### Method 1: Force HTTP in Browser (RECOMMENDED)

When the browser opens automatically, **manually type `http://` before the IP address** in the address bar:

**WRONG:** `https://[IP]:3000` or just `[IP]:3000`  
**CORRECT:** `http://[IP]:3000`

Example: `http://34.142.15.23:3000`

### Method 2: Clear Browser HSTS Cache

If your browser keeps forcing HTTPS, clear the HSTS (HTTP Strict Transport Security) cache:

**Chrome/Edge:**
1. Go to: `chrome://net-internals/#hsts` (or `edge://net-internals/#hsts`)
2. Scroll to "Delete domain security policies"
3. Enter your BECA IP address
4. Click "Delete"
5. Try accessing BECA again with `http://` prefix

**Firefox:**
1. Close Firefox
2. Find your Firefox profile folder:
   - Windows: `%APPDATA%\Mozilla\Firefox\Profiles\`
   - Look for the folder ending in `.default-release`
3. Delete the file `SiteSecurityServiceState.txt`
4. Restart Firefox

### Method 3: Use Incognito/Private Mode

Open an incognito/private window and access `http://[EXTERNAL-IP]:3000`

This bypasses any cached security settings.

## 📋 Updated start-beca.bat Script

Here's an improved version that explicitly uses HTTP:

```batch
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
echo IMPORTANT: Make sure the URL uses HTTP (not HTTPS)
echo.
start http://%BECA_IP%:3000
echo.
echo If browser shows "Not Secure" warning, that's normal for HTTP.
echo Click "Advanced" and "Proceed" if needed.
echo.
echo Access URLs:
echo   Frontend:  http://%BECA_IP%:3000
echo   Backend:   http://%BECA_IP%:8000/docs
echo   Portainer: http://%BECA_IP%:9000
echo   MCP:       http://%BECA_IP%:8080
echo.
echo ==========================================
echo Press any key to close this window...
pause >nul
```

## 🔐 Why No HTTPS?

BECA runs without SSL certificates by default because:
1. It's a development environment
2. You access it via IP address (not domain name)
3. It runs on your private Google Cloud VM
4. SSL certificates require a domain name

## ⚡ Optional: Enable HTTPS (Advanced)

If you want HTTPS, you need to:
1. Get a domain name (e.g., from Google Domains, Namecheap)
2. Point it to your VM's external IP
3. Install Let's Encrypt SSL certificate
4. Enable the nginx-proxy container in production mode

This is optional and not required for normal use.

## 🎯 Summary

**The Fix:** Always use `http://` (not `https://`) when accessing BECA.

Your browser may show a "Not Secure" warning - this is normal for HTTP connections. Simply proceed to the site.

---

**All working?** You should now see the BECA React interface at `http://[YOUR-IP]:3000`! 🎉
