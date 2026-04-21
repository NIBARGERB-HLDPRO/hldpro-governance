# Org Governance Tooling Distribution Runbook

## Purpose

`hldpro-governance` is the source of truth for shared governance tooling. Governed repos consume a pinned version of that tooling instead of copying runner logic, validators, hook helpers, and workflow contracts by hand.

CI remains authoritative. Local gates are upstream filters for preventable failures before push; a local pass is not a full GitHub Actions replay.

## Package Contract

The machine-readable contract lives at `docs/governance-tooling-package.json`.

The initial package contract defines:

- package owner: `NIBARGERB-HLDPRO/hldpro-governance`
- initial package version: `0.1.0-contract`
- initial release tag: `governance-tooling-v0.1.0`
- required downstream pin: governance git SHA
- recommended readable coordinate: release tag plus git SHA
- consumer record path: `.hldpro/governance-tooling.json`
- final epic gate: downstream end-to-end pull, deploy, local enforcement, GitHub enforcement, and rollback or uninstall proof

Downstream repos must record the governance SHA they consume. A release tag improves readability and rollback communication, but it cannot replace the exact SHA in the consumer record.

## Release Tags

The first package release coordinate is:

```text
governance-tooling-v0.1.0
```

Create release tags only after the release PR merges and GitHub Actions pass. The tag must point at the merged `main` commit that contains the package contract and closeout evidence for that release.

Consumers should use both values:

- release tag for human-readable intent, for example `governance-tooling-v0.1.0`
- exact git SHA for immutable audit evidence in `.hldpro/governance-tooling.json`

Do not deploy from tag name alone. Resolve the tag, record the exact SHA, and keep that SHA in the consumer record. A rollback should name both the previous release tag and the previous SHA when both are known.

## Surface Classes

| Class | Meaning | Examples |
|---|---|---|
| Package core | Shared logic owned by `hldpro-governance` | Local CI Gate runner, execution-scope checker, structured-plan validator |
| Repo profile | Centrally owned repo command mapping | `tools/local-ci-gate/profiles/local-ai-machine.yml` |
| Managed file | Consumer repo file written by a deployer and marked as managed | `.hldpro/local-ci.sh` |
| Repo-local override | Consumer-owned deviation from package defaults | temporary profile exception, repo-specific hook note |
| Tracked baseline | Committed evidence or generated artifact | workflow coverage inventory, scoped graph/wiki outputs |
| Per-run report | Local or CI output not committed by default | `cache/local-ci-gate/reports/` |

Do not collapse these classes. A profile is not a runner fork. A generated baseline is not a per-run report. A local hook is not GitHub branch protection.

## Package Core

The current package-core surfaces are:

- `tools/local-ci-gate/bin/hldpro-local-ci`
- `tools/local-ci-gate/local_ci_gate.py`
- `scripts/overlord/deploy_local_ci_gate.py`
- `scripts/overlord/assert_execution_scope.py`
- `scripts/overlord/check_execution_environment.py`
- `scripts/overlord/validate_structured_agent_cycle_plan.py`
- `scripts/overlord/check_workflow_local_coverage.py`
- supporting tests and schemas named in `docs/governance-tooling-package.json`

Consumers should reference these from a pinned governance checkout or through a managed shim. They should not copy and edit package-core logic in place.

## Repo Profiles

Repo profiles are centrally owned but repo-specific:

- `hldpro-governance`
- `ai-integration-services`
- `knocktracker`
- `local-ai-machine`

Profiles map each repo's existing commands into shared runner semantics. A repo can request profile changes through an issue, but local profile forks require a repo-local override entry and an expiry or review cadence.

## Managed Files

Managed files must be identifiable and reversible.

Current managed paths:

- `.hldpro/local-ci.sh`
- `.governance/local-ci.sh`
- `.hldpro/governance-tooling.json`

The Local CI shim marker is:

```text
# hldpro-governance local-ci gate managed
```

Unmanaged files at managed paths are refused by default. A deployer may support backup or force modes, but those modes require issue evidence.

## Consumer Record

Every downstream deployment must write or update `.hldpro/governance-tooling.json`.

Required fields:

- `schema_version`
- `consumer_repo`
- `governance_repo`
- `governance_ref`
- `package_version`
- `deployed_at`
- `managed_files`
- `profile`
- `local_verification`
- `github_verification`
- `overrides`

This record is the downstream repo's answer to: "Which governance tooling did this repo consume, from where, and how was it verified?"

## Overrides

Repo-local overrides are allowed only when explicit.

An override must include:

- GitHub issue
- reason
- owner
- affected file or profile
- expiry or review cadence
- verification command that still proves the repo is safe

Forbidden overrides:

- forking package-core logic without an issue-backed exception
- disabling a CI-required gate through local package configuration
- treating dry-run output as live enforcement evidence
- hiding generated or per-run artifacts as if they were source-controlled baselines

## Pull And Deploy Contract

The package-level deployer is:

```bash
python3 scripts/overlord/deploy_governance_tooling.py <command>
```

Supported commands:

- `dry-run`: print the planned write set and rollback set without writing files.
- `apply`: write the managed Local CI shim and `.hldpro/governance-tooling.json`.
- `verify`: verify the managed shim and consumer record match the requested governance ref and package version.
- `rollback`: remove managed package files, refusing unmanaged files by default.

The mechanism must satisfy this contract:

1. Resolve a governance package version by git SHA.
2. Verify the target repo and execution scope before writes.
3. Support `dry-run`, `apply`, `verify`, and `rollback`.
4. Print the planned write set before apply.
5. Refuse unmanaged file overwrite by default.
6. Write the consumer record.
7. Prove idempotency with tests.
8. Prove rollback or uninstall with tests.

Example dry-run:

```bash
python3 scripts/overlord/deploy_governance_tooling.py dry-run \
  --target-repo /path/to/consumer-repo \
  --profile <profile> \
  --governance-ref "$(git rev-parse HEAD)"
```

Example apply and verify:

```bash
python3 scripts/overlord/deploy_governance_tooling.py apply \
  --target-repo /path/to/consumer-repo \
  --profile <profile> \
  --governance-ref "$(git rev-parse HEAD)"

python3 scripts/overlord/deploy_governance_tooling.py verify \
  --target-repo /path/to/consumer-repo \
  --profile <profile> \
  --governance-ref "$(git rev-parse HEAD)"
```

The deployer refuses dirty target repos and unmanaged managed-path files by default. The existing Local CI shim deployer remains the compatibility surface for rendering the managed shim body.

## Consumer Pull Verification

The first repo-pulled surface is non-mutating verification:

```bash
python3 scripts/overlord/verify_governance_consumer.py \
  --target-repo /path/to/consumer-repo \
  --profile <profile> \
  --governance-ref <exact-governance-sha>
```

The verifier reads the consumer repo's `.hldpro/governance-tooling.json`, checks that `governance_ref` is an exact 40-character git SHA, confirms the package version/profile, and verifies that expected managed files exist without escaping the repo root. For the managed Local CI shim, it also checks the governance marker and the pinned ref.

For SSOT bootstrap v0.2 records, the verifier remains report-only but also reports:

- unknown or missing repo profiles,
- mutable reusable workflow refs such as `@main`,
- managed hook/content checksum drift,
- managed files missing governance markers,
- missing or invalid local override metadata,
- missing profile constraints for HP, Seek, LAM, Stampede, and ASC profiles,
- observed local overrides in a separate `observed_overrides` JSON bucket.

This is the boundary between repo-pulled rules and centrally applied GitHub policy:

- Repo-pulled: consumer record, managed shim, Local CI profile, package-core verifier/evaluator logic, and PR-visible drift reporting.
- Centrally applied: org rulesets, repo rulesets, repository auto-merge settings, bypass actors, and required-status wiring.

Consumer verification must not mutate GitHub settings. If a consumer check detects central-policy drift, open or update issue-backed governance work and use the governed apply path. Do not let downstream repos silently self-rewrite rulesets or repository settings.

The desired-state contract for this first slice is `docs/governance-consumer-pull-state.json`.

## Verification Matrix

| Surface | Local verification | GitHub verification |
|---|---|---|
| Package manifest | `python3 -m json.tool docs/governance-tooling-package.json` | `validate` / Local CI Gate |
| Structured plans | `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .` | `governance-check.yml` |
| Execution scope | `python3 scripts/overlord/check_execution_environment.py --scope <scope> --changed-files-file <files>` | `governance-check.yml` planner-boundary |
| Local CI Gate | `python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json` | `local-ci-gate.yml` |
| Workflow coverage | `python3 scripts/overlord/check_workflow_local_coverage.py --root .` | `graphify-governance-contract.yml` and `local-ci-gate.yml` |
| Package deployer | `python3 scripts/overlord/test_deploy_governance_tooling.py` | `local-ci-gate.yml` when deployer paths change |
| Consumer pull verifier | `python3 scripts/overlord/test_verify_governance_consumer.py` | `local-ci-gate.yml` when verifier paths change |
| Shim deployer compatibility | `python3 scripts/overlord/test_deploy_local_ci_gate.py` | `local-ci-gate.yml` when deployer paths change |

When changed-file selection skips a check, the report must say whether it ran zero specs, a subset, or full coverage. A skipped local surface is not proof that CI will pass.

## Downstream Pilot Rule

`local-ai-machine` is the default pilot repo for the downstream adoption slice.

A different pilot may be selected only if the Phase 4 child issue proves one of these blockers:

- LAM cannot create a clean adoption worktree.
- LAM cannot run package deployment prerequisites.

The replacement repo must be named before deployment starts.

## Final Epic Gate

Issue #288 must remain open until the final e2e slice proves all of the following in a downstream repo:

- package pull from a pinned governance version
- managed deploy without manual copying
- deliberate blocker caught before push
- local pass after remediation
- GitHub Actions pass after push
- rollback or uninstall path tested or mechanically proven
- closeout links in both governance and the downstream repo

Documentation alone cannot satisfy the final AC.
