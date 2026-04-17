# Issue #228 — Local Model Runtime and Guardrail Lane PDCA/R

## Plan

Issue #228 inventories local model runtime capacity without granting autonomous authority. The slice must document Mac memory budgets, resolve the stale Windows VRAM assumption conservatively, add metadata-only health probes, and keep PII routing fail-closed.

## Do

- Added `scripts/lam/runtime_inventory.py`.
- Added `scripts/lam/test_runtime_inventory.py`.
- Added `docs/runbooks/local-model-runtime.md`.
- Added `docs/runbooks/windows-ollama.md`.
- Updated `STANDARDS.md` to replace the stale Windows 16 GB VRAM assertion with unverified VRAM status.
- Added the issue-specific structured plan required by the governance-surface gate.
- Extended the governance-surface classifier to cover `scripts/lam/` now that this slice introduces runtime guardrail probes there.

## Check

Planned validation:

- `python3 scripts/lam/test_runtime_inventory.py`
- `python3 scripts/lam/runtime_inventory.py`
- `python3 -m py_compile scripts/lam/runtime_inventory.py scripts/lam/test_runtime_inventory.py`
- `bash scripts/windows-ollama/tests/test_decide.sh`
- `python3 -m pytest scripts/windows-ollama/tests/test_submit.py scripts/windows-ollama/tests/test_audit.py`
- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-228-model-runtime-20260417 --require-if-issue-branch`
- governance-surface changed-file validation with `--enforce-governance-surface`
- model pin checks
- graphify governance contract check
- org governance compendium freshness check

## Adjust

The Windows endpoint timed out from the Mac during the 2026-04-17 probe. The implementation therefore does not claim Windows availability, installed models, or VRAM-backed placement. It records Windows as LAN-only fallback/batch/health infrastructure until direct host telemetry exists.

The runtime inventory probe uses `/api/tags` only for Windows and sends no prompt payloads to any model endpoint.

## Review

Alternate-family review is recorded in `raw/cross-review/2026-04-17-model-runtime.md`.
