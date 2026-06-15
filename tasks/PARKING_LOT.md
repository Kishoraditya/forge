# Parking Lot

Ideas, observations, and potential tasks that emerged during development but are not yet scheduled. Review weekly during sanity check.

---

<!-- Add items as they come up during development -->

---

### Context Engineering Improvements To Consider

- Add a compact `docs/DECISIONS.md` or ADR index so agents can load one short decision map before reading individual ADRs.
- Add `docs/CONTEXT_MAP.md` that tells agents which files to read for each task type: backend, frontend, infra, specs, tests, docs.
- Add a `docs/GLOSSARY.md` for project-specific terms like BYOK, Option B graph, skill, personality, decision, tool call, and session.
- Add a `docs/PROMPT_LIBRARY.md` or formalize `docs/prompts_used.md` so reusable agent prompts are versioned and discoverable.
- Add a short `docs/QUALITY_GATES.md` listing exact commands required before review for Python, frontend, docs-only, and infra-only changes.
- Revisit whether all dependencies in `pyproject.toml` should be installed at scaffold time or introduced feature-by-feature to reduce setup friction.
- Add frontend package management files after HT-005 so Node tooling has the same level of governance as Python tooling.
- Add CI workflow files once Git is initialized and first tests exist; `.github/workflows/.gitkeep` is currently only a placeholder.
