# Backend setup and launch helper for Windows PowerShell
# Usage: Run from the repo root or backend folder

$ErrorActionPreference = 'Stop'

# Move to backend folder if not already there
if (!(Test-Path "app/main.py")) {
    Set-Location "$PSScriptRoot"
    if (!(Test-Path "app/main.py")) {
        Set-Location "tax-software/backend"
    }
}

# Create venv if missing
if (!(Test-Path ".venv/Scripts/Activate.ps1")) {
    Write-Host "Creating Python venv..."
    python -m venv .venv
}

# Activate venv
Write-Host "Activating venv..."
. .venv/Scripts/Activate.ps1

# Install backend requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing backend requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Ensure dev tools
pip install --upgrade uvicorn fastapi pytest

# Run DB migrations (Cloudflare D1 local)
if (Test-Path "..\..\..\wrangler.toml") {
    Write-Host "Applying DB migrations (wrangler)..."
    try {
        wrangler d1 migrations apply d1 --local
    } catch {
        Write-Host "Wrangler migration failed or not installed. Skipping."
    }
}

# Run tests
Write-Host "Running backend tests..."
python -m pytest || Write-Host "Tests failed."

# Launch FastAPI dev server
Write-Host "Launching FastAPI dev server..."
python -m uvicorn app.main:app --reload
