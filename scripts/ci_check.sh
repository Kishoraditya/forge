#!/usr/bin/env bash
# =============================================================================
# Forge — Local CI parity check (mirrors .github/workflows/ci.yml)
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> CI contract tests"
poetry run pytest backend/tests/ci/ -v

echo "==> Backend unit tests"
poetry run pytest backend/tests/unit/ -v

echo "==> Backend lint"
cd backend && poetry run ruff check . && poetry run mypy app/
cd "$ROOT"

echo "==> Frontend npm ci"
cd frontend && npm ci

echo "==> Frontend lint"
npm run lint

echo "==> Frontend build"
npm run build

echo "==> All CI checks passed"
