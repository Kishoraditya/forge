# Agent State Contract

This is the conceptual state contract for LangGraph and agent workflows. Specs
may refine it, but should not silently contradict it.

## Core State Fields

```python
class AgentState:
    session_id: str
    conversation_id: str
    user_message: str
    messages: list[dict]
    active_skill_ids: list[str]
    active_personality_id: str | None
    model_alias: str
    budget_remaining_usd: float
    tool_calls: list[dict]
    tool_results: list[dict]
    memory_refs: list[str]
    graph_node_refs: list[str]
    decisions_made: list[dict]
    next_action: str
```

## Ownership

| Field Type | Owner |
|---|---|
| Session IDs and budgets | Session service + db layer |
| Messages | Message service + db layer |
| Tool calls/results | Tool service + core executor |
| Graph references | Graph service + graph layer |
| Decisions | Decision service + db/graph layers |
| Model alias | BYOK/model config service |

## Rules

- LangGraph nodes may read and update state, but persistent writes go through
  services.
- Services call `backend/app/db/` or `backend/app/graph/`.
- State must not contain raw provider API keys.
- State serialization must redact sensitive tool inputs and outputs when
  written to telemetry.
- Budget fields are authoritative only after validation by the budget/session
  service.

## Validation

Each feature that changes state must specify:
- New fields
- Field owner
- Persistence target
- Serialization behavior
- Redaction behavior
- Tests proving invalid state is rejected
