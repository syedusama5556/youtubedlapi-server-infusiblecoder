param(
    [string]$Version,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

if (-not $Version) {
    $current = (Select-String -Path "$root\youtubedlapi_server_infusiblecoder\version.py" -Pattern "__version__ = '(.+)'").Matches.Groups[1].Value
    $Version = Read-Host "Current version $current. Enter new version"
}

Write-Host "Releasing v$Version" -ForegroundColor Cyan

# Update version files
Set-Content -Path "$root\youtubedlapi_server_infusiblecoder\version.py" -Value "__version__ = '$Version'"
$toml = Get-Content "$root\pyproject.toml" -Raw
$toml = $toml -replace 'version = "[\d.]+"', "version = `"$Version`""
Set-Content -Path "$root\pyproject.toml" -Value $toml
Write-Host "  Version files updated" -ForegroundColor Green

if ($DryRun) {
    Write-Host "DRY RUN: stopping before build" -ForegroundColor Yellow
    exit 0
}

# Load .env if present
$envFile = "$root\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.+)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Install deps
pip install build twine -q

# Clean old builds
Remove-Item "$root\dist" -Recurse -Force -ErrorAction SilentlyContinue

# Build
Write-Host "Building..." -ForegroundColor Cyan
python -m build "$root"
Write-Host "  Build OK" -ForegroundColor Green

# Upload
Write-Host "Uploading to PyPI..." -ForegroundColor Cyan
twine upload "$root\dist\*"
Write-Host "  Upload OK" -ForegroundColor Green

Write-Host "Done. v$Version published." -ForegroundColor Cyan
