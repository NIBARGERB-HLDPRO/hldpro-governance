# Issue #403 Validation: Knocktracker Consumer-Pull Pilot

Date: 2026-04-20
Governance issue: `NIBARGERB-HLDPRO/hldpro-governance#403`
Downstream issue: `NIBARGERB-HLDPRO/knocktracker#177`

## Downstream PRs

| PR | Result | Evidence |
| --- | --- | --- |
| `NIBARGERB-HLDPRO/knocktracker#178` | Merged | Added `.github/workflows/consumer-governance-verifier.yml`, refreshed managed `.hldpro` pin to governance ref `615f4848568ac9a1633d82e0fac0d27d79d39c8f`, and proved the new `verify-consumer-governance` job passed. |
| `NIBARGERB-HLDPRO/knocktracker#179` | Merged | Repaired the sprint-doc gate by updating `docs/sprint/runner-status.md`; all seven PR checks passed before merge. |

## Local Verification

- `deploy_governance_tooling.py verify`: passed for `knocktracker`, profile `knocktracker`, package `0.1.0-contract`, governance ref `615f4848568ac9a1633d82e0fac0d27d79d39c8f`.
- `verify_governance_consumer.py`: passed against the knocktracker worktree and pinned consumer record.
- Negative control: `verify_governance_consumer.py` with mismatched package version `0.1.0-contract-negative` failed as expected.
- `/opt/homebrew/bin/actionlint .github/workflows/consumer-governance-verifier.yml`: passed.
- `npm run pr:dry-run`: passed for downstream PR bodies after the issue branch was clean.
- `.hldpro/local-ci.sh`: passed when local `python3` was mapped to `python3.11`; the default local `python3` lacks PyYAML.

## GitHub Verification

PR #179 was the final green downstream correction PR. Checks:

- `CI / validate`: success.
- `Consumer Governance Verifier / verify-consumer-governance`: success.
- `PR Hygiene / validate-pr`: success.
- `Security / gitleaks`: success.
- `Security / npm-audit`: success.
- `Workflow Lint / actionlint`: success.
- `sprint-doc-gate / require-sprint-status-update`: success.

## Incident / Adjustment

PR #178 merged even though `sprint-doc-gate` failed and some checks were still pending because the repository did not enforce those checks as merge-blocking. The verifier job itself passed. PR #179 corrected the missing runner-status evidence and was merged only after all checks were green.

## Rollback

Rollback remains PR-based:

- revert PR #178 to remove the verifier workflow and managed `.hldpro` pin refresh; or
- revert PR #179 if only the runner-status documentation correction must be undone; or
- run the governance deployer rollback for `.hldpro/local-ci.sh` and `.hldpro/governance-tooling.json` if the managed package pin itself must be removed.

No central GitHub rulesets, branch protections, bypass actors, or repository settings were changed by the downstream pilot.
