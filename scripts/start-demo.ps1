# MemBridge - lancement one-click (Windows)
Set-Location $PSScriptRoot\..

if (-not (Test-Path .venv)) {
    Write-Host "Creation environnement Python 3.12..."
    py -3.12 -m venv .venv
}

.\.venv\Scripts\Activate.ps1
pip install -q -e ".[dev,demo]"

Write-Host ""
Write-Host "  MemBridge - demarrage" -ForegroundColor DarkRed
Write-Host "  Dashboard : http://localhost:8765" -ForegroundColor DarkGreen
Write-Host "  Battle    : http://localhost:8765/battle" -ForegroundColor DarkGreen
Write-Host "  Terminal  : python -m demo.live_battle" -ForegroundColor DarkYellow
Write-Host ""

$env:PYTHONPATH = "src;."
python -m benchmark.harness | Out-Null
python -m demo.web_server
