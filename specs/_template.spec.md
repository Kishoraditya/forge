# [FXXX] — [Feature Name]
<!-- Spec version: 1.0.0 | Author: [human/agent] | Date: YYYY-MM-DD -->

## Feature Reference
- **Feature ID**: FXXX
- **Phase**: Phase X
- **Depends on**: [list feature IDs or "none"]
- **Blocks**: [list feature IDs or "none"]
- **Feature registry entry**: docs/FEATURES.md
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

## Agent State Impact
[New/changed state fields, owner, persistence target, serialization behavior, redaction behavior. Use docs/STATE.md.]

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

## Security & Secrets
[Secrets touched, redaction requirements, RLS/auth impact, telemetry sensitivity. Use docs/SECURITY.md.]

## Dependencies
[New dependencies required, alternatives considered, security/license/size notes, or "none".]

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

## Phase/Feature Exit Signal
[What world signal or quality gate proves this feature is complete? Use docs/WORLD_SIGNALS.md and docs/QUALITY_GATES.md.]

## Notes & Assumptions
[Anything uncertain, any tradeoffs made in this spec]
