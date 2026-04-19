# Org Repo Intake Runbook

## Purpose

Use this runbook when creating a new `NIBARGERB-HLDPRO` repository or adding an existing repository to org-level governance. The goal is to make every repo's status explicit across three layers:

- GitHub org and repo controls
- repo-local product governance files
- Overlord registry, sweep, graph, metrics, memory, Codex, and compendium coverage

Do not treat one layer as proof of another. A repo can have branch rules and still be absent from Overlord. A repo can be in `docs/governed_repos.json` and still lack repo-local required checks.

## Inputs

Collect these before writes:

- Repo name and GitHub owner, usually `NIBARGERB-HLDPRO/<repo>`.
- Whether this is a new repo or an existing repo.
- Default branch.
- Local checkout path under `$HLDPRO_REPOS_ROOT` or `~/Developer/HLDPRO`.
- Governance tier: `full`, `full-hipaa`, `standard`, `limited`, `adoption_blocked`, or `exempt`.
- Security tier: `baseline`, `full-pentagi`, `full-pentagi-hipaa`, or `exempt`.
- Intended subsystem flags: `graphify`, `sweep`, `metrics`, `memory_integrity`, `codex_ingestion`, `compendium`, `raw_feed_sync`, and `code_governance`.
- Issue number in `hldpro-governance` for intake planning and closeout.

## Stage 0 - Plan

Every intake needs an issue-backed planning surface before registry or downstream writes.

Required artifacts:

- `docs/plans/issue-<n>-<repo>-intake-pdcar.md`
- `docs/plans/issue-<n>-structured-agent-cycle-plan.json`
- `raw/execution-scopes/<date>-issue-<n>-<repo>-intake-<mode>.json`

The PDCAR must state whether the slice is:

- discovery only,
- repo creation plus local governance bootstrap,
- Overlord registry enrollment,
- generated graph/wiki refresh,
- closeout only.

If multiple people or agents are active in the repo, record the active roots in the execution scope and keep writes inside `allowed_write_paths`.

Validation:

```bash
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/<scope>.json --changed-files-file <changed-files>
git diff --check
```

## Stage 1 - Create Or Resolve The GitHub Repo

For a new repo:

```bash
gh repo create NIBARGERB-HLDPRO/<repo> --private --source /path/to/local/repo --remote origin --push
```

For an existing repo:

```bash
gh repo view NIBARGERB-HLDPRO/<repo> --json nameWithOwner,url,visibility,defaultBranchRef,viewerPermission
git -C /path/to/local/repo remote -v
```

Confirm:

```bash
gh repo view NIBARGERB-HLDPRO/<repo> --json nameWithOwner,owner,visibility,isPrivate,defaultBranchRef,viewerPermission,url
gh api user/memberships/orgs/NIBARGERB-HLDPRO --jq '{organization: .organization.login, role, state}'
```

## Stage 2 - Install Repo-Local Product Governance

Minimum product repo files:

```text
.github/CODEOWNERS
.github/dependabot.yml
.github/pull_request_template.md
.github/workflows/governance-check.yml
.github/workflows/gitleaks.yml
.gitleaks.toml
.hldpro/governance-tooling.json
docs/PROGRESS.md
docs/exception-register.md
```

The exact workflow commands must match the repo's stack. Do not copy a profile that cannot run in the target repo. If only Phase 0 artifacts exist, use deterministic artifact validation and secret scanning until the application stack exists.

Validate locally before push:

```bash
python3 -m json.tool .hldpro/governance-tooling.json >/dev/null
git diff --check
```

Add stack-specific validation, for example:

```bash
python3 -m json.tool label_schema_v0_1.json >/dev/null
python3 -m json.tool baselines_v0_1.json >/dev/null
python3 - <<'PY'
from pathlib import Path
import yaml

with Path("phase0.yaml").open("r", encoding="utf-8") as handle:
    yaml.safe_load(handle)
PY
```

## Stage 3 - Apply GitHub Rules And Security Guards

Confirm inherited org rulesets:

```bash
gh api /orgs/NIBARGERB-HLDPRO/rulesets --jq '.[] | [.id,.name,.enforcement] | @tsv'
```

Create a repo-level main policy only after the required check workflows exist on the default branch. Required status contexts must exactly match live check names.

Example repo ruleset shape:

```bash
gh api --method POST /repos/NIBARGERB-HLDPRO/<repo>/rulesets --input ruleset.json
```

The policy should normally include:

- deletion block
- non-fast-forward block
- pull request required
- one approving review
- code-owner review
- review-thread resolution
- strict required checks
- no bypass actors unless an issue-backed exception exists

Enable security settings:

```bash
gh api -X PUT /repos/NIBARGERB-HLDPRO/<repo>/vulnerability-alerts --silent
gh api -X PUT /repos/NIBARGERB-HLDPRO/<repo>/automated-security-fixes --silent
gh api -X PATCH /repos/NIBARGERB-HLDPRO/<repo> --input - <<'JSON'
{
  "security_and_analysis": {
    "secret_scanning": {"status": "enabled"},
    "secret_scanning_push_protection": {"status": "enabled"},
    "secret_scanning_non_provider_patterns": {"status": "enabled"},
    "secret_scanning_validity_checks": {"status": "enabled"},
    "dependabot_security_updates": {"status": "enabled"}
  }
}
JSON
```

Verify:

```bash
gh api /repos/NIBARGERB-HLDPRO/<repo>/rulesets --jq '.[] | [.id,.name,.source_type,.enforcement] | @tsv'
gh api /repos/NIBARGERB-HLDPRO/<repo>/vulnerability-alerts -i
gh api /repos/NIBARGERB-HLDPRO/<repo>/automated-security-fixes --jq '{enabled,paused}'
gh api /repos/NIBARGERB-HLDPRO/<repo> --jq '{web_commit_signoff_required,security_and_analysis}'
gh run list --repo NIBARGERB-HLDPRO/<repo> --branch main --limit 10
```

Classic branch protection may return `404 Branch not protected` when rulesets are the active protection mechanism. In that case, verify the rulesets directly instead of creating duplicate classic protection.

## Stage 4 - Enroll In Overlord

Repo-local GitHub governance is not Overlord enrollment. Add the repo to `docs/governed_repos.json` with all required fields:

- `repo_slug`
- `display_name`
- `repo_dir_name`
- `github_repo`
- `local_path`
- `ci_checkout_path`
- `graph_output_path`
- `wiki_path`
- `project_path`
- `governance_tier`
- `security_tier`
- `lifecycle_status`
- `governance_status`
- `classification`
- `description`
- `enabled_subsystems`

If `graphify` is enabled, add a matching row to `docs/graphify_targets.json`.

Validate:

```bash
python3 scripts/overlord/validate_governed_repos.py
python3 scripts/overlord/check_org_repo_inventory.py --live --format text
python3 scripts/knowledge_base/graphify_targets.py show --repo-slug <repo-slug>
python3 scripts/overlord/validate_governed_repos.py --print-subsystem sweep
python3 scripts/overlord/validate_governed_repos.py --print-subsystem code_governance
python3 scripts/overlord/validate_governed_repos.py --print-subsystem metrics
python3 scripts/overlord/validate_governed_repos.py --print-subsystem compendium
```

Regenerate compendium, graph, wiki, metrics, or raw-feed artifacts only when the implementation scope includes those paths.

## Stage 5 - PR And Closeout

Before opening a PR:

```bash
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/<scope>.json --changed-files-file <changed-files>
python3 scripts/overlord/validate_governed_repos.py
git diff --check
```

PR body must include:

- issue link,
- repo URL,
- created or existing repo status,
- ruleset IDs,
- security setting evidence,
- required check run IDs,
- registry subsystem selection,
- open risks and deferrals.

Closeout must not claim completion until:

- GitHub org/repo controls are active or explicitly deferred.
- Repo-local governance files are committed on the default branch or explicitly deferred.
- Overlord registry enrollment is complete or explicitly classified as `adoption_blocked`, `limited`, or `exempt`.
- Required checks pass on the PR and, after merge, on `main`.

## Solo-Owner Repos

GitHub blocks self-approval. If a solo-owner repo requires one approving review, normal merges will block even when checks pass.

Preferred options:

1. Add a second trusted reviewer with write access.
2. Keep the ruleset strict and use a documented temporary ruleset-disable override only when the operator explicitly authorizes it.
3. Create an issue-backed exception with expiry or review cadence before weakening review requirements.

When an override is used:

- back up the ruleset,
- disable only the minimum repo-level overlay,
- merge,
- immediately restore the ruleset,
- capture audit-log evidence,
- update `docs/exception-register.md` if the override is repeatable.
