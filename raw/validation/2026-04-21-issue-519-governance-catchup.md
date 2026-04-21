# Issue #519 Governance Catch-Up Validation

## Gap

Issue #519 tracked three loose governance cleanup items:

- Stampede issue #111 Stage 6 closeout evidence.
- The Codex Fire fail-fast row from issue #469.
- Three duplicate graphify wiki paths that collide with canonical uppercase wiki pages on case-insensitive macOS filesystems.

## Change

- Confirmed `origin/main` already tracks `raw/closeouts/2026-04-21-stampede-issue-111-permanent-services.md`.
- Confirmed `origin/main` already tracks `raw/fail-fast-log.md` with the `2026-04-21 13:13` `gpt-5.4` preflight timeout row.
- Confirmed `origin/main` already has the `OVERLORD_BACKLOG.md` Done row for Stampede issue #111 / governance issue #494.
- Removed these duplicate wiki collision paths from git tracking:
  - `wiki/healthcareplatform/Training_assignments.md`
  - `wiki/hldpro/Repos_Ai_integration.md`
  - `wiki/hldpro/Repos_Healthcare_platform.md`
- Added issue #519 governance evidence and backlog Done tracking.

## Local Validation

Commands to run before merge:

```bash
git diff --name-only origin/main...HEAD > /tmp/issue-519-changed-files.txt
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-519-governance-catchup-20260421 --changed-files-file /tmp/issue-519-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-519-governance-catchup-implementation.json --changed-files-file /tmp/issue-519-changed-files.txt --require-lane-claim
tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance --changed-files-file /tmp/issue-519-changed-files.txt
./hooks/governance-check.sh
```

Observed output on 2026-04-21:

- `PASS validated 132 structured agent cycle plan file(s)`
- `PASS execution scope matches declared root, branch, write paths, and forbidden roots`
- `Governance check PASS`
- `Local CI Gate profile: hldpro-governance`
- `Verdict: PASS`
- `Summary: profile=hldpro-governance changed_files=8 source=file:/tmp/issue-519-changed-files.txt mode=live scope=subset total_checks=12 blockers=0 advisories=0 skipped=6 planned=0 verdict=pass.`
