# PDCAR — Issue #559: Add Five Governance Agents
Date: 2026-04-22
Branch: issue-559-five-new-agents-20260422
Structured Plan: docs/plans/issue-559-five-new-agents-structured-agent-cycle-plan.json

## Problem

The hldpro-governance dispatcher (CLAUDE.md) routes only 4 tasks to dedicated agents: standards drift check, weekly audit, deep pattern analysis, and completion verification. Five high-frequency, high-complexity governance workflows are currently performed ad hoc by the dispatcher session, violating the "NEVER RESPOND DIRECTLY" rule:

1. **Codex Spark dispatch briefs** — operators ask "fire codex on issue #N" and the dispatcher manually encodes all 5 prerequisites each time, with inconsistent results.
2. **SoM packet triage** — `raw/packets/inbound/` accumulates packets without systematic tier classification or Worker availability checking.
3. **Issue lane bootstrapping** — each new issue lane requires manually creating worktrees, deriving branch names per policy, and writing execution-scope skeletons.
4. **hldpro-sim invocation** — operators ask to run simulations but the invocation pattern (CodexCliProvider-only, persona resolution, artifact schema) is not documented in a single agent.
5. **Codex ingestion promotion** — CODEX-FLAGGED findings in `.codex-ingestion/*/backlog-*.md` accumulate without a HITL review path.

## Design

Five agent files in `agents/`, each with YAML frontmatter (`name`, `description`, `model`, `tools`) per §DA schema.

**codex-brief (haiku):** Seven-step procedure encoding all 5 dispatch prerequisites: quota preflight → issue context → worktree creation → execution-scope confirmation → structured-plan confirmation → brief authoring from template → report. Read-only except for `raw/packets/inbound/`.

**som-worker-triage (haiku):** Five-step triage: list packets → classify by tier using SoM routing table → check Worker availability (codex-spark, Windows Ollama, LAM fleet) → emit triage table → recommend next action. Read-only, never fires Workers directly.

**issue-lane-bootstrap (haiku):** Six-step bootstrap: read issue → derive branch per lane policy → create worktree with `HLDPRO_LANE_CLAIM_BOOTSTRAP=1` → verify clean log → write execution-scope skeleton → report. Writes only to `raw/execution-scopes/`.

**sim-runner (claude-sonnet-4-6):** Six-step invocation: confirm hldpro-sim installed → confirm codex in PATH → resolve persona (local-first/shared fallback) → build invocation pattern → write artifacts to `raw/packets/outbound/` → report. CodexCliProvider only; AnthropicApiProvider explicitly excluded.

**backlog-promoter (claude-sonnet-4-6):** Five-step HITL promotion: scan CODEX-FLAGGED findings → present with file:line evidence → ask operator for per-finding decision → execute decision → summary report. Writes only to `docs/PROGRESS.md` or `docs/FAIL_FAST_LOG.md`. Never bulk-promotes.

Model pin rationale:
- `haiku` for codex-brief, som-worker-triage, issue-lane-bootstrap: lightweight orchestration and routing tasks; Haiku is the SoM Tier 1 model for these activities.
- `claude-sonnet-4-6` for sim-runner and backlog-promoter: complex reasoning required (sim invocation with provider constraints, HITL with code evidence reading).

Additionally: update CLAUDE.md routing table and delegation rules, write `docs/agents-adoption-guide.md` for cross-repo adoption.

## Constraints

- All 5 agent files must follow §DA frontmatter schema: `name`, `description`, `model`, `tools`
- CLAUDE.md must not exceed a reasonable line count after update
- No changes to STANDARDS.md, scripts/, packages/, or .github/workflows/
- No changes to any downstream repo
- Execution scope must list all allowed write paths explicitly
- Structured plan JSON must pass `validate_structured_agent_cycle_plan.py` before any commit

## Acceptance Criteria

1. `agents/codex-brief.md`, `agents/som-worker-triage.md`, `agents/issue-lane-bootstrap.md`, `agents/sim-runner.md`, `agents/backlog-promoter.md` all exist with correct frontmatter
2. CLAUDE.md routing table has 5 new rows; delegation rules have 5 new DO NOT rows
3. `docs/agents-adoption-guide.md` exists with complete table of all 9 governance agents
4. `docs/plans/issue-559-five-new-agents-structured-agent-cycle-plan.json` passes validator
5. `raw/execution-scopes/2026-04-22-issue-559-five-new-agents-implementation.json` exists
6. `raw/closeouts/2026-04-22-issue-559-five-new-agents.md` exists and closeout-hook passes
7. `OVERLORD_BACKLOG.md` Done section has issue #559 row at top

## Risks

- **CLAUDE.md line count:** The LAM CLAUDE.md line limit memory note mentions ≤30 lines; hldpro-governance CLAUDE.md is not subject to this (that is the LAM repo constraint). Risk: LOW.
- **Agent frontmatter drift:** If future §DA schema changes add required fields, these agents will need updates. Mitigation: agents follow the same pattern as existing `overlord.md` etc.
- **codex-brief template dependency:** If `docs/templates/codex-spark-dispatch-brief.md` moves, codex-brief agent Step 6 will reference wrong path. Risk: LOW (template path is stable since #412).

## Review

- Scope reviewer: accepted — all writes within declared allowed_write_paths
- Agent schema reviewer: accepted — all 5 agents have correct frontmatter and model pins per SoM routing table
- Alternate model review: not required — documentation-only, no standards or architecture changes
