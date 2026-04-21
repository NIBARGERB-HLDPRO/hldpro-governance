# Issue #430 Validation: Seek and Stampede Env Bootstrap Targets

Issue: [#430](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/430)
Branch: `feature/issue-430-env-bootstrap-seek-stampede-20260421`

## Scope

Add repo-native SSOT bootstrap coverage for `seek-and-ponder` and `Stampede` without editing either downstream repo.

## Acceptance Criteria

- `bootstrap-repo-env.sh seek` writes the default Seek staging `.env` target.
- `bootstrap-repo-env.sh seek-local` writes the default Seek local Supabase `.env` target.
- `bootstrap-repo-env.sh seek-worktree <target>` supports explicit worktree targets.
- `bootstrap-repo-env.sh stampede` writes the default Stampede `.env` target.
- Dry-run previews remain redacted.
- `docs/ENV_REGISTRY.md`, `docs/PROGRESS.md`, and `OVERLORD_BACKLOG.md` document the lane and mappings.

## Validation

Passed local validation:

- `bash -n scripts/bootstrap-repo-env.sh`
- `python3 scripts/test_bootstrap_repo_env_contract.py`
- `DRY_RUN=1 bash scripts/bootstrap-repo-env.sh seek /tmp/seek.env`
- `DRY_RUN=1 bash scripts/bootstrap-repo-env.sh seek-local /tmp/seek-local.env`
- `DRY_RUN=1 bash scripts/bootstrap-repo-env.sh stampede /tmp/stampede.env`
- `tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance`

Local CI result: PASS.
