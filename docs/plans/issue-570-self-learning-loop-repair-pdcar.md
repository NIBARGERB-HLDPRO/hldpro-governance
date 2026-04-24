# Issue #570 — Self-Learning Loop Repair (credentials + consolidate-memory + CI integrity)

## Plan

Issue #570 closes three structural gaps found in the 2026-04-24 audit that prevent the operator_context → MEMORY.md write-back loop from ever executing. Gap 1 (High): `consolidate-memory.sh` calls a `count_since` GET action that does not exist in the memory-writer edge function, causing a 405 on every closeout-hook invocation and silently skipping the consolidate step. Fix: rewrite the count logic to use local file state, matching the approach already used by `scripts/orchestrator/self_learning.py`, so no cross-repo edge-function change is required. Gap 2 (High): `AIS_SUPABASE_ANON_KEY` and `AIS_SUPABASE_URL` are not emitted by the `governance` target in `scripts/bootstrap-repo-env.sh`, so `consolidate-memory.sh` always exits at the credential guard before reaching the API call. Fix: add both vars to the governance bootstrap target and document the prerequisite in the always-on-governance runbook. Gap 3 (Medium): the `overlord-sweep.yml` memory integrity step always runs `--allow-missing` on a GitHub Actions runner where `~/.claude/projects/` is absent, so all 6 repos SKIP and CI emits no integrity signal. Fix: add a `memory_integrity.py` invocation (without `--allow-missing`) to `hooks/closeout-hook.sh` scoped to the governance repo, providing real validation at every local closeout. The CI `--allow-missing` flag remains unchanged because self-hosted runners are not available.

## Do

- Removed the Supabase `count_since` HTTP call from `scripts/consolidate-memory.sh` and replaced it with a local file-based count of recent closeout artifacts, matching the pattern in `scripts/orchestrator/self_learning.py`.
- Removed the AIS credential guard from `consolidate-memory.sh` because the local-only path requires no Supabase credentials.
- Added `AIS_SUPABASE_URL` and `AIS_SUPABASE_ANON_KEY` to the `governance` target block in `scripts/bootstrap-repo-env.sh` so future consolidate steps that write to Supabase have credentials available.
- Added a DRY_RUN=1 test confirming both vars appear in the governance target output.
- Added a `memory_integrity.py` call to `hooks/closeout-hook.sh` after the consolidate-memory step, failing loudly if MEMORY.md is absent or malformed (non-fatal, fail-open).
- Updated `docs/runbooks/always-on-governance.md` to document the AIS credential prerequisite and the memory integrity closeout-hook check.

## Check

Planned validation:

- `bash scripts/consolidate-memory.sh --repo hldpro-governance --dry-run` exits 0 without credentials and without a 405.
- `DRY_RUN=1 bash scripts/bootstrap-repo-env.sh governance` output contains `AIS_SUPABASE_URL` and `AIS_SUPABASE_ANON_KEY`.
- `python3 scripts/overlord/memory_integrity.py` (without `--allow-missing`) exits 0 on a machine with a populated `~/.claude/projects/` directory.
- `hooks/closeout-hook.sh` invokes `memory_integrity.py` and does not abort when MEMORY.md is present.
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py docs/plans/issue-570-self-learning-loop-repair-structured-agent-cycle-plan.json` exits 0.
- Local CI Gate passes.

## Adjust

The self-learning loop stays deterministic and local-file-based. No cross-repo edge-function changes are authorized. The AIS memory-writer edge function remains write-only; the read path (count_since) is not implemented in AIS and must not be implemented there. If the governance MEMORY.md write-back loop later requires richer session-count signals, a separate issue must be opened before any Supabase read path is considered.

## Review

Alternate-family review is required before implementation proceeds. No review has been requested as of this planning session (2026-04-24). The implementation agent must obtain cross-family review and record it at `raw/cross-review/2026-04-24-issue-570-self-learning-loop-repair.md` before merge.
