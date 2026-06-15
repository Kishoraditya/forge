# [FXXX] — [Feature Name]
<!-- Spec version: 1.0.0 | Author: [human/agent] | Date: YYYY-MM-DD -->

## Feature Reference
- **Feature ID**: FXXX
- **Phase**: Phase X
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
