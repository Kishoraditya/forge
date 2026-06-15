#!/usr/bin/env bash
# =============================================================================
# forge / scripts / bootstrap.sh
# =============================================================================
# Description : One-command local development setup
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : claude-code + KSR (reviewed by)
# Created     : 2026-06-12
# Modified    : 2026-06-12
# Version     : 0.1.0
# =============================================================================

set -euo pipefail

echo "========================================"
echo "  FORGE — Bootstrap Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $1 found: $(command -v "$1")"
        return 0
    else
        echo -e "  ${RED}✗${NC} $1 not found"
        return 1
    fi
}

echo "[1/7] Checking prerequisites..."
FAILED=0
check_command python3 || FAILED=1
check_command pip || FAILED=1
check_command node || FAILED=1
check_command npm || FAILED=1
check_command docker || FAILED=1
check_command git || FAILED=1

if [ $FAILED -eq 1 ]; then
    echo ""
    echo -e "${RED}ERROR: Missing prerequisites. Install the missing tools above and re-run.${NC}"
    exit 1
fi
echo ""

echo "[2/7] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
    echo -e "  ${GREEN}✓${NC} Python $PYTHON_VERSION (>= 3.11 required)"
else
    echo -e "  ${RED}✗${NC} Python $PYTHON_VERSION found, but >= 3.11 required"
    exit 1
fi
echo ""

echo "[3/7] Installing Poetry..."
if command -v poetry &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Poetry already installed"
else
    pip install poetry
    echo -e "  ${GREEN}✓${NC} Poetry installed"
fi
echo ""

echo "[4/7] Installing Python dependencies..."
poetry install
echo -e "  ${GREEN}✓${NC} Python dependencies installed"
echo ""

echo "[5/7] Installing pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo -e "  ${GREEN}✓${NC} Pre-commit hooks installed"
else
    poetry run pre-commit install
    echo -e "  ${GREEN}✓${NC} Pre-commit hooks installed (via poetry)"
fi
echo ""

echo "[6/7] Checking for .env.local..."
if [ -f ".env.local" ]; then
    echo -e "  ${GREEN}✓${NC} .env.local exists"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        echo -e "  ${YELLOW}!${NC} .env.local created from .env.example — fill in your values!"
    else
        echo -e "  ${YELLOW}!${NC} No .env.example found. Create .env.local manually (see docs/ENVIRONMENT.md)"
    fi
fi
echo ""

echo "[7/7] Verifying project structure..."
DIRS=("backend/app" "frontend" "infra" "scripts" "specs" "tasks" "docs" "reports")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir/"
    else
        echo -e "  ${RED}✗${NC} $dir/ missing"
    fi
done
echo ""

echo "========================================"
echo -e "  ${GREEN}Bootstrap complete!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Fill in .env.local with your API keys (see docs/ENVIRONMENT.md)"
echo "  2. Set up external services (see tasks/HUMAN_TASKS.md)"
echo "  3. Run 'make dev' to start local services"
echo "  4. Run 'make test' to verify everything works"
echo ""
