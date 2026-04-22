# Session Error Patterns Runbook

This runbook is the operator lookup table for recurring session errors. It complements `docs/FAIL_FAST_LOG.md`, which remains the formal ledger, and `docs/ERROR_PATTERNS.md`, which remains the canonical machine-readable pattern catalog. Each entry is intentionally short so self-learning lookup can return the correction path before another retry repeats the same failure.

Use this schema for new entries:

| Field | Value |
|---|---|
| Signature | Exact log text, command symptom, or PR/check behavior. |
| Category | One of hook classifier, CLI supervisor, governance evidence, merge/check flow, schema drift, consumer verifier, or agent QA. |
| Root Cause | Why the session failed. |
| Correction | The concrete command, flag, file, path, or implementation fix. |
| Guardrail | Existing or new guardrail that should catch the issue before retry. |
| Validation | Deterministic check proving the correction. |
| Related Files | Primary repo paths or downstream package files. |
| First Observed | Date first recorded. |
| Prevented By | Issue, PR, or guardrail that prevents recurrence. |

## Pattern: hook-command-classification-false-positive

| Field | Value |
|---|---|
| Signature | `schema-guard: BLOCKED: Bash file write detected` with target fragments from quoted `awk` or `jq` comparisons such as `for = 0`, `0)po`, or `> 1`. |
| Category | hook classifier |
| Root Cause | Bash write detection treated quoted comparison operators as shell redirects or writes. |
| Correction | Route write-target detection through `scripts/overlord/check_plan_preflight.py` and add command fixture coverage before changing hook regexes. |
| Guardrail | `hooks/schema-guard.sh` consumes the shared classifier; `hooks/branch-switch-guard.sh` strips heredoc bodies before executable matching. |
| Validation | `python3 scripts/overlord/test_check_plan_preflight.py` and `python3 scripts/overlord/test_schema_guard_hook.py`. |
| Related Files | `scripts/overlord/check_plan_preflight.py`, `hooks/schema-guard.sh`, `hooks/branch-switch-guard.sh` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #538, pattern `hook-command-classification-drift` |

## Pattern: claude-stream-json-verbose-required

| Field | Value |
|---|---|
| Signature | `Claude requires --verbose with --output-format stream-json`. |
| Category | CLI supervisor |
| Root Cause | Worker launch used Claude stream JSON output without the required verbose flag, and one wrapper path did not expose that flag. |
| Correction | Include `--verbose` whenever `--output-format stream-json` is selected, or fall back to the default output mode when the wrapper cannot pass verbose. |
| Guardrail | Supervisor command-mode contract should validate Claude flag combinations before launch. |
| Validation | Fake Claude supervisor tests cover stream JSON with verbose and default-output fallback. |
| Related Files | `scripts/orchestrator/cli_session_supervisor.py`, `scripts/orchestrator/test_cli_session_supervisor.py` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #536 |

## Pattern: force-push-policy-advisory-only

| Field | Value |
|---|---|
| Signature | `git push --force-with-lease`, `git push -f`, `git push --force`, or `git push origin +branch` appears in session output without an explicit local block. |
| Category | hook classifier |
| Root Cause | Remote history mutation was a session policy but not locally enforced by branch/worktree guardrails. |
| Correction | Block force flags and `+` refspecs in `hooks/branch-switch-guard.sh`; use normal push after branch hygiene or create a replacement branch when history rewrite is not issue-approved. |
| Guardrail | Branch-switch guard force-push detector. |
| Validation | Hook fixture tests for force flag and plus-refspec variants. |
| Related Files | `hooks/branch-switch-guard.sh`, `scripts/overlord/test_branch_switch_guard.py` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #538 |

## Pattern: stale-governance-workflow-sha

| Field | Value |
|---|---|
| Signature | Consumer PR still pins an older governance workflow SHA after a governance package adoption update. |
| Category | consumer verifier |
| Root Cause | Worker updated part of the governance package but missed one workflow ref or managed package pin. |
| Correction | Run the non-mutating consumer verifier, update every managed workflow/package reference to the target SHA, and preserve override metadata for any intentional local difference. |
| Guardrail | Governance SSOT consumer verifier v0.2 drift detection. |
| Validation | Consumer verifier tests for workflow-ref mismatch and package SHA mismatch. |
| Related Files | `scripts/overlord/verify_governance_consumer.py`, `docs/governance-consumer-pull-state.json` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #537 |

## Pattern: malformed-local-overrides

| Field | Value |
|---|---|
| Signature | Consumer verifier rejects `local_overrides` metadata or reports a forbidden override class. |
| Category | consumer verifier |
| Root Cause | Worker wrote override metadata that was malformed, incomplete, or outside the allowed consumer-local override contract. |
| Correction | Normalize `local_overrides` to the verifier schema, remove forbidden override classes, and rerun verifier before handoff. |
| Guardrail | Strict override metadata validation. |
| Validation | Consumer verifier tests for malformed override metadata and forbidden override classes. |
| Related Files | `scripts/overlord/verify_governance_consumer.py`, `docs/governance-consumer-pull-state.json` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #537 |

## Pattern: typoed-governance-root

| Field | Value |
|---|---|
| Signature | `File not found` or package verification failure references a misspelled governance root path. |
| Category | governance evidence |
| Root Cause | Worker or operator command used a stale or typoed absolute path instead of resolving the repo root from the current checkout. |
| Correction | Resolve the root with `git rev-parse --show-toplevel`, use the governed root override only when documented, and rerun package verification from the intended worktree. |
| Guardrail | Execution-scope root validation and managed shim `HLDPRO_GOVERNANCE_ROOT` verification. |
| Validation | `scripts/overlord/assert_execution_scope.py` plus local package/verifier dry run from the target worktree. |
| Related Files | `scripts/overlord/assert_execution_scope.py`, `docs/governance-tooling-package.json` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #537 |

## Pattern: pr-checks-pending-exit-code-eight

| Field | Value |
|---|---|
| Signature | `gh pr checks` exits with code 8 while checks are still `pending`. |
| Category | merge/check flow |
| Root Cause | Polling command treated GitHub's pending-check exit as a hard failure instead of a wait state. |
| Correction | Poll check state explicitly, classify pending as wait, and only merge after required checks are pass or skipped according to repository policy. |
| Guardrail | PR supervisor contract separates pending, failed, and passed states. |
| Validation | Fake `gh pr checks` fixtures for pending, fail, pass, and skipped states. |
| Related Files | `scripts/orchestrator/cli_session_supervisor.py`, `scripts/orchestrator/test_cli_session_supervisor.py` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #536 |

## Pattern: local-multi-worktree-main-merge-conflict

| Field | Value |
|---|---|
| Signature | `gh pr merge` or a local merge flow hits a main conflict caused by multiple local worktrees. |
| Category | merge/check flow |
| Root Cause | Merge flow depended on local main/worktree state when the authoritative PR merge decision was on GitHub. |
| Correction | Merge through GitHub's PR API or `gh pr merge` against the PR without switching local main; refresh local refs after merge. |
| Guardrail | PR supervisor should avoid local main checkout mutation for merge operations. |
| Validation | Merge dry-run or fake supervisor test proves no local main checkout is required. |
| Related Files | `scripts/orchestrator/cli_session_supervisor.py`, `.github/workflows/governance-check.yml` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #536 |

## Pattern: sql-schema-drift-stale-column

| Field | Value |
|---|---|
| Signature | Wipe or migration reaches later SQL and fails because a query uses `org_id` while `organizations` has `organization_id`. |
| Category | schema drift |
| Root Cause | SQL referenced a stale column name not covered by a schema probe before destructive or late-stage operations. |
| Correction | Update the query to the canonical column name and add a schema probe that checks expected columns before executing the wipe or migration sequence. |
| Guardrail | Repo-local SQL schema drift probe contract blocks stale column references before late SQL execution. |
| Validation | `python3 scripts/overlord/test_validate_sql_schema_probe_contract.py` and the consumer repo's profile hook exercise live or fixture schema metadata before mutation. |
| Related Files | `docs/runbooks/sql-schema-drift-probes.md`, `docs/examples/sql-schema-drift/healthcareplatform-maintenance-reset.json`, `scripts/overlord/validate_sql_schema_probe_contract.py` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #534 |

## Pattern: stage6-closeout-missing-before-handoff

| Field | Value |
|---|---|
| Signature | Implementation session reaches PR readiness with no issue-matching `raw/closeouts/*issue-NNN*.md`. |
| Category | governance evidence |
| Root Cause | Closeout validation existed but closeout creation was not merge-enforced. |
| Correction | Create the Stage 6 closeout before handoff/merge, validate it, and keep implementation diffs inside the declared execution scope. |
| Guardrail | Stage 6 closeout presence gate in reusable governance CI and Local CI. |
| Validation | `python3 scripts/overlord/check_stage6_closeout.py --root . --branch-name issue-NNN --changed-files-file <file>`. |
| Related Files | `scripts/overlord/check_stage6_closeout.py`, `raw/closeouts/TEMPLATE.md` |
| First Observed | 2026-04-21 |
| Prevented By | Issue #541, pattern `stage6-closeout-passive-gate` |
