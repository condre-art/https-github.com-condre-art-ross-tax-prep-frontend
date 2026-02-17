# Frontend setup and launch helper for Windows PowerShell
# Usage: Run from the repo root or frontend folder

$ErrorActionPreference = 'Stop'

# Move to frontend folder if not already there
if (!(Test-Path "src/App.tsx")) {
    Set-Location "$PSScriptRoot"
    if (!(Test-Path "src/App.tsx")) {
        Set-Location "tax-software/frontend"
    }
}

# Install dependencies
Write-Host "Installing frontend dependencies..."
npm install

# Run tests
Write-Host "Running frontend tests..."
npm test || Write-Host "Frontend tests failed."

# Start dev server
Write-Host "Starting frontend dev server..."
npm run dev
