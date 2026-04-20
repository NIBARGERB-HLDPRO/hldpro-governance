# Issue #376 Validation: Remote MCP Monitor Operating Mode

Date: 2026-04-20
Branch: `issue-376-remote-mcp-monitor-operating-mode-20260420`
Issue: [#376](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/376)

## Decision

Selected live operating mode: local `launchd` using `launchd/com.hldpro.remote-mcp-monitor.plist`.

GitHub Actions remains the scheduled fixture harness and optional configured-live runner. Fixture evidence is not production live health.

## Acceptance Criteria

| AC | Result | Evidence |
|---|---|---|
| Operating mode is explicitly selected and justified | PASS | `docs/runbooks/remote-mcp-bridge.md`; `raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-decision.json` |
| Runbook documents setup, evidence capture, and operator response | PASS | `docs/runbooks/remote-mcp-bridge.md` |
| Payload-safe monitor alert artifact is preserved | PASS | `raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.alert.json`; `raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.alert.md` |
| Live mode fails closed when required production configuration is absent | PASS | `raw/remote-mcp-monitor-operating-mode/2026-04-20.live-missing-config.proof.json`; exit code `2` |
| Evidence scan finds no sensitive material | PASS | `rg` denylist scan returned no matches |
| Local tests and Local CI Gate pass | PASS | Focused pytest suite: `18 passed`; Local CI Gate verdict: `PASS` |
| Final AC: GitHub PR checks pass before closeout | PASS | PR #377 checks passed: Analyze (actions), Analyze (python), CodeQL, commit-scope, contract, local-ci-gate, and validate |

## Commands

```bash
python3 scripts/remote-mcp/live_health_monitor.py \
  --mode fixture \
  --fixture-evidence-dir /tmp/issue376-remote-mcp-monitor-fixture \
  --json \
  > raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.monitor.json
```

Result: PASS.

```bash
python3 scripts/remote-mcp/monitor_alert.py \
  --input raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.monitor.json \
  --json-output raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.alert.json \
  --markdown-output raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.alert.md \
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

Result: PASS, `18 passed in 1.52s`.

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
python3 -m json.tool docs/plans/issue-376-remote-mcp-monitor-operating-mode-structured-agent-cycle-plan.json
python3 -m json.tool raw/execution-scopes/2026-04-20-issue-376-remote-mcp-monitor-operating-mode-implementation.json
python3 -m json.tool raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-decision.json
python3 -m json.tool raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.monitor.json
python3 -m json.tool raw/remote-mcp-monitor-operating-mode/2026-04-20.local-launchd-rehearsal.alert.json
python3 -m json.tool raw/remote-mcp-monitor-operating-mode/2026-04-20.live-missing-config.proof.json
```

Result: PASS.

```bash
rg -n "123-45-6789|Bearer\s+[A-Za-z0-9._~+/=-]{10,}|CF-Access|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}" raw/remote-mcp-monitor-operating-mode || true
```

Result: PASS, no matches.

```bash
plutil -lint launchd/com.hldpro.remote-mcp-monitor.plist
```

Result: PASS, `OK`.

```bash
python3 scripts/overlord/validate_structured_agent_cycle_plan.py \
  --root . \
  --branch-name issue-376-remote-mcp-monitor-operating-mode-20260420 \
  --changed-files-file /tmp/issue376-changed-files.txt \
  --enforce-governance-surface
```

Result: PASS, `validated 81 structured agent cycle plan file(s)`.

```bash
python3 scripts/overlord/assert_execution_scope.py \
  --scope raw/execution-scopes/2026-04-20-issue-376-remote-mcp-monitor-operating-mode-implementation.json \
  --changed-files-file /tmp/issue376-changed-files.txt
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
gh pr checks 377 --watch --interval 10
```

Result: PASS. Checks passed: Analyze (actions), Analyze (python), CodeQL, commit-scope, contract, local-ci-gate, and validate.

## Residual Risk

Production live recurring health is not claimed in this slice because live credentials and copied production audit evidence were intentionally not available in the repo. Future live evidence must run through the selected local launchd surface or an explicitly configured equivalent and remain issue-backed.
