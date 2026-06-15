# Security Rules

Forge is BYOK and handles user-supplied provider credentials. Treat secrets,
telemetry, and execution outputs as sensitive by default.

## Secret Handling

- Never commit `.env.local`, provider keys, service-role keys, tokens, cookies,
  downloaded credential files, or private certificates.
- Never print secrets in final answers, logs, telemetry, reports, screenshots,
  or test summaries.
- Secrets must come from environment variables or approved secret stores.
- Provider credentials must not be stored in plaintext.
- Supabase service-role keys are server-only and must never be exposed to the
  frontend.

## Logging And Telemetry

- Redact known secret fields before logging.
- Do not log request bodies that may contain API keys, user documents, or
  provider payloads unless explicitly sanitized.
- Telemetry spans may include IDs, status, durations, model aliases, and costs,
  but not raw credentials or sensitive prompt content by default.

## Database Access

- All database access originates in `backend/app/db/`.
- Services call db modules.
- API routes call services.
- Core/LangGraph code calls services, not db clients directly.
- RLS policy changes require human review.

## Sandboxed Execution

- User or LLM-generated code must run only in the approved sandbox layer.
- Local subprocess execution must have explicit timeout and resource limits.
- e2b credentials are optional until the cloud sandbox task is scheduled.

## Dependency Security

New dependencies require:
- Justification
- Alternatives considered
- License/security review
- Size/runtime impact
- Package file update
- Relevant quality gates

## Incident Rule

If a secret is exposed, stop feature work and rotate the secret before
continuing. Record the incident in `tasks/BLOCKED.md` without including the
secret value.
