# Issue 45 — Governance Doc Consistency Rollout PDCA/R

Date: 2026-04-09
Issue: `#45`
Repo Scope:
- `hldpro-governance`
- `local-ai-machine`
- `knocktracker`

## Plan

Tighten the minimum governance-doc contract so governed repos cannot satisfy `docs/DATA_DICTIONARY.md` and `docs/SERVICE_REGISTRY.md` with placeholder rows only, while preserving the existing AIS and HealthcarePlatform exceptions.

Success criteria:
- shared standards explicitly require source-of-truth metadata for data and service docs
- reusable governance CI fails placeholder-only dictionary/service docs
- `local-ai-machine` and `knocktracker` pass the stricter contract with real entries
- no repo-specific exception is flattened away

## Do

- update `STANDARDS.md` with the stricter minimum contract
- update reusable `governance-check.yml` to block placeholder-only dictionary/service registry docs
- normalize `local-ai-machine` metadata formatting and replace its placeholder service registry
- replace KnockTracker placeholder data dictionary and service registry rows with real summarized entries

## Check

- `git diff --check` in all touched repos
- `python3`/shell contract checks pass locally
- updated docs still reflect the real repo topology instead of generic template text

## Adjust

- keep HealthcarePlatform pointer semantics intact
- keep AIS backlog/document exceptions intact
- prefer compact source-of-truth summaries over exhaustive mirrors of migrations or code

## Review

Expected review focus:
- contract is stricter but still repo-safe
- low-risk scaffolding repos now satisfy the contract with real metadata
- no new hidden repo exceptions were introduced
