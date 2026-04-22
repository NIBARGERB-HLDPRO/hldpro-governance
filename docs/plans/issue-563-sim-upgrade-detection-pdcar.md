# PDCAR — Issue #563: hldpro-sim Upgrade Detection Documentation

**Date:** 2026-04-22
**Issue:** https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/563
**Author:** claude-sonnet-4-6 (session-20260422-issue-563-sim-upgrade-detection)

---

## Problem

Consumer repos that install hldpro-sim via `scripts/deployer/deploy-hldpro-sim.sh` have no documented way to:
1. Check which version they have installed (pinned SHA)
2. Determine if that version is current relative to the governance repo
3. Trigger a re-deploy when a new version is released

The deployer writes a consumer record at `.hldpro/hldpro-sim.json`, and the governance repo maintains `docs/hldpro-sim-consumer-pull-state.json` as the canonical current state, but no adoption guide or runbook explains how to use these files together for version management. This creates a drift risk: consumer repos may silently run stale versions of hldpro-sim with outdated personas.

A drift detector script (`scripts/overlord/check_hldpro_sim_version.py`) was considered for this issue but is deferred because prior attempts at similar worker handoffs were blocked by the worker-handoff gate; keeping this issue documentation-only avoids that blocker.

---

## Decision

Add a **hldpro-sim Version Management** section to `docs/agents-adoption-guide.md` covering:
- How to read the installed version from `.hldpro/hldpro-sim.json`
- How to compare `pinned_sha` against `docs/hldpro-sim-consumer-pull-state.json`
- How to trigger re-deploy via the deployer script
- A note that automated drift detection is tracked in a follow-up issue

No new Python files are introduced in this issue.

---

## Context

- `docs/hldpro-sim-consumer-pull-state.json` is the governance-owned canonical state record. It contains `pinned_sha`, `tag`, `install_methods`, `managed_personas`, `deployer_script`, and `consumer_record_path`.
- Consumer repos write `.hldpro/hldpro-sim.json` at deploy time (same schema fields as the governance pull-state record, plus local deploy metadata).
- The deployer script is `scripts/deployer/deploy-hldpro-sim.sh` and accepts a consumer repo path as its argument.
- Personas live in `packages/hldpro-sim/personas/` and are deployed to `sim-personas/shared/` in the consumer repo.
- Governing issues: #407 (package build), #422 (deployer + consumer record), #563 (this — version management docs).

---

## Action

1. Write and validate `docs/plans/issue-563-sim-upgrade-detection-structured-agent-cycle-plan.json`
2. Write `raw/execution-scopes/2026-04-22-issue-563-sim-upgrade-detection-implementation.json`
3. Append version management section to `docs/agents-adoption-guide.md`
4. Write `raw/closeouts/2026-04-22-issue-563-sim-upgrade-detection.md` and run closeout hook
5. Commit all artifacts in one commit on branch `issue-563-hldpro-sim-upgrade-detection-20260422`

---

## Result

After merge:
- `docs/agents-adoption-guide.md` will have a version management section that any consumer repo operator can follow to check and refresh their hldpro-sim installation
- The drift detector script remains deferred; its follow-up issue will reference this PDCAR as prior context
- All five artifacts exist and are linked via the structured plan and execution scope

---

## Residual / Follow-Up

- Drift detector script (`scripts/overlord/check_hldpro_sim_version.py`) + overlord-sweep integration: tracked as a follow-up issue (to be opened after merge)
- Consumer-side CI automation for pinned SHA enforcement: not in scope for this issue
