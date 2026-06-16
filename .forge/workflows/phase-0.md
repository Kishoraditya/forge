# Phase 0 Workflow

## Order

1. Human completes HT-001–HT-008
2. Agent drafts specs F001–F008 → human reviews each
3. Agent populates BACKLOG → human reviews dependencies
4. Implement in dependency order:

```text
F001 (scaffold) → F008 (schema) → F006 (admin auth base)
  → F002 (BYOK) → F003 (LLM) → F004 (sessions)
  → F005 (chat UI) + F007 (RAG, parallel after F003)
```

5. Phase gate: `docs/PHASE_GATES.md` Phase 0 checklist

## Per-Task Loop

```text
turn start → read spec + task → branch sync → failing test → implement
→ quality gates → turn stop → human review → DONE.md
```

## Branches

One branch per feature: `feat/F001-scaffolding`, `feat/F008-supabase-schema`, etc.
Merge to `main` only after human review and quality gates.
