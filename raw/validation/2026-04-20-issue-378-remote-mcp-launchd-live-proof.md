# Issue #378 Validation: Remote MCP Launchd Live Proof

Date: 2026-04-20
Branch: `issue-378-remote-mcp-launchd-live-proof-20260420`
Issue: [#378](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/378)

## Decision

The selected local launchd monitor surface now invokes `scripts/remote-mcp/live_health_monitor.py --mode live`. This prevents the live-authoritative surface from silently falling back to fixture mode when live inputs are absent.

Production live health is not claimed in this slice because production credentials and copied audit evidence were intentionally unavailable to the repo. The preserved live proof is the expected fail-closed behavior.

## Acceptance Criteria

| AC | Result | Evidence |
|---|---|---|
| Backlog/progress mirrors track #378 as active before implementation | PASS | `OVERLORD_BACKLOG.md`; `docs/PROGRESS.md` |
| Runbook documents launchd live proof sequence, evidence capture, rollback, and no-secrets artifact policy | PASS | `docs/runbooks/remote-mcp-bridge.md` |
| Launchd plist render/lint proof is preserved | PASS | `raw/remote-mcp-launchd-live-proof/2026-04-20.com.hldpro.remote-mcp-monitor.rendered.plist`; `2026-04-20.rendered-plutil.txt` |
| Selected-mode monitor rehearsal and alert artifact are preserved | PASS | `2026-04-20.launchd-rehearsal.monitor.json`; `2026-04-20.launchd-rehearsal.alert.json`; `2026-04-20.launchd-rehearsal.alert.md` |
| Live mode missing-config proof fails closed before requests | PASS | `2026-04-20.live-missing-config.proof.json`; exit code `2` |
| Evidence scan finds no sensitive material | PASS | `rg` denylist scan returned no matches |
| Local tests and Local CI Gate pass | PASS | Focused pytest suite: `18 passed`; Local CI Gate verdict: `PASS` |
| Final AC: GitHub PR checks pass before closeout | PASS | PR #379 checks passed: Analyze (actions), Analyze (python), CodeQL, commit-scope, contract, local-ci-gate, and validate |

## Commands

```bash
plutil -lint launchd/com.hldpro.remote-mcp-monitor.plist
plutil -lint raw/remote-mcp-launchd-live-proof/2026-04-20.com.hldpro.remote-mcp-monitor.rendered.plist
rg -n "<string>live</string>" launchd/com.hldpro.remote-mcp-monitor.plist raw/remote-mcp-launchd-live-proof/2026-04-20.com.hldpro.remote-mcp-monitor.rendered.plist
```

Result: PASS. Both plist files linted and both contain the `live` mode argument.

```bash
python3 scripts/remote-mcp/live_health_monitor.py \
  --mode fixture \
  --fixture-evidence-dir /tmp/issue378-remote-mcp-monitor-fixture \
  --json \
  > raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.monitor.json
```

Result: PASS.

```bash
python3 scripts/remote-mcp/monitor_alert.py \
  --input raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.monitor.json \
  --json-output raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.alert.json \
  --markdown-output raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.alert.md \
  --fail-on-degraded
```

Result: PASS. Alert health: `healthy`; sensitive findings: `0`.

```bash
env -i PATH="$PATH" python3 scripts/remote-mcp/live_health_monitor.py --mode live --json
```

Result: PASS as fail-closed proof. Exit code `2`; stderr lists missing configuration names only.

```bash
python3 -m pytest \
  scripts/remote-mcp/tests/test_verify_audit.py \
  scripts/remote-mcp/tests/test_stage_d_smoke.py \
  scripts/remote-mcp/tests/test_live_health_monitor.py \
  scripts/remote-mcp/tests/test_monitor_alert.py \
  scripts/som-client/tests/test_som_client.py
```

Result: PASS, `18 passed in 1.54s`.

```bash
python3 -m py_compile \
  scripts/remote-mcp/verify_audit.py \
  scripts/remote-mcp/stage_d_smoke.py \
  scripts/remote-mcp/live_health_monitor.py \
  scripts/remote-mcp/monitor_alert.py \
  scripts/som-client/som_client.py
```

Result: PASS.

```bash
python3 -m json.tool docs/plans/issue-378-remote-mcp-launchd-live-proof-structured-agent-cycle-plan.json
python3 -m json.tool raw/execution-scopes/2026-04-20-issue-378-remote-mcp-launchd-live-proof-implementation.json
python3 -m json.tool raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-live-proof.json
python3 -m json.tool raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.monitor.json
python3 -m json.tool raw/remote-mcp-launchd-live-proof/2026-04-20.launchd-rehearsal.alert.json
python3 -m json.tool raw/remote-mcp-launchd-live-proof/2026-04-20.live-missing-config.proof.json
```

Result: PASS.

```bash
rg -n "123-45-6789|Bearer\s+[A-Za-z0-9._~+/=-]{10,}|CF-Access|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}" raw/remote-mcp-launchd-live-proof || true
```

Result: PASS, no matches.

```bash
python3 scripts/overlord/validate_structured_agent_cycle_plan.py \
  --root . \
  --branch-name issue-378-remote-mcp-launchd-live-proof-20260420 \
  --changed-files-file /tmp/issue378-changed-files.txt \
  --enforce-governance-surface
```

Result: PASS, `validated 82 structured agent cycle plan file(s)`.

```bash
python3 scripts/overlord/assert_execution_scope.py \
  --scope raw/execution-scopes/2026-04-20-issue-378-remote-mcp-launchd-live-proof-implementation.json \
  --changed-files-file /tmp/issue378-changed-files.txt
```

Result: PASS. Warnings were limited to declared active parallel roots outside this issue worktree.

```bash
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
python3 scripts/overlord/validate_registry_surfaces.py
git diff --check
```

Result: PASS.

```bash
tools/local-ci-gate/bin/hldpro-local-ci run --profile hldpro-governance --json
```

Result: PASS. Verdict: `PASS`.

```bash
gh pr checks 379 --watch --interval 10
```

Result: PASS. Checks passed: Analyze (actions), Analyze (python), CodeQL, commit-scope, contract, local-ci-gate, and validate.

## Residual Risk

Production launchd live health is not claimed because live configuration and copied audit evidence were unavailable. The launchd template is now live fail-closed, and the runbook documents the production operator setup and rollback path.
