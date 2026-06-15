# FORGE — Coding Conventions & Standards
<!-- Conventions version: 1.0.0 | Author: claude-code + KSR | Date: 2026-06-12 -->

All code written by human developers or AI agents in the Forge project must adhere to these guidelines.

---

## 1. Developer Signature Header

Every new file created must start with a header containing file metadata.

### Python Files
```python
# =============================================================================
# forge / [module path]
# =============================================================================
# Description : [one sentence — what this file does]
# Layer       : [Infra | API | Core | Tools | Memory | Observability]
# Feature     : [FXXX — Feature Name]
# Author      : [human | claude-code | cursor | codex] + KSR (reviewed by)
# Created     : YYYY-MM-DD
# Modified    : YYYY-MM-DD
# Version     : 0.1.0
# =============================================================================
```

### TypeScript / TSX Files
```typescript
// =============================================================================
// forge / [module path]
// Description : [one sentence — what this file does]
// Layer       : [Infra | API | Core | Tools | Memory | Observability]
// Feature     : [FXXX — Feature Name]
// Author      : [human | claude-code | cursor | codex] + KSR (reviewed by)
// Created     : YYYY-MM-DD
// Modified    : YYYY-MM-DD
// Version     : 0.1.0
// =============================================================================
```

---

## 2. Docstring Standard (Python)

All functions, classes, and modules must have docstrings. For functions, use the Google-style docstring format including arguments, returns, exceptions raised, example, and specifications notes:

```python
def create_session(model_alias: str, credit_budget_usd: float) -> Session:
    """
    Create a new anonymous agent session with token budget tracking.

    Args:
        model_alias: LiteLLM model alias (e.g., 'smart', 'fast', 'cheap')
        credit_budget_usd: Maximum spend allowed for this session in USD

    Returns:
        Session: Newly created session with UUID, expiry, and credit ledger entry

    Raises:
        ValueError: If model_alias not found in LiteLLM config
        BudgetError: If credit_budget_usd is below minimum threshold

    Example:
        >>> session = create_session("fast", 0.10)
        >>> session.id
        'uuid-here'

    Notes:
        - Session is written to Supabase immediately on creation
        - Token counter starts at 0, hard stop enforced at 100% of budget
        - See: specs/phase-0/F004-session-management.spec.md
    """
```

---

## 3. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| **Python files** | `snake_case` | `session_service.py` |
| **Python classes** | `PascalCase` | `SessionService` |
| **Python functions** | `snake_case` | `create_session()` |
| **Python constants** | `UPPER_SNAKE` | `MAX_SESSION_TOKENS` |
| **TypeScript files** | `kebab-case` | `session-provider.tsx` |
| **React components** | `PascalCase` | `SessionBudgetBar` |
| **API routes** | `kebab-case` | `/api/session-create` |
| **Env vars** | `UPPER_SNAKE` | `SUPABASE_SERVICE_ROLE_KEY` |
| **Database tables** | `snake_case` | `session_messages` |
| **Graph nodes** | `PascalCase` | `:Message`, `:ToolCall` |
| **Feature branches** | `feat/FXXX-short-name` | `feat/F009-langgraph-graph` |
| **Fix branches** | `fix/FXXX-short-desc` | `fix/F004-redis-leak` |

---

## 4. Structural Rules

- **Maximum file length**: 300 lines. If a file grows beyond 300 lines, extract logic into submodules.
- **Maximum function length**: 50 lines. If a function is longer than 50 lines, extract sub-helpers.
- **No business logic in API route handlers**: API routes in `backend/app/api/` must remain extremely thin, handling only input validation/parsing and dispatching to services.
- **No direct database calls outside `db/`**: Supabase/ORM queries must originate in `backend/app/db/`. Services call db modules. API routes call services. LangGraph/core code calls services and never queries tables directly.
- **No hardcoded strings**: Use config templates, schemas, or constant definitions.
- **Strict import structures**: All imports must be absolute. No relative imports are allowed.
- **Clean __init__.py files**: Do not add business or mapping logic inside `__init__.py` files. Keep them for clean namespace exports.

---

## 5. Commit Message Format

We use Conventional Commits. Commits must reference the Feature ID (e.g. F001) in parentheses:

```
<type>(FXXX): <description>
```

Types permitted:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Formatting changes (missing semi-colons, spaces, linting)
- `refactor`: Code restructuring without functional behavior modifications
- `test`: Adding or correcting tests
- `chore`: Configuration, package updates, dev tools maintenance

**Example**:
```
feat(F009): add conversation node state serialization to neo4j
```

---

## 6. Import Ordering Rules

Format using `isort`. Imports must be sorted alphabetically and grouped:

1. Standard library imports
2. Third-party library imports
3. Local application imports

---

## 7. Error Handling Patterns

- Always catch specific exceptions (never use bare `except:` or `except Exception:` unless logging and re-raising).
- Map internal exceptions (e.g. DB lookup failure) to custom exceptions defined in `app/core/exceptions.py`.
- Custom exceptions should map to HTTP exception layers gracefully inside `api` controllers using standard middleware or handlers.

---

## 8. Testing Conventions

- **Write tests alongside implementation**: Do not write tests afterward.
- **Unit tests**: Situating in `backend/tests/unit/`, mirroring the `app` folder structure. (e.g. `tests/unit/test_session_service.py` checks `app/services/session_service.py`).
- **Integration tests**: Situating in `backend/tests/integration/` (e.g. endpoint validations with mock dependencies).
- **Assertions**: Avoid generic asserts. Use descriptive pytest assertions.
