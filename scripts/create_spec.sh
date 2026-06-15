#!/usr/bin/env bash
# =============================================================================
# forge / scripts / create_spec.sh
# =============================================================================
# Description : Scaffold a new spec file from the template
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : claude-code + KSR (reviewed by)
# Created     : 2026-06-12
# Modified    : 2026-06-12
# Version     : 0.1.0
# =============================================================================

set -euo pipefail

# Usage: bash scripts/create_spec.sh F001
# Creates: specs/phase-0/F001-name.spec.md

FEATURE_ID="${1:?Usage: create_spec.sh <FEATURE_ID> (e.g., F001)}"

# Determine phase from feature number
FEATURE_NUM=${FEATURE_ID#F}
FEATURE_NUM=${FEATURE_NUM#0}
FEATURE_NUM=${FEATURE_NUM#0}

if [ "$FEATURE_NUM" -le 8 ]; then
    PHASE="phase-0"
elif [ "$FEATURE_NUM" -le 20 ]; then
    PHASE="phase-1"
elif [ "$FEATURE_NUM" -le 30 ]; then
    PHASE="phase-2"
elif [ "$FEATURE_NUM" -le 39 ]; then
    PHASE="phase-3"
elif [ "$FEATURE_NUM" -le 45 ]; then
    PHASE="phase-4"
elif [ "$FEATURE_NUM" -le 50 ]; then
    PHASE="phase-5"
else
    echo "ERROR: Feature number $FEATURE_NUM out of range (1-50)"
    exit 1
fi

# Prompt for feature name
read -rp "Feature name (kebab-case, e.g., session-management): " FEATURE_NAME

if [ -z "$FEATURE_NAME" ]; then
    echo "ERROR: Feature name cannot be empty"
    exit 1
fi

SPEC_DIR="specs/${PHASE}"
SPEC_FILE="${SPEC_DIR}/${FEATURE_ID}-${FEATURE_NAME}.spec.md"

# Check if already exists
if [ -f "$SPEC_FILE" ]; then
    echo "ERROR: Spec file already exists: $SPEC_FILE"
    exit 1
fi

# Create from template
mkdir -p "$SPEC_DIR"
DATE=$(date +%Y-%m-%d)

cat > "$SPEC_FILE" << EOF
# [${FEATURE_ID}] — ${FEATURE_NAME}
<!-- Spec version: 1.0.0 | Author: [human/agent] | Date: ${DATE} -->

## Feature Reference
- **Feature ID**: ${FEATURE_ID}
- **Phase**: ${PHASE/phase-/Phase }
- **Depends on**: [list feature IDs or "none"]
- **Blocks**: [list feature IDs or "none"]
- **Estimated tasks**: N

## What This Does (One Paragraph)
[Plain English description. No jargon. What does a user experience?]

## What This Does NOT Do
[Explicit scope boundaries. Prevents scope creep during implementation.]

## Acceptance Criteria
- [ ] AC1: [specific, testable, binary]
- [ ] AC2: ...
- [ ] AC3: ...

## Data Model
[Pydantic schema or table definition for any new data structures]

## API Contract (if applicable)
[Endpoint, method, request body, response body — exact shapes]

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| backend/app/services/xxx.py | New | ... |
| backend/tests/unit/test_xxx.py | New | ... |

## Files to Modify
| File | Change |
|------|--------|
| backend/app/main.py | Register new router |

## Test Cases
### Happy Path
- Input: ... → Expected output: ...

### Edge Cases
- Empty input → Expected: validation error, no side effects
- Budget exceeded → Expected: graceful stop, log entry

### Should Not Happen
- [What explicitly must NOT be possible after this feature]

## Manual Test Flow
[1-5 step human-executable test. Added to MANUAL_TESTING.md when done.]

## Notes & Assumptions
[Anything uncertain, any tradeoffs made in this spec]
EOF

echo "✓ Created spec: $SPEC_FILE"
echo "  Next: Fill in all sections, then run 'bash scripts/create_task.sh' to break into tasks."
