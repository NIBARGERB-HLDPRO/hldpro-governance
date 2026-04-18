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
| `local-ai-machine` | `local-ai-machine` | `python3`, `deno`, `bash` | Governance profile is available; consumer shim rollout must happen separately in local-ai-machine. |

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

## Local AI Machine Profile

The LAM consumer profile is `tools/local-ci-gate/profiles/local-ai-machine.yml`.

It runs existing LAM commands only:

- Always-on static governance contracts: agent governance, env-var docs, clean-branch governance, and fail-fast governance.
- Changed-file scoped blocker checks: required-check reconciliation, PR routing, edge critic reference, MicroVM boot command, inference router, and critic runner contracts.
- Changed-file scoped advisory check: Deno durable workflow test for workflow/orchestrator changes.

Use the profile from a LAM checkout:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/local-ai-machine \
  --profile local-ai-machine
```

Preview without executing LAM commands:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/local-ai-machine \
  --profile local-ai-machine \
  --dry-run
```

LAM currently uses direct Python, Deno, and bash workflow commands rather than `package.json` scripts. Do not add wrapper scripts in governance; if LAM needs wrapper commands, create a separate LAM issue-backed PR.

LAM managed shim rollout must happen in a separate LAM issue-backed PR after the governance profile lands.

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

Managed shims embed only the governance checkout path used at install time. They do not embed the consumer repo root or the installed shim path. At runtime, the shim resolves its own path and asks git for the target repo root, so copied or moved checkouts report the live checkout instead of the original deploy target.

Operators can override the governance root without editing the consumer repo:

```bash
HLDPRO_GOVERNANCE_ROOT=/path/to/hldpro-governance .hldpro/local-ci.sh
```

The generated shim resolves:

1. `HLDPRO_GOVERNANCE_ROOT` when set.
2. The embedded install-time governance root otherwise.
3. The target repo root from `git rev-parse --show-toplevel` at the live shim location.
4. The shim path from `BASH_SOURCE[0]` at invocation time.

The runner invocation records the resolved governance root, governance ref, shim path, argv, cwd, and runner path in JSON reports, so local evidence shows which governance checkout supplied the profile and runner.

## Enforcement Taxonomy

Use these labels when discussing rollout status:

| Status | Meaning | Merge claim allowed |
|--------|---------|---------------------|
| Profile available | A governance-owned profile exists and loads in `hldpro-governance`. | The repo has a reusable check definition only. |
| Shim installed | A consumer repo has a managed `.hldpro/local-ci.sh` or `.governance/local-ci.sh`. | The repo can invoke the governance runner through the shim. |
| Manual local live gate | Operators run the installed shim manually and blocker failures exit non-zero. | Manual local enforcement works when invoked. |
| Pre-push hook gate | The consumer repo wires the shim into a local pre-push hook or equivalent repo-local hook. | Local push attempts are filtered on machines with hooks installed. |
| CI required gate | Branch protection, rulesets, or workflow status checks require the gate or an equivalent CI check before merge. | Repository-level enforcement is mandatory for protected branches. |

Do not collapse these states. A dry-run is mapping evidence only. A live manual shim run is not proof of pre-push hook wiring. A local hook is not proof of GitHub branch-protection or ruleset enforcement. CI remains authoritative.

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

Use this checklist for each consumer repo:

1. Create a consumer-repo GitHub issue before editing files.
2. Confirm the consumer repo is not already owned by another active lane.
3. Create an isolated clean worktree or branch for the consumer rollout.
4. Run the deployer in `dry-run` mode from this governance checkout and record the planned write set:

```bash
python3 scripts/overlord/deploy_local_ci_gate.py dry-run \
  --target-repo /path/to/consumer-repo \
  --profile <profile-name> \
  --governance-ref "$(git rev-parse HEAD)"
```

5. Install or refresh only the managed shim path, normally `.hldpro/local-ci.sh`:

```bash
python3 scripts/overlord/deploy_local_ci_gate.py install \
  --target-repo /path/to/consumer-repo \
  --profile <profile-name> \
  --governance-ref "$(git rev-parse HEAD)"
```

6. Add `cache/local-ci-gate/reports/` to the consumer repo `.gitignore` if it is not already ignored.
7. Run the consumer profile in dry-run mode before installing or refreshing live enforcement:

```bash
python3 /path/to/hldpro-governance/tools/local-ci-gate/bin/hldpro-local-ci run \
  --repo-root /path/to/consumer-repo \
  --profile <profile-name> \
  --dry-run
```

8. Run the installed shim live only when the repo lane owner confirms the local dependency state is ready:

```bash
.hldpro/local-ci.sh
```

9. Open a consumer-repo PR that includes only the shim, ignore-rule, and any repo-local usage note required by that repo.
10. Merge only after required CI is green; CI remains authoritative.
