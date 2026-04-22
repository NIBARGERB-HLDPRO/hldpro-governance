# PDCAR — Issue #562: sim-runner Pre-flight Consumer Record + SHA Validation

**Date:** 2026-04-22
**Issue:** https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/562
**Branch:** issue-562-sim-runner-preflight-20260422
**Agent:** sim-runner (agents/sim-runner.md)
**Model:** claude-sonnet-4-6

---

## Problem

`agents/sim-runner.md` Step 1 documented that hldpro-sim must be deployed, but provided no pre-flight validation. An agent invoking sim-runner could proceed to import hldprosim and fail with an obscure Python import error rather than a clear actionable HALT. Additionally, there was no check to detect whether the deployed version in the consumer repo matched the canonical governance version, leaving version drift silent.

---

## Decision

Add a **Step 0 Pre-flight** to `agents/sim-runner.md` that runs before any existing step:

1. HALT with a clear deploy command if `.hldpro/hldpro-sim.json` is absent.
2. Compare `pinned_sha` from consumer record vs. `docs/hldpro-sim-consumer-pull-state.json`.
3. SHA match → print CURRENT message and continue.
4. SHA mismatch → print WARNING with both SHAs (first 8 chars) and re-deploy recommendation, then continue (not a hard HALT).

The SHA mismatch is a WARNING, not a HALT, because a redeployment may be pending and the consumer may still have a functional (if stale) version installed.

---

## Context

- Issue #561 added the deployer reference to Step 1 of sim-runner.md.
- The canonical state is in `docs/hldpro-sim-consumer-pull-state.json`: `pinned_sha: fed5ead670cf6834e5c73bffcaf64e41cc483fce`, version `0.1.0`.
- Consumer record path is `.hldpro/hldpro-sim.json` per the deployer contract (issue #422).

---

## Action

Edited `agents/sim-runner.md` using the Edit tool to insert the Step 0 Pre-flight block immediately before the existing Step 1. No other files in the agent or deployer surface were modified.

---

## Result

`agents/sim-runner.md` now has Step 0 Pre-flight as the first workflow step. Any sim-runner invocation will:
- HALT immediately with a clear, actionable message if hldpro-sim is not deployed.
- Emit a version-current confirmation when SHAs match.
- Emit a soft warning (proceed anyway) when SHAs differ, allowing workflows to continue without blocking.

---

## Structured Plan Reference

`docs/plans/issue-562-sim-runner-preflight-structured-agent-cycle-plan.json`

Validator: `PASS validated 155 structured agent cycle plan file(s)`

---

## Files Changed

- `agents/sim-runner.md` — Step 0 Pre-flight block added

## Files Added

- `docs/plans/issue-562-sim-runner-preflight-structured-agent-cycle-plan.json`
- `docs/plans/issue-562-sim-runner-preflight-pdcar.md`
- `raw/execution-scopes/2026-04-22-issue-562-sim-runner-preflight-implementation.json`
- `raw/closeouts/2026-04-22-issue-562-sim-runner-preflight.md`
