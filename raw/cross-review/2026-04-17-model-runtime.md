# Cross-Review — Issue #228 Local Model Runtime and Guardrail Lane

Date: 2026-04-17
Issue: #228
Reviewer: Claude Opus 4.6
Reviewed worktree: `/Users/bennibarger/Developer/HLDPRO/_worktrees/gov-issue-228-model-runtime-20260417`
Verdict: APPROVED_WITH_CHANGES
Final disposition: Accepted after required changes

## Scope

Read-only alternate-family review of the #228 model runtime diff:

- `scripts/lam/runtime_inventory.py`
- `scripts/lam/test_runtime_inventory.py`
- `docs/runbooks/local-model-runtime.md`
- `docs/runbooks/windows-ollama.md`
- `STANDARDS.md` Windows hardware/VRAM wording
- governance-surface classifier update for `scripts/lam/`
- #228 plan, PDCAR, and registry documentation

## Findings

### B-1 — Test-generated Windows audit artifacts had manifest drift

Severity: blocking raw-artifact integrity issue
Status: resolved

Reviewer finding: local Windows-Ollama tests generated untracked `raw/remote-windows-audit/2026-04-17.jsonl` and manifest files where the JSONL contained more entries than the manifest covered.

Resolution: removed the untracked test-generated raw audit and fallback files from the issue worktree after clearing the macOS append-only flag. No raw Windows audit artifact is part of this PR.

### NB-1 — Windows role strings were inconsistent

Severity: non-blocking consumer ergonomics
Status: resolved

Resolution: unified Windows role reporting to `lan_only_fallback_batch_health_unverified` until direct host telemetry verifies hardware and model placement.

### NB-2 — PII helper import used `sys.path` mutation

Severity: non-blocking robustness issue
Status: resolved

Resolution: switched to `importlib.util.spec_from_file_location()` for the repo-local Windows-Ollama `_pii.py` helper.

### NB-3 — Mac memory budget was static

Severity: non-blocking portability issue
Status: resolved

Resolution: `build_inventory()` now parses the hardware probe memory string and passes the detected total into `memory_budget()`, defaulting to 48 GB only when parsing is unavailable.

### NB-4 — PII guardrail happy-path coverage gap

Severity: non-blocking test coverage issue
Status: resolved

Resolution: added a test asserting the local PII pattern file detects an email probe and does not flag a clean probe.

### NB-5 — Cross-review artifact missing during review

Severity: expected in-flight artifact gap
Status: resolved

Resolution: this file records the review and final disposition.

## Accepted Review Notes

The reviewer verified that:

- The Windows probe calls `/api/tags` only and sends no prompt payloads.
- PII to cloud and PII to Windows are both disallowed.
- Missing PII patterns fail closed.
- STANDARDS now treats Windows VRAM as unverified instead of asserting 16 GB.
- `scripts/lam/` is included in governance-surface path classification and covered by tests.

## Result

All required review changes were applied before closeout validation.
