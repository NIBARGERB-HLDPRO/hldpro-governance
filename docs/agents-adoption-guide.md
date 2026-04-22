# Governance Agents Adoption Guide
Last updated: 2026-04-22
Issue: [#559](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/559)

## Overview

hldpro-governance ships 9 Claude Code agents that automate governance workflows. Each agent has a YAML frontmatter pin (`name`, `description`, `model`, `tools`) and a defined trigger phrase set. The dispatcher (CLAUDE.md) routes to agents automatically — you never invoke agents by typing their filenames.

## Complete Agent Roster

| Agent | Trigger Phrases | Model | Purpose |
|-------|----------------|-------|---------|
| `overlord` | "check standards", "session start", "what's drifted" | haiku | Session-start standards drift check against STANDARDS.md |
| `overlord-sweep` | "run sweep", "weekly audit", "check all repos" | haiku | Weekly cross-repo audit: metrics, compliance, backlog alignment |
| `overlord-audit` | "deep audit", "analyze patterns", "PR recommendations" | claude-sonnet-4-6 | Deep pattern analysis: anti-pattern detection, PR recommendations |
| `verify-completion` | "verify done", "check artifacts", "mark complete" | haiku | Hard-gate completion verification before any DONE status update |
| `codex-brief` | "fire codex", "dispatch to spark", "write the brief", "brief issue #NNN" | haiku | Authors and validates Codex Spark dispatch briefs (all 5 prerequisites) |
| `som-worker-triage` | "triage packets", "process inbound", "what's in the queue", "route packets" | haiku | SoM packet triage: tier classification + Worker availability check |
| `issue-lane-bootstrap` | "start work on #NNN", "bootstrap issue", "claim lane", "set up issue lane" | haiku | Issue lane creation: worktree + branch + execution-scope skeleton |
| `sim-runner` | "run simulation", "test persona", "simulate slice", "run sim for" | claude-sonnet-4-6 | hldpro-sim invocation via CodexCliProvider + artifact write |
| `backlog-promoter` | "promote codex findings", "review ingestion", "promote to progress", "process backlog findings" | claude-sonnet-4-6 | HITL CODEX-FLAGGED finding promotion to PROGRESS.md or FAIL_FAST_LOG.md |

## Installing Agents Globally

To use governance agents in any repo session (not just hldpro-governance):

```bash
# Copy all governance agents to your global Claude agents directory
cp /Users/bennibarger/Developer/HLDPRO/hldpro-governance/agents/*.md ~/.claude/agents/
```

Or install symlinks for live updates:
```bash
for f in /Users/bennibarger/Developer/HLDPRO/hldpro-governance/agents/*.md; do
  ln -sf "$f" ~/.claude/agents/$(basename "$f")
done
```

Verify installation:
```bash
ls ~/.claude/agents/
```

## Per-Repo Configuration Checklist

For each governance agent to work correctly in a repo, the following infrastructure must exist:

### All Agents
- [ ] `CLAUDE.md` — routing table with agent trigger phrases
- [ ] GitHub issue open for any active work lane (`issue-N-*` branch)
- [ ] Branch named `issue-<N>-<slug>-YYYYMMDD` or `riskfix/<slug>-YYYYMMDD`

### `overlord`, `overlord-sweep`, `overlord-audit`
- [ ] `STANDARDS.md` — or pointer to governance STANDARDS.md
- [ ] `docs/PROGRESS.md` — backlog-labeled issues tracked
- [ ] `docs/FAIL_FAST_LOG.md` — error patterns tracked
- [ ] `graphify-out/<repo>/GRAPH_REPORT.md` — graph output present

### `verify-completion`
- [ ] `raw/closeouts/` directory exists
- [ ] `hooks/closeout-hook.sh` is executable
- [ ] Structured plan JSON passes `validate_structured_agent_cycle_plan.py`

### `codex-brief`
- [ ] `scripts/codex-preflight.sh` exists and is executable
- [ ] `docs/templates/codex-spark-dispatch-brief.md` exists (installed by PR #417)
- [ ] `raw/packets/inbound/` directory exists
- [ ] `codex` CLI is in PATH

### `som-worker-triage`
- [ ] `STANDARDS.md §Society of Minds` present (routing table)
- [ ] `raw/packets/inbound/` directory exists
- [ ] `scripts/codex-preflight.sh` exists (for Tier 2 availability check)
- [ ] `raw/windows-ollama/` directory exists (for Windows Ollama heartbeat check)
- [ ] `raw/lam/` directory exists (for LAM fleet status check)

### `issue-lane-bootstrap`
- [ ] `gh` CLI authenticated (`gh auth status`)
- [ ] `git` configured with user.name and user.email
- [ ] `raw/execution-scopes/` directory exists
- [ ] `HLDPRO_LANE_CLAIM_BOOTSTRAP=1` environment variable support (no config needed — used as prefix on git command)

### `sim-runner`

#### Installation (required before first run)

Canonical install via the governance deployer:
```bash
bash <governance-root>/scripts/deployer/deploy-hldpro-sim.sh <consumer-repo-path>
```

The deployer:
- Installs the `hldpro-sim` package (pip-editable, with directory-copy fallback)
- Deploys managed personas to `sim-personas/shared/` — **commit this directory**
- Writes `.hldpro/hldpro-sim.json` (consumer record) — **commit this file**

Verify install: check `.hldpro/hldpro-sim.json` exists and `pinned_sha` matches the value in `docs/hldpro-sim-consumer-pull-state.json` in hldpro-governance.

#### Checklist
- [ ] `hldpro-sim` deployed via deployer: `.hldpro/hldpro-sim.json` present in consumer repo root
- [ ] `codex` CLI in PATH
- [ ] `raw/packets/outbound/` directory exists
- [ ] Persona files in `sim-personas/local/` (local overrides) or `sim-personas/shared/` (deployer-managed)
- [ ] Outcome schema JSON prepared with `additionalProperties: false`

### `backlog-promoter`
- [ ] `~/.codex-ingestion/<repo>/backlog-*.md` files exist (populated by codex-ingestion workflow)
- [ ] `docs/PROGRESS.md` and `docs/FAIL_FAST_LOG.md` exist in target repos
- [ ] Operator is present (HITL agent — requires live session)

## Integration with Local CI Gate

The Local CI Gate (`scripts/run_local_ci_gate.sh`) validates governance surface writes, including:
- Structured plan JSON schema validation (`validate_structured_agent_cycle_plan.py`)
- Execution scope boundary checking (`assert_execution_scope.py`)
- Backlog/GitHub issue alignment (`check_overlord_backlog_github_alignment.py`)

Agents that write to governance surfaces (agents/, docs/plans/, raw/) must operate within an accepted execution scope. The `issue-lane-bootstrap` agent creates the execution scope skeleton; the operator or planner must set `execution_mode` to `implementation_ready` before implementation writes are allowed.

## Routing Example Session

```
User: bootstrap issue #560
→ Dispatcher routes to: issue-lane-bootstrap
→ Agent: reads GH issue, creates worktree, writes execution-scope skeleton

User: write the brief for issue #560
→ Dispatcher routes to: codex-brief
→ Agent: runs preflight, confirms plan, authors brief to raw/packets/inbound/

User: triage packets
→ Dispatcher routes to: som-worker-triage
→ Agent: reads inbound queue, classifies by tier, checks Worker availability

User: verify done
→ Dispatcher routes to: verify-completion
→ Agent: checks all artifacts exist and pass gates before DONE update
```
