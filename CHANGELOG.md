# Changelog

All notable changes to the Forge project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.0] — 2026-06-12

### Added
- Project scaffold: folder structure, governance documents, templates
- CLAUDE.md — AI agent cold-start context file
- AGENTS.md — Multi-agent context file
- docs/ARCHITECTURE.md — System design document
- docs/CONVENTIONS.md — Coding standards and conventions
- docs/CONTEXT.md — Living project state document
- docs/ENVIRONMENT.md — Environment setup and API key reference
- docs/SCOPE.md — Future scope beyond current phases
- docs/RITUALS.md — Development ceremonies
- Spec template (specs/_template.spec.md)
- Task format guide (tasks/_format.md)
- Task board files (BACKLOG, IN_PROGRESS, DONE, BLOCKED, PARKING_LOT, HUMAN_TASKS, THIS_WEEK)
- ADR template (docs/adr/ADR-000-template.md)
- Makefile with developer commands
- Helper scripts (bootstrap.sh, create_spec.sh, create_task.sh, context_refresh.sh)
- pyproject.toml with full dependency list
- Pre-commit configuration (.pre-commit-config.yaml)
- GitHub PR template
- .gitignore
- .cursorrules for Cursor IDE

### Notes
- No product code written yet — this is the governance and scaffolding layer only
- Phase 0 specs and tasks are the next step
- See tasks/HUMAN_TASKS.md for Day 0 manual setup items
