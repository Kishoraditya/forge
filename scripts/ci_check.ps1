# Forge — Local CI parity check (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "==> CI contract tests"
poetry run pytest backend/tests/ci/ -v

Write-Host "==> Backend unit tests"
poetry run pytest backend/tests/unit/ -v

Write-Host "==> Backend lint"
Push-Location backend
poetry run ruff check .
poetry run mypy app/
Pop-Location

Write-Host "==> Frontend npm ci"
Push-Location frontend
npm ci
npm run lint
npm run build
Pop-Location

Write-Host "==> All CI checks passed"
