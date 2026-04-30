# Validation: Issue #627 Local Root-Hook Fallback Proof

Date: 2026-04-30
Repo: hldpro-governance
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/627
Branch: `issue-627-local-root-hook-fallback-proof`

## Scope

This validation artifact records the bounded implementation slice for issue
`#627`, limited to local `governance-check.sh` consumption of the merged
`#625` degraded-fallback proof contract through a mechanical helper and
focused tests.

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 -m json.tool docs/plans/issue-627-local-root-hook-fallback-proof-structured-agent-cycle-plan.json` | PASS | Structured plan JSON parses cleanly after promotion to `implementation_ready`. |
| `python3 -m json.tool raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json` | PASS | Implementation execution-scope JSON parses cleanly and carries the merged `#625` degraded-fallback fields. |
| `python3 -m json.tool raw/handoffs/2026-04-30-issue-627-plan-to-implementation.json` | PASS | Implementation handoff JSON parses cleanly with issue-local packet, review, gate, and closeout refs. |
| `python3 scripts/overlord/test_check_governance_hook_execution_scope.py` | PASS | Focused helper tests passed: planning-only no-op, valid same-family degraded fallback, missing proof field failure, unsafe ref failure, and ordinary cross-family pass-through. |
| `bash -n hooks/governance-check.sh` | PASS | Hook shell syntax is valid after adding execution-scope replay. |
| `python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-30-issue-627-local-root-hook-fallback-proof-implementation.json --require-lane-claim` | PASS with warnings | Implementation scope validates; warnings only reflect declared dirty parallel roots. |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-627-local-root-hook-fallback-proof --require-if-issue-branch` | PASS | Structured plan validator passed on the active issue-627 branch. |
| `python3 scripts/overlord/validate_handoff_package.py --root . raw/handoffs/2026-04-30-issue-627-plan-to-implementation.json` | PASS after closeout exists | Implementation handoff passes once the issue-local closeout artifact is present. |
| `bash scripts/cross-review/require-dual-signature.sh raw/cross-review/2026-04-30-issue-627-local-root-hook-fallback-proof-plan.md` | PASS | Issue-local cross-review artifact retains valid dual-signature planning frontmatter. |
| `bash hooks/governance-check.sh` | PASS | Live positive root-hook proof: the local governance hook replays the active implementation-capable issue-627 scope and passes after backlog mirror and branch parity co-staging. |
| `bash hooks/governance-check.sh` with `cross_family_path_ref` temporarily removed from the issue-627 implementation scope, then restored immediately | PASS (expected fail-closed, exit 1) | Live negative root-hook proof: the local governance hook blocked with `planner/implementer same model or family requires handoff_evidence.cross_family_path_ref`, proving local consumption of the merged `#625` contract. |
| `bash scripts/codex-review.sh claude raw/packets/2026-04-30-issue-627-claude-review-packet.md` | PASS | Implementation-phase alternate-family review returned `APPROVED` and was normalized into `docs/codex-reviews/2026-04-30-issue-627-claude.md`. |
| `python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-30-issue-627-local-root-hook-fallback-proof.md --root .` | PASS | Stage 6 closeout validated cleanly after the implementation-phase artifacts were normalized. |
| `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | PASS | Local CI Gate passed on the issue-627 implementation slice with report dir `cache/local-ci-gate/reports/20260430T133022Z-hldpro-governance-git`. |
| `git diff --check` | PASS | Diff hygiene is clean on the bounded implementation slice so far. |

## Findings

- Issue `#627` stays bounded to:
  - `hooks/governance-check.sh`
  - `scripts/overlord/check_governance_hook_execution_scope.py`
  - `scripts/overlord/test_check_governance_hook_execution_scope.py`
  - required governance doc co-staging
  - issue-local artifacts
- The implementation consumes the merged `#625` degraded-fallback proof
  contract by replaying the active implementation-capable execution scope
  through `assert_execution_scope.py`, rather than reimplementing the contract
  in shell.
- `hooks/backlog-check.sh` remains unchanged in this slice and retains only
  backlog/parity behavior.
- Live root-hook proof now exists for:
  - one allowed governance-check path
  - one blocked same-family degraded-fallback path
- The slice preserves explicit external boundaries for:
  - `#625` execution-scope ownership
  - `#612` fallback-log schema/workflow parity
  - `#607` planning-authority work
  - `#614` downstream verifier/drift-gate work

## Residual Risk

- None. This slice remains bounded and does not claim broader `#615` or `#612`
  closure.
