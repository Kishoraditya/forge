#!/usr/bin/env bash
# =============================================================================
# forge / scripts / context_refresh.sh
# =============================================================================
# Description : Reminder and helper to update CONTEXT.md
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : claude-code + KSR (reviewed by)
# Created     : 2026-06-12
# Modified    : 2026-06-12
# Version     : 0.1.0
# =============================================================================

set -euo pipefail

echo "========================================"
echo "  FORGE — Context Refresh Reminder"
echo "========================================"
echo ""

# Show current context
if [ -f "docs/CONTEXT.md" ]; then
    echo "--- Current CONTEXT.md ---"
    cat docs/CONTEXT.md
    echo ""
    echo "--- End of CONTEXT.md ---"
else
    echo "WARNING: docs/CONTEXT.md does not exist!"
fi

echo ""
echo "Questions to answer when updating:"
echo "  1. What phase are you in?"
echo "  2. What was just completed?"
echo "  3. What is currently in progress?"
echo "  4. What is blocked and why?"
echo "  5. Any key decisions made?"
echo "  6. What are the next 3 tasks?"
echo ""

# Show recent git history for context
echo "--- Recent Git History ---"
if git log --oneline -10 2>/dev/null; then
    echo ""
else
    echo "  (no git history yet)"
fi

# Show current task status
echo ""
echo "--- Tasks In Progress ---"
if [ -f "tasks/IN_PROGRESS.md" ]; then
    cat tasks/IN_PROGRESS.md
else
    echo "  (no IN_PROGRESS.md found)"
fi

echo ""
echo "--- Blocked Tasks ---"
if [ -f "tasks/BLOCKED.md" ]; then
    cat tasks/BLOCKED.md
else
    echo "  (no BLOCKED.md found)"
fi

echo ""
echo "Now update docs/CONTEXT.md! Keep it under 500 tokens."
