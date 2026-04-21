# Issue #459 Sonnet Worker Brief

You are a Claude Sonnet 4.6 worker in the hldpro-governance repository. You are not alone in the repo. Do not revert unrelated changes, especially generated wiki/graphify files already dirty in this worktree. Codex is orchestrator and QA.

## Scope

Implement only the bounded issue #459 slice:

- Add `scripts/overlord/report_governance_consumer_status.py`.
- Add `scripts/overlord/test_report_governance_consumer_status.py`.
- Wire the report into `.github/workflows/overlord-sweep.yml`.
- Wire focused tests into `tools/local-ci-gate/profiles/hldpro-governance.yml`.

Do not edit downstream repos. They are read-only status targets only.

## Acceptance Criteria

1. The weekly sweep can report each sweep-enabled consumer repo's profile, governance SHA, package version, managed files, local overrides, verifier status, workflow pin status, and residual drift.
2. The report distinguishes critical failures from migration warnings.
3. The reporter emits deterministic Markdown and JSON.
4. The reporter reuses `scripts/overlord/verify_governance_consumer.py` and `scripts/overlord/governed_repos.py` instead of duplicating core verifier logic.
5. Focused tests cover passing status, missing-record critical status, warning-only classification, and mutable/mismatched workflow pin status.

## Implementation Notes

- Resolve repos from `governed_repos.repos_enabled_for("sweep")`.
- In GitHub Actions, repos are under `repos/<repo_dir_name>` from `ci_checkout_path`; locally, use `HLDPRO_REPOS_ROOT` or `/Users/bennibarger/Developer/HLDPRO`.
- Use desired-state profile package versions from `docs/governance-consumer-pull-state.json` when invoking the verifier.
- Default exact governance SHA comparison should be optional. The report must still show the observed SHA from the consumer record.
- Markdown should include a summary table plus `Critical Failures` and `Migration Warnings` sections.
- Exit nonzero only with an explicit `--fail-on-critical` flag.

## Validation To Run If Time Permits

- `python3 -m unittest scripts.overlord.test_report_governance_consumer_status`
- `python3 -m py_compile scripts/overlord/report_governance_consumer_status.py`
