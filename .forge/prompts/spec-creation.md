# Prompt — Spec Creation

Read in order:
1. `docs/forge.md` (target feature section)
2. `docs/FEATURES.md` (feature ID registry)
3. `specs/_template.spec.md`
4. `docs/STATE.md`, `docs/SECURITY.md` if state/secrets involved

Create `specs/phase-X/FXXX-name.spec.md` only. Do not write implementation code.

Rules:
- Acceptance criteria must be binary (pass/fail).
- List every file to create or modify.
- Define exact Pydantic models and API shapes.
- State what the feature does NOT do.
- Reference `docs/VALIDATION.md` and `docs/LOGGING.md` where relevant.
- Show the spec for human review before finalizing.
