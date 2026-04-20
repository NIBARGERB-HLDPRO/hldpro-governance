# PDCAR: hldpro-sim v0.1.0 Deployment Readiness

Date: 2026-04-20
Branch: `issue-422-hldpro-sim-deploy-20260420`
Repo: `hldpro-governance`
Status: APPROVED — implementation ready
GitHub issue: [#422](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/422)

## Problem

`packages/hldpro-sim/` (governance-owned OASIS simulation engine) is implemented and tested
(13/13 tests pass, PR #411 merged) but is not consumable by Stampede or any other product repo.
Two blockers:

1. **No version tag** — no `hldpro-sim-v0.1.0` git tag exists; consumers cannot pin to a stable SHA.
2. **No deployer** — no managed installer pushes the package + shared personas to consumer repos.
   Stampede's Slice 6 (simulation runner) cannot start without an adoption path.

## Plan

Two-sprint implementation following the governance-tooling-v0.1.0 precedent (PR #401):

**Sprint 1 — Version tag + distribution contract**
- Push `hldpro-sim-v0.1.0` tag → PR #411 merge commit (`fed5ead670cf6834e5c73bffcaf64e41cc483fce`)
- Commit `docs/hldpro-sim-consumer-pull-state.json` documenting package + managed personas contract

**Sprint 2 — Deployer script + validation**
- `scripts/deployer/deploy-hldpro-sim.sh <consumer-repo-path> [--dry-run]`
  - Installs `packages/hldpro-sim/` into consumer (pip install -e, fallback: directory copy)
  - Deploys `packages/hldpro-sim/personas/` → `<consumer>/sim-personas/shared/` (managed, read-only)
  - Writes `<consumer>/.hldpro/hldpro-sim.json` consumer record with pinned SHA + install method
- Dry-run proof against `/tmp/sim-consumer-test`
- Validation evidence committed to `raw/validation/`

## Scope

In scope:
- `hldpro-sim-v0.1.0` git tag
- `docs/hldpro-sim-consumer-pull-state.json`
- `scripts/deployer/deploy-hldpro-sim.sh`
- `raw/validation/2026-04-20-issue-422-hldpro-sim-deploy.md`

Out of scope:
- `packages/hldpro-sim/` source changes (already merged, no regressions)
- `ClaudeCliProvider` implementation (separate issue)
- Stampede adoption PR (Stampede owns that; unblocked once deployer ships)
- Cloud/API provider (future issue)

## Do

1. Push `hldpro-sim-v0.1.0` tag from this worktree
2. Commit `docs/hldpro-sim-consumer-pull-state.json`
3. Write and test `scripts/deployer/deploy-hldpro-sim.sh --dry-run`
4. Commit validation evidence
5. PR → CI green → merge

## Check

```bash
# Tag points to correct commit
git rev-list -n 1 hldpro-sim-v0.1.0
# expected: fed5ead670cf6834e5c73bffcaf64e41cc483fce

# Deployer dry-run
bash scripts/deployer/deploy-hldpro-sim.sh /tmp/sim-consumer-test --dry-run

# Consumer record written
cat /tmp/sim-consumer-test/.hldpro/hldpro-sim.json | python3 -m json.tool

# Personas deployed
ls /tmp/sim-consumer-test/sim-personas/shared/

# CI gate
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --enforce-governance-surface
python3 scripts/overlord/assert_execution_scope.py \
  --scope raw/execution-scopes/2026-04-20-issue-422-hldpro-sim-deploy-implementation.json \
  --require-lane-claim
```

## Adjust

If pip-editable install fails in consumer env (Python 3.14 on Stampede), fall back to directory copy
and record `install_method: "directory-copy"` in the consumer record. Deployer must degrade gracefully.

## Review

Self-approved — non-architecture implementation slice, same-model exception active.
No cross-review artifact required. Implementation may start immediately.
