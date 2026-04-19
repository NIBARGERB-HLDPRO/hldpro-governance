# Validation - Issue #347 Qwen3.6 Mac Model Roster

Date: 2026-04-19
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/347
PR: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/pull/349
Merge commit: `f2c1318a4faa2ee37814627cb3a8aff8a34ed8a8`
Branch: `issue-347-qwen36-mac-model-roster`

## Source Verification

Primary model sources checked:

- `Qwen/Qwen3.6-35B-A3B`: source model card for the 35B total / A3B active model.
- `mlx-community/Qwen3.6-35B-A3B-4bit`: MLX conversion from `Qwen/Qwen3.6-35B-A3B`, Apache-2.0, 4-bit, approximately 20.4 GB package size.

Governance inventory uses a 24 GB budget for runtime headroom and keeps the entry on-demand only.

## Local Results

| Check | Result |
|---|---|
| `python3 scripts/lam/test_runtime_inventory.py` | PASS; 7 tests |
| `python3 scripts/lam/runtime_inventory.py --timeout 0.2` | PASS; no prompt payloads sent; `worker_lam_large` reports MLX/on-demand/24 GB; Windows metadata probe timed out safely when unreachable |
| `python3 -m py_compile scripts/lam/runtime_inventory.py scripts/lam/test_runtime_inventory.py` | PASS |
| `python3 -m json.tool docs/plans/issue-347-structured-agent-cycle-plan.json` | PASS |
| `python3 -m json.tool raw/execution-scopes/2026-04-19-issue-347-qwen36-mac-model-roster-implementation.json` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-347-qwen36-mac-model-roster --require-if-issue-branch` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-347-qwen36-mac-model-roster --changed-files-file /tmp/issue-347-changed-files.txt --enforce-governance-surface` | PASS |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-19-issue-347-qwen36-mac-model-roster-implementation.json --changed-files-file /tmp/issue-347-changed-files.txt` | PASS; declared active parallel roots warned only |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `git diff --check` | PASS |
| `tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance --json` | PASS |

## GitHub Results

PR #349 passed all required checks after rebasing onto current `origin/main` and adding the issue-specific execution scope:

- `local-ci-gate`: PASS
- `validate`: PASS
- `contract`: PASS
- `commit-scope`: PASS
- `Analyze (actions)`: PASS
- `Analyze (python)`: PASS
- `CodeQL`: PASS

## Acceptance Criteria

| AC | Result |
|---|---|
| MLX model ID appropriate for this MacBook setup, not BF16 or Windows/Ollama placement | PASS; `.lam-config.yml` uses `mlx-community/Qwen3.6-35B-A3B-4bit` under Mac worker candidates |
| On-demand only and does not displace resident Guardrail-LAM or warm MCP intent | PASS; `worker_lam_large.resident` is false and existing guardrail/MCP entries are unchanged |
| Runtime inventory reports conservative memory budget and policy note | PASS; inventory reports 24 GB and one-large-on-demand-model-at-a-time policy |
| PII boundaries unchanged | PASS; `pii_to_cloud_allowed=false`, `pii_to_windows_allowed=false`, and missing patterns still halt/fail closed |
| PDCA/R artifact records Plan, Do, Check, Adjust, Review | PASS |
| End-to-end local and GitHub validation passes | PASS |

## Reviewer Checkpoint

Read-only reviewer agent reported no blocking findings. Two hardening recommendations were completed before merge: config/inventory drift coverage and explicit pass/fail evidence in the PDCA/R artifact.
