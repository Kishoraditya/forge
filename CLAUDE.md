# FORGE - Claude Code Context

`AGENTS.md` is the canonical source of truth for all AI coding assistants.

Claude Code must read `AGENTS.md` first, then follow the context loading order,
turn-file convention, task rules, architecture rules, and safety rules defined
there.

Do not duplicate project rules in this file. This file exists only as a Claude
Code entrypoint to prevent drift between assistant-specific instruction files.
