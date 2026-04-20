# Issue #403 — Consumer-Pulled Governance Adoption Rollout PDCAR

## Plan

Roll out the consumer-pulled governance package model from issue #398 through one low-blast-radius downstream pilot before expanding to other governed repositories.

The first pilot target is `knocktracker` issue #177 because it already completed the prior governance tooling package proof and has a smaller blast radius than the SaaS, HIPAA, or LAM repos.

## Do

- Keep governance as the package source of truth.
- Add repo-side verification in `knocktracker` that reads `.hldpro/governance-tooling.json`, resolves the pinned governance SHA, and runs `scripts/overlord/verify_governance_consumer.py`.
- Keep central GitHub rulesets, required-status wiring, bypass actors, and repository settings report-only from the consumer repo.
- Preserve downstream and governance evidence in issue-backed PRs.

## Check

Required validation for this epic:

- Governance planning/scope validation in this repo.
- Knocktracker local verifier execution against its pinned governance record.
- Knocktracker GitHub Actions proof for the verifier workflow.
- Governance closeout with downstream PR and CI evidence.

## Adjust / Review

If the knocktracker pilot reveals package contract gaps, patch `hldpro-governance` before wider rollout. Do not normalize repo-local forks of package-core logic.

## Rollback

Rollback is per consumer repo:

- revert the downstream verifier workflow PR; or
- disable/remove the workflow file in a follow-up PR; and
- leave existing `.hldpro/governance-tooling.json` and managed Local CI shim untouched unless the managed deployer rollback is explicitly requested.

No central GitHub settings are changed by this rollout slice.
