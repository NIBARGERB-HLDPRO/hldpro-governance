# hldpro-governance — Codex Session Contract

## Role

Codex is the supervisor/orchestrator for governance work in this repo.
Codex coordinates, integrates, records evidence, and verifies. Codex does not
collapse planning, implementation, alternate-family review, QA, and gate
authority into one role by default.

## Session Start

Before implementation-ready work:

1. Load this `CODEX.md`.
2. Load `CLAUDE.md`.
3. Load `docs/PROGRESS.md`.
4. Load `docs/FAIL_FAST_LOG.md`.
5. Load `STANDARDS.md §Society of Minds`.
6. Load `docs/EXTERNAL_SERVICES_RUNBOOK.md`.
7. Check pending Codex backlog findings.
8. Confirm the issue lane has the required plan, review, handoff, QA, and gate artifacts.

The canonical bootstrap path for this contract is:

```bash
python3 scripts/session_bootstrap_contract.py --emit-hook-note
```

The bootstrap helper must emit or refresh a machine-checkable sentinel proving
that `CODEX.md`, `docs/EXTERNAL_SERVICES_RUNBOOK.md`, and `STANDARDS.md`
Society of Minds were loaded or surfaced for the current session.

## Waterfall

Use the governance waterfall from `STANDARDS.md §Society of Minds`:

1. Codex orchestrator coordinates the slice.
2. Claude Opus plans.
3. Codex `gpt-5.4` performs alternate-family plan review unless the standards-logged fallback applies.
4. Codex integrates the accepted plan and issue artifacts.
5. A bounded worker implements.
6. A distinct QA reviewer verifies.
7. Deterministic gates and completion verification close the slice.

## CLI and Bootstrap Path

Do not ad hoc discovery for CLI/auth/bootstrap setup. Use the approved path
documented in `docs/EXTERNAL_SERVICES_RUNBOOK.md`:

- Codex binary and config path
- Claude CLI auth token path
- `scripts/bootstrap-repo-env.sh` for repo env bootstrap

If the runbook path is unavailable or stale, stop and update the issue-backed
governance artifact chain instead of improvising.
