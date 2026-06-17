# Known Issues

Bugs, edge cases, and quirks discovered during development. Review regularly.

| Date | Description | Severity | Affected Feature | Workaround | Status |
|------|-------------|----------|-----------------|------------|--------|
| 2026-06-17 | `poetry.lock` gitignored — installs may drift across machines | Medium | F001 | Commit lock file or pin versions in docs | Open |
| 2026-06-17 | Host Python 3.14 default; project uses Poetry 3.12 | Low | F001 | `poetry env use python3.12` | Resolved |
| 2026-06-17 | Frontend on Next.js 16; docs reference Next.js 14 | Low | F001/F005 | Document in F001 spec notes | Open |

<!-- Add entries as issues are discovered during development -->
