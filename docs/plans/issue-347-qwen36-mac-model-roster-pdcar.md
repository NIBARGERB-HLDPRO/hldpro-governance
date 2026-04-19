# Issue #347 — Qwen3.6-35B-A3B Mac Model Roster PDCA/R

## Plan

Add `Qwen/Qwen3.6-35B-A3B` to the governed local model roster in the Mac-appropriate MLX form. The slice is documentation and inventory metadata only: no model download, no prompt payload, no autonomous routing authority, and no PII boundary change.

Acceptance criteria from issue #347:

- Use an MLX model ID appropriate for the MacBook setup.
- Keep the entry on-demand only.
- Report the candidate through runtime inventory with a conservative memory budget.
- Preserve fail-closed PII routing boundaries.
- Record PDCA/R evidence.
- Pass local end-to-end validation.

## Do

- Added `mlx-community/Qwen3.6-35B-A3B-4bit` as a large on-demand Worker-LAM candidate in `.lam-config.yml`.
- Added `worker_lam_large` to `scripts/lam/runtime_inventory.py`.
- Added a focused unit test proving the model is MLX, on-demand, and bounded to a 24 GB budget.
- Updated `docs/runbooks/local-model-runtime.md` to document the Mac placement decision and explain why BF16 and 8-bit variants are not the default for this 48 GB lane.
- Added this PDCA/R artifact and an issue-specific structured plan.

## Check

Validation commands:

| Command | Result |
|---|---|
| `python3 scripts/lam/test_runtime_inventory.py` | PASS — 6 tests before review hardening; 7 tests after config/inventory drift coverage was added |
| `python3 scripts/lam/runtime_inventory.py --timeout 0.2` | PASS — no prompt payloads sent; Windows metadata probe timed out safely; `worker_lam_large` reported as MLX/on-demand/24 GB |
| `python3 -m py_compile scripts/lam/runtime_inventory.py scripts/lam/test_runtime_inventory.py` | PASS |
| `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-347-qwen36-mac-model-roster --require-if-issue-branch` | PASS |
| governance-surface validation with the changed-file list and `--enforce-governance-surface` | PASS |
| `python3 scripts/overlord/check_overlord_backlog_github_alignment.py` | PASS |
| `git diff --check` | PASS |
| focused content check for the Qwen3.6 model ID, `worker_lam_large`, and unchanged PII boundary text | PASS |

## Adjust

The chosen model ID is `mlx-community/Qwen3.6-35B-A3B-4bit`. The BF16 package is too large for the 48 GB Mac lane, and the 8-bit package leaves too little headroom after resident guardrail and intent models. The 24 GB budget is conservative for an on-demand large worker candidate and preserves the existing one-large-model-at-a-time policy.

If runtime testing later proves this model too slow or memory-tight for the Mac lane, the follow-up should benchmark a smaller quantized MLX variant or the 19 GB Mac-focused package before promoting it beyond candidate status.

## Review

Review status for this slice is local implementation review plus automated validation. No alternate-family cross-review artifact is required because this change does not alter `STANDARDS.md`, routing order, PII policy, or autonomous execution authority.
