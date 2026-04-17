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

## Safety Contract

- Managed shim marker: `# hldpro-governance local-ci gate managed`.
- Valid shim paths: `.hldpro/local-ci.sh` or `.governance/local-ci.sh` under the target repo root.
- Existing unmanaged shims are refused by default.
- `--backup-existing` renames an unmanaged shim to `local-ci.sh.pre-local-ci-gate` before install.
- `--force` overwrites an unmanaged shim only when explicitly passed.
- `resolve` and `dry-run` print the target repo, profile, shim path, governance source/ref, command preview, and planned write set before install.

## Consumer Rollout

Consumer rollout remains separate issue-backed work. Do not install shims in downstream repos from the governance implementation PR.
