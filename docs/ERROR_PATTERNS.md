# ERROR_PATTERNS

Reusable solutions to recurring governance failures. See `docs/schemas/error-patterns.schema.md` for the canonical schema.

## Contributing

When a pattern emerges from one or more incidents in `FAIL_FAST_LOG.md`, document it here following the schema:

1. Create a new `## Pattern: <kebab-case-id>` section (kebab-case name, e.g., `overlord-sweep-stale-checkout`)
2. Fill in: Symptom, Root Cause, Detection, Resolution Playbook, Instances
3. Optional: Prevention (can be empty for Phase 1)
4. Reference the pattern in your `FAIL_FAST_LOG.md` entries

See `docs/schemas/error-patterns.schema.md` for examples and detailed field semantics.

## Pattern: overlord-sweep-self-learning-skipped

**Symptom:** `metrics/self-learning/latest.json` remains stale even after new closeouts, fail-fast entries, or operator-context records land.

**Root Cause:** A pre-sweep gate fails before `.github/workflows/overlord-sweep.yml` reaches the `Build self-learning knowledge report` step. In the April 2026 instance, `check_codex_model_pins.py` scanned both an authoritative hldpro-sim provider invocation missing `model_reasoning_effort` and stale local worktree mirrors under `var/worktrees/**`, causing the scheduled sweep to stop before self-learning report generation.

**Detection:** Compare `metrics/self-learning/latest.json.generated_at` to current governance activity. Also inspect the latest `Overlord Sweep -- Weekly Cross-Repo Audit` GitHub Actions run and confirm whether `Build self-learning knowledge report` ran or was skipped.

**Resolution Playbook:** Fix the upstream pre-sweep blocker first, then regenerate the self-learning report locally and let the next scheduled or manual sweep prove remote persistence. If stale worktree mirrors are the failure source, exclude local worktree roots from repo-authoritative scanners rather than editing copied artifacts.

**Instances:**
- 2026-04-20: GitHub Actions run `24674456168` failed at `Validate codex and agent model pins`, so self-learning report generation was skipped.
- 2026-04-21: Issue #475 records the operational proof gap and refreshes self-learning metrics from the current corpus.

**Prevention:** Keep workflow preflight scanners scoped to authoritative repo files, add local validation for `self_learning.py report`, and require at least one issue-backed `raw/operator-context/self-learning/` artifact when closing a self-learning loop gap.
