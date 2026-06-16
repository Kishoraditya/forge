# Decision Log

Record of project decisions: who decided, what was chosen, and why. Solo operator:
**Kishoraditya (human)**. LLM assistants propose; human approves unless noted.

| Date | ID | Topic | Decision | Decided by | LLM role | Alternatives | Status | Reference |
|------|-----|-------|----------|------------|----------|--------------|--------|-----------|
| 2026-06-12 | D-001 | Agent orchestration | LangGraph over AutoGen | Human (Kishoraditya) | Proposed options | AutoGen, LangChain agents | Accepted | ADR-001 |
| 2026-06-12 | D-002 | Conversation storage | Option B full graph (Neo4j + Supabase) | Human (Kishoraditya) | Drafted ADR | Flat messages, JSON blob graph | Accepted | ADR-002 |
| 2026-06-12 | D-003 | LLM access | All inference via LiteLLM | Human (Kishoraditya) | Proposed ADR | Native provider SDKs | Accepted | ADR-003 |
| 2026-06-17 | D-004 | Python runtime | `poetry env use python3.12` (not 3.14 default) | Human (Kishoraditya) | Flagged dependency conflict | 3.13, 3.11 | Accepted | KNOWN_ISSUES, ENVIRONMENT.md |
| 2026-06-17 | D-005 | Git workflow | No direct commits to `main`; one commit per completed turn on feature branch | Human (Kishoraditya) | Implemented in docs | Direct-to-main | Accepted | GIT_WORKFLOW.md |
| 2026-06-17 | D-006 | Phase 0 specs | Eight specs F001–F008 approved for implementation | Human (Kishoraditya) | Drafted all specs | One-at-a-time review only | Accepted | specs/phase-0/ |
| 2026-06-17 | D-007 | Implementation start | Begin F001 on `feat/F001-scaffolding` with P0-F001-001 | Human (Kishoraditya) | Executing | — | In progress | BACKLOG.md |

## How to Add a Row

1. Assign next `D-NNN` ID.
2. Set **Decided by**: `Human (Kishoraditya)` | `LLM (cursor)` | `Joint`.
3. Set **LLM role**: `Drafted`, `Implemented`, `Reviewed`, `N/A`.
4. Link ADR, spec, or PR in **Reference**.
5. Update **Status**: Proposed → Accepted | Superseded | Rejected.

## LLM vs Human (current team)

| Actor | Responsibility |
|-------|----------------|
| Kishoraditya | Architecture approval, spec sign-off, merge approval, secrets, manual QA |
| Cursor / agents | Spec drafts, task breakdown, implementation, tests, turn files |
| LiteLLM providers | Inference only — not project decision-makers |
