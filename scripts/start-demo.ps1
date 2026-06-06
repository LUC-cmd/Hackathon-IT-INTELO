# MemBridge — lancement one-click (Windows)
Set-Location $PSScriptRoot\..

if (-not (Test-Path .venv)) {
    Write-Host "Création environnement Python 3.12..."
    py -3.12 -m venv .venv
}

.\.venv\Scripts\Activate.ps1
pip install -q -e ".[dev,demo]"

Write-Host ""
Write-Host "  MemBridge — démarrage" -ForegroundColor DarkRed
Write-Host "  Dashboard : http://localhost:8765" -ForegroundColor DarkGreen
Write-Host ""

$env:PYTHONPATH = "src;."
python -m benchmark.harness | Out-Null
python -m demo.web_server
