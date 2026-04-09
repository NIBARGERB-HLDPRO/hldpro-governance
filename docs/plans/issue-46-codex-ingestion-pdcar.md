# Issue 46 — Codex Ingestion Operationalization PDCA/R

Date: 2026-04-09
Issue: `#46`
Repo: `hldpro-governance`

## Plan

Verify whether the Codex ingestion helper and weekly sweep path still have a real production-readiness gap, or whether the remaining backlog item is now stale and only needs closeout.

Success criteria:
- prove a real governed-repo `generate -> qualify -> status` cycle completes under the current helper/runtime
- confirm the weekly sweep already contains the canary/auth/timeout protections captured in fail-fast history
- close the stale backlog note if no new code change is required

## Do

- inspect `scripts/overlord/codex_ingestion.py`, `scripts/overlord/README.md`, and `.github/workflows/overlord-sweep.yml`
- run a real Codex review cycle against `knocktracker`
- verify `review-*.json`, `qualified-*.json`, and `backlog-*.md` are written successfully
- re-run `status` to confirm backlog surfacing works on the generated artifact set

## Check

- `python3 scripts/overlord/codex_ingestion.py generate --repo knocktracker ...`
- `python3 scripts/overlord/codex_ingestion.py qualify --repo knocktracker ...`
- `python3 scripts/overlord/codex_ingestion.py status --repo knocktracker ... --latest-only`
- inspect the generated JSON/markdown artifacts under a bounded temporary ingestion root

## Adjust

- if validation succeeds, treat the remaining backlog note as stale and move the item to `Done`
- if validation fails, log the exact new blocker in `docs/FAIL_FAST_LOG.md` and keep the issue open with the new root cause

## Review

Observed result:
- the current helper completed a real `knocktracker` review cycle and wrote `review-2026-04-09.json`, `qualified-2026-04-09.json`, and `backlog-2026-04-09.md`
- `status --latest-only` correctly surfaced the generated backlog file
- no new runtime/auth blocker was discovered beyond the already-documented fail-fast history
