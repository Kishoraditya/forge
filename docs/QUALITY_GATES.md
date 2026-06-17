# Quality Gates

Run the smallest gate that matches the change. Broaden the gate when touching
shared behavior, cross-module contracts, or user-facing flows.

## Docs-Only Changes

- Read changed docs for stale instructions and contradictions.
- Run markdown/lint tooling if configured.
- No test run required unless docs include generated examples.

## Python Backend Changes

```bash
make test-unit
make lint
```

For API, database, or integration behavior:

```bash
make test-integration
```

Before merge:

```bash
make test
make lint
```

## Frontend Changes

Run the package scripts introduced by HT-005/frontend setup. Expected gates once
available:

```bash
npm run lint
npm run test
npm run build
```

For UI behavior, add Playwright or manual browser verification as required by
the feature spec.

## Infra Changes

- Validate Docker Compose syntax for changed compose files.
- Run `make ci-contract` or `make ci-check` before opening a PR (mirrors GitHub Actions).
- Validate Terraform formatting/plan for changed Terraform files.
- Do not apply production infrastructure from an agent task.

Expected commands once configured:

```bash
docker compose -f infra/docker/docker-compose.dev.yml config
terraform -chdir=infra/terraform fmt -check
terraform -chdir=infra/terraform validate
```

## Live Integration Tests

Live tests may use real Supabase or LLM credentials only when the task
explicitly requires it. Redact all secret values from logs and summaries.
