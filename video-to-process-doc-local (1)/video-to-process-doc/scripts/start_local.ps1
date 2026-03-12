param()
$ErrorActionPreference = 'Stop'

# Paths
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Repo = Join-Path $Root '..'
$Backend = Join-Path $Repo 'backend'
$Frontend = Join-Path $Repo 'frontend'

# Python venv
python -m venv "$Backend/.venv"
& "$Backend/.venv/Scripts/Activate.ps1"
python -m pip install --upgrade pip
pip install -r "$Backend/requirements.txt"

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Backend'; $env:WORK_DIR='./data'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Frontend deps
Push-Location $Frontend
if (!(Test-Path 'node_modules')) { npm install --legacy-peer-deps }
$env:NEXT_PUBLIC_API_BASE = 'http://localhost:8000'

# Open browser
Start-Process "http://localhost:3000"

npm run dev
Pop-Location
