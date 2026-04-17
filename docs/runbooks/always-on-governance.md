# Always-On Governance Observer Runbook

## Purpose

The read-only observer generates per-repo governance health reports from existing local artifacts. It does not enqueue packets, dispatch workers, call models, or mutate governed repositories.

## Manual Run

From the governance repo root:

```bash
python3 scripts/orchestrator/read_only_observer.py
```

Dry-run summary without writing reports:

```bash
python3 scripts/orchestrator/read_only_observer.py --check-only
```

Default report outputs:

- `projects/hldpro-governance/reports/latest.json`
- `projects/hldpro-governance/reports/latest.md`
- `projects/ai-integration-services/reports/latest.json`
- `projects/healthcareplatform/reports/latest.json`
- `projects/local-ai-machine/reports/latest.json`
- `projects/knocktracker/reports/latest.json`
- `projects/asc-evaluator/reports/latest.json`

## launchd Install

This slice provides the plist template only. Install is an operator action:

```bash
mkdir -p ~/Library/LaunchAgents
sed "s#__REPO_ROOT__#$(pwd)#g" \
  launchd/com.hldpro.governance-observer.plist \
  > ~/Library/LaunchAgents/com.hldpro.governance-observer.plist
plutil -lint ~/Library/LaunchAgents/com.hldpro.governance-observer.plist
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.hldpro.governance-observer.plist
launchctl kickstart -k "gui/$(id -u)/com.hldpro.governance-observer"
```

The committed plist is a template. The install command replaces `__REPO_ROOT__` with the current checkout path. The template uses `RunAtLoad` and a 900-second interval, so it runs after reboot once the user launchd domain starts.

## Health Check

```bash
launchctl print "gui/$(id -u)/com.hldpro.governance-observer"
tail -n 50 projects/hldpro-governance/reports/observer.stdout.log
tail -n 50 projects/hldpro-governance/reports/observer.stderr.log
python3 scripts/orchestrator/read_only_observer.py --check-only
```

Confirm report freshness by checking `generated_at` in any `projects/<repo_slug>/reports/latest.json`.

## Kill / Disable SOP

Stop and unload:

```bash
launchctl bootout "gui/$(id -u)" ~/Library/LaunchAgents/com.hldpro.governance-observer.plist
```

Remove the local install:

```bash
rm -f ~/Library/LaunchAgents/com.hldpro.governance-observer.plist
```

Emergency process kill, if a process remains after bootout:

```bash
pkill -f "scripts/orchestrator/read_only_observer.py"
```

## Safety Contract

- Writes only to `projects/<repo_slug>/reports/` by default.
- Does not write to `raw/packets/`.
- Does not call model APIs or route work.
- Does not install itself.
- Uses local metadata-only raw issue feed files when present; issue bodies are not read or stored.
