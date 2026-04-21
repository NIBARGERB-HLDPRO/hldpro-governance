# PDCAR: Issue #430 Seek and Stampede Env Bootstrap

Date: 2026-04-21
Branch: `feature/issue-430-env-bootstrap-seek-stampede-20260421`
Issue: [#430](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/430)

## Plan

Extend the governance `.env.shared` bootstrap so `seek-and-ponder` and `Stampede` have repo-native targets. Keep generated env files local and gitignored; commit only key-name mappings, docs, tests, and no-secret validation.

Acceptance criteria:

- `seek`, `seek-local`, and `seek-worktree` aliases are supported.
- `stampede` emits the repo-native market-data key set expected by Stampede `.env.example`.
- Dry-run output remains redacted.
- Isolated governance worktrees under `HLDPRO/var/worktrees` can discover the primary `.env.shared`.
- Focused contract tests, Local CI, and GitHub PR checks pass.

## Do

1. Add missing aliases and Stampede target to `scripts/bootstrap-repo-env.sh`.
2. Extend `scripts/test_bootstrap_repo_env_contract.py` with synthetic redaction and worktree discovery coverage.
3. Ignore Python bytecode/cache residue created by local validation.
4. Update `docs/ENV_REGISTRY.md`, `docs/PROGRESS.md`, and `OVERLORD_BACKLOG.md`.
5. Record validation in `raw/validation/2026-04-21-issue-430-env-bootstrap-seek-stampede.md`.

## Check

- Shell syntax must pass.
- Bootstrap contract tests must pass.
- Redacted dry-run checks for `seek`, `seek-local`, and `stampede` must pass.
- Local CI must pass before publication.

## Adjust

If a target requires live credentials that are absent from `.env.shared`, generate blank optional keys and document the missing credential rather than inventing values or copying credentials from another repo.

## Review

Review must confirm no downstream repo files, `.env.shared`, generated `.env` files, or real secret values are committed.
