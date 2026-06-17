# =============================================================================
# forge / tests / ci / test_ci_contract
# =============================================================================
# Description : CI contract tests — repo files required for GitHub Actions parity.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_github_ci_workflow_exists() -> None:
    """GitHub Actions CI workflow must exist."""
    workflow = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert workflow.is_file(), "Missing .github/workflows/ci.yml"


def test_ci_workflow_runs_npm_ci() -> None:
    """Frontend job must use npm ci for reproducible installs."""
    content = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "npm ci" in content


def test_frontend_lockfile_contains_emnapi_pins() -> None:
    """Lock file must include @emnapi 1.11.1 entries (Linux npm ci requirement)."""
    lock_text = (REPO_ROOT / "frontend" / "package-lock.json").read_text(encoding="utf-8")
    assert "@emnapi/core/-/core-1.11.1.tgz" in lock_text
    assert "@emnapi/runtime/-/runtime-1.11.1.tgz" in lock_text


def test_frontend_package_json_emnapi_overrides() -> None:
    """package.json pins @emnapi versions for cross-platform lock consistency."""
    pkg = json.loads((REPO_ROOT / "frontend" / "package.json").read_text(encoding="utf-8"))
    overrides = pkg.get("overrides", {})
    assert overrides.get("@emnapi/core") == "1.11.1"
    assert overrides.get("@emnapi/runtime") == "1.11.1"
    dev_deps = pkg.get("devDependencies", {})
    assert dev_deps.get("@emnapi/core") == "1.11.1"
    assert dev_deps.get("@emnapi/runtime") == "1.11.1"
