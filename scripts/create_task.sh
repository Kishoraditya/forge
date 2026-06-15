#!/usr/bin/env bash
# =============================================================================
# forge / scripts / create_task.sh
# =============================================================================
# Description : Scaffold a new task entry and append to BACKLOG.md
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : claude-code + KSR (reviewed by)
# Created     : 2026-06-12
# Modified    : 2026-06-12
# Version     : 0.1.0
# =============================================================================

set -euo pipefail

echo "=== Forge Task Creator ==="
echo ""

read -rp "Phase number (0-5): " PHASE
read -rp "Feature ID (e.g., F001): " FEATURE_ID
read -rp "Task sequence number (e.g., 001): " SEQ
read -rp "Short title: " TITLE
read -rp "Spec file path (e.g., specs/phase-0/F001-scaffolding.spec.md): " SPEC_PATH
read -rp "Assigned to (human / claude-code / cursor / codex): " ASSIGNED
read -rp "Size (S / M / L): " SIZE
read -rp "What to do (one sentence): " WHAT_TO_DO
read -rp "Depends on (task IDs, comma-separated, or 'none'): " DEPENDS

TASK_ID="P${PHASE}-${FEATURE_ID}-${SEQ}"

TASK_ENTRY="
---
### ${TASK_ID} — ${TITLE}

**Spec**: ${SPEC_PATH}
**Assigned to**: ${ASSIGNED}
**Status**: backlog
**Estimated**: ${SIZE}
**Actual**: [fill when done]
**Depends on**: ${DEPENDS}

**What to do (one sentence)**:
${WHAT_TO_DO}

**Acceptance checklist**:
- [ ] File created at correct path
- [ ] Function signature matches spec
- [ ] Docstring present (see CONVENTIONS.md)
- [ ] Unit test written and passing
- [ ] No new imports added without updating pyproject.toml
- [ ] CONTEXT.md updated after completion
- [ ] TURN.md updated

**Context needed**:
- Read: ${SPEC_PATH}
- Read: docs/CONVENTIONS.md

**Do not**:
- [Add scope boundaries here]

**Definition of done**:
Relevant tests pass. Files at correct paths. Docstrings present.
"

echo "$TASK_ENTRY" >> tasks/BACKLOG.md

echo ""
echo "✓ Task ${TASK_ID} added to tasks/BACKLOG.md"
echo "  Next: Review the task in BACKLOG.md, then move to IN_PROGRESS.md when starting."
