# Local CI Gate Toolkit Runbook

## Purpose

`hldpro-governance` owns the reusable Local CI Gate toolkit. Governed repos should use a thin managed shim that delegates back to this checkout instead of copying local-check logic into each repo.

CI remains authoritative. The local gate is an upstream filter for preventable failures before push; a local pass is not a full CI replay.

## Runner

Run the governance profile from this repo root:

```bash
python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance
```

Preview checks without executing them:

```bash
python3 tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --dry-run
```

Use explicit changed files for a narrow check:

```bash
python3 tools/local-ci-gate/bin/hldpro-local-ci run \
  --profile hldpro-governance \
  --changed-file tools/local-ci-gate/local_ci_gate.py \
  --changed-file scripts/overlord/deploy_local_ci_gate.py
```

Reports are local-only by default under `cache/local-ci-gate/reports/`, which is ignored by the repo root `.gitignore`.

## Profile Catalog

| Profile | Intended repo | Required local dependencies | Notes |
|---------|---------------|-----------------------------|-------|
| `hldpro-governance` | `hldpro-governance` | `python3`, `git` | Runs deterministic governance checks, planner-boundary checks, diff hygiene, and focused toolkit tests. |
| `knocktracker` | `knocktracker` | `npm` | Adopted by knocktracker issue #173 / PR #174 as the live managed-shim profile. |
| `ai-integration-services` | `ai-integration-services` | `npm` | Governance profile is available; consumer shim rollout is tracked separately by ai-integration-services issue #1113. |

Profiles declare their dependency metadata in `profile.requires_dependencies`. The runner validates that metadata shape and rejects duplicate check IDs at profile-load time. Dependency metadata is descriptive; each command still fails normally if the target repo has not installed its own dependencies.

## Governance Profile

The initial profile is `tools/local-ci-gate/profiles/hldpro-governance.yml`.

It runs or plans:

- Overlord backlog issue alignment.
- Structured agent cycle plan validation.
- Governance-surface planning gate when governance paths changed.
- Planner-boundary execution-scope assertion when planner-boundary paths changed.
- `git diff --check`.
- Focused Local CI Gate tests when `tools/local-ci-gate/` changed.

The runner continues through all checks it can run and exits non-zero only for blocker failures. Advisory failures are reported but do not block by default.

## Knocktracker Profile

The consumer profile is `tools/local-ci-gate/profiles/knocktracker.yml`.

It runs existing knocktracker commands only:

- Always-on: `npm run brand:verify`, `npm run lint`, `npm run typecheck`, and `npm run file-index:check`.
- Changed-file scoped: `npm run test:routing`, `npm run test:track-logic`, `npm run test:contracts`, `npm run test:manager-dashboard`, and `npm run build:web`.

Use the profile from a knocktracker checkout:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/knocktracker \
  --profile knocktracker
```

Preview without executing npm commands:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/knocktracker \
  --profile knocktracker \
  --dry-run
```

The current knocktracker dry-run shim can move to live enforcement after the governance profile lands by switching `--profile hldpro-governance --dry-run` to `--profile knocktracker`. That consumer edit must happen in a separate knocktracker issue-backed PR.

## AI Integration Services Profile

The second consumer profile is `tools/local-ci-gate/profiles/ai-integration-services.yml`.

It runs existing AIS commands only:

- Always-on: `npm run typecheck`.
- Changed-file scoped blocker builds: `npm run build:dashboard`, `npm run build:marketing`, `npm run build:reseller`, and `npm run build:pwa`.
- Changed-file scoped advisory checks: `npm run audit:error-handlers`, `npm run preflight`, and `npm run smoke`.

Use the profile from an AIS checkout:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/ai-integration-services \
  --profile ai-integration-services
```

Preview without executing npm commands:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/ai-integration-services \
  --profile ai-integration-services \
  --dry-run
```

An AIS managed shim rollout must happen in a separate AIS issue-backed PR after the governance profile lands.

## Managed Shim Deployer

Preview a shim install:

```bash
python3 scripts/overlord/deploy_local_ci_gate.py dry-run \
  --target-repo /path/to/consumer-repo \
  --profile hldpro-governance \
  --governance-ref "$(git rev-parse HEAD)"
```

Install the default shim:

```bash
python3 scripts/overlord/deploy_local_ci_gate.py install \
  --target-repo /path/to/consumer-repo \
  --profile hldpro-governance \
  --governance-ref "$(git rev-parse HEAD)"
```

Refresh an existing managed shim:

```bash
python3 scripts/overlord/deploy_local_ci_gate.py refresh \
  --target-repo /path/to/consumer-repo \
  --profile hldpro-governance \
  --governance-ref "$(git rev-parse HEAD)"
```

Managed shims embed the governance checkout path used at install time, but operators can override that root without editing the consumer repo:

```bash
HLDPRO_GOVERNANCE_ROOT=/path/to/hldpro-governance .hldpro/local-ci.sh
```

The generated shim resolves:

1. `HLDPRO_GOVERNANCE_ROOT` when set.
2. The embedded install-time governance root otherwise.

The runner invocation records the resolved governance root with `--governance-root`, so local reports keep showing which governance checkout supplied the profile and runner.

## Safety Contract

- Managed shim marker: `# hldpro-governance local-ci gate managed`.
- Valid shim paths: `.hldpro/local-ci.sh` or `.governance/local-ci.sh` under the target repo root.
- Existing unmanaged shims are refused by default.
- `--backup-existing` renames an unmanaged shim to `local-ci.sh.pre-local-ci-gate` before install.
- `--force` overwrites an unmanaged shim only when explicitly passed.
- `resolve` and `dry-run` print the target repo, profile, shim path, governance source/ref, command preview, and planned write set before install.
- Generated shims honor `HLDPRO_GOVERNANCE_ROOT` as an operator override and fall back to the embedded root.

## Consumer Rollout

Consumer rollout remains separate issue-backed work. Do not install shims in downstream repos from the governance implementation PR.
