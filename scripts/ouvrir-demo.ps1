# Ouvre la démo MemBridge dans le navigateur
Start-Process "http://localhost:8765"
Start-Sleep -Seconds 1
Start-Process "http://localhost:8765/battle"
Write-Host ""
Write-Host "  DEMO OUVERTE dans le navigateur" -ForegroundColor Green
Write-Host "  Dashboard : http://localhost:8765" -ForegroundColor Cyan
Write-Host "  Battle    : http://localhost:8765/battle" -ForegroundColor Cyan
Write-Host "  GitHub    : https://github.com/LUC-cmd/Hackathon-IT-INTELO" -ForegroundColor Yellow
Write-Host ""
