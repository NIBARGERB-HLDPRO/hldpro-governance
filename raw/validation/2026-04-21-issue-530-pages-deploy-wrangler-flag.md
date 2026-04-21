# Issue #530 Pages Deploy Wrangler Flag Validation

## Gap

Wrangler 4.x rejects `wrangler pages deploy --non-interactive` with an unknown-argument error. The Pages deploy gate already sets `CI=true` for the child process, so the removed flag is unnecessary and blocks live deploy adoption.

## Change

- Removed `--non-interactive` from `scripts/pages-deploy/pages_deploy_gate.py`.
- Updated the focused deploy command test to assert `--non-interactive` is absent and `CI=true` remains present.
- Updated Pages deploy runbook and feature registry wording.

## Local Validation

Commands to run before merge:

```bash
/opt/homebrew/bin/pytest scripts/pages-deploy/tests/test_pages_deploy_gate.py
python3 scripts/overlord/validate_provisioning_evidence.py --root . --changed-files-file /tmp/issue-530-changed-files.txt
python3 scripts/overlord/validate_handoff_package.py raw/handoffs/2026-04-21-issue-530-pages-deploy-wrangler-flag.json --root .
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-530-pages-deploy-wrangler-flag-20260421 --changed-files-file /tmp/issue-530-changed-files.txt --enforce-governance-surface --enforce-planner-boundary-scope
python3 scripts/overlord/assert_execution_scope.py --scope raw/execution-scopes/2026-04-21-issue-530-pages-deploy-wrangler-flag-implementation.json --changed-files-file /tmp/issue-530-changed-files.txt --require-lane-claim
python3 scripts/overlord/validate_closeout.py raw/closeouts/2026-04-21-issue-530-pages-deploy-wrangler-flag.md --root .
tools/local-ci-gate/bin/hldpro-local-ci --profile hldpro-governance --changed-files-file /tmp/issue-530-changed-files.txt
```

Observed output on 2026-04-21:

- `/opt/homebrew/bin/pytest scripts/pages-deploy/tests/test_pages_deploy_gate.py` — `18 passed in 0.07s`
- `PASS provisioning evidence scan: 11 file(s)`
- `PASS validated 1 package handoff file(s)`
- `PASS validated 138 structured agent cycle plan file(s)`
- `PASS execution scope matches declared root, branch, write paths, and forbidden roots`
- `PASS closeout evidence validated: raw/closeouts/2026-04-21-issue-530-pages-deploy-wrangler-flag.md`
- `git diff --check` — PASS
- `Local CI Gate profile: hldpro-governance`
- `Verdict: PASS`
- `Summary: profile=hldpro-governance changed_files=11 source=file:/tmp/issue-530-changed-files.txt mode=live scope=subset total_checks=13 blockers=0 advisories=0 skipped=6 planned=0 verdict=pass.`
