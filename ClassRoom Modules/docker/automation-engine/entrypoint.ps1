#!/usr/bin/env pwsh
# PowerShell Automation Engine Entry Point

Write-Host "Starting EduOps Automation Engine..." -ForegroundColor Green

# Import modules
$modulePath = "/automation/modules"
$env:PSModulePath = "$modulePath`:$env:PSModulePath"

Write-Host "Module path configured: $modulePath"

# Keep container running and listen for jobs
while ($true) {
    Start-Sleep -Seconds 10
}
