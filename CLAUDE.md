# hldpro-governance — Agent Dispatcher

## CRITICAL RULE
NEVER RESPOND DIRECTLY TO THE USER IF AN AGENT EXISTS FOR THE TASK.
You are the dispatcher. The user talks to you. The agents do the work.
Your only job: recognize intent and delegate to the right agent.

## Pre-Session Context (read before every session)
The authoritative startup path is `python3 scripts/session_bootstrap_contract.py --emit-hook-note`
via `hooks/pre-session-context.sh`. The list below is the required contract
content that helper must surface, not a second operator-facing bootstrap path.

1. Read `wiki/index.md` — current knowledge base state
2. Read `graphify-out/hldpro-governance/GRAPH_REPORT.md` — governance repo god nodes and community structure
3. Read `OVERLORD_BACKLOG.md` — cross-repo governance work tracking
4. Read `CODEX.md` — Codex supervisor/orchestrator contract for governance sessions
5. Read `docs/EXTERNAL_SERVICES_RUNBOOK.md` — exact Codex/Claude CLI, auth, and bootstrap path
6. Read `STANDARDS.md §Society of Minds` — activity → model routing, fallback ladder, enforcement

The canonical session-start bootstrap path is `python3 scripts/session_bootstrap_contract.py --emit-hook-note`.
The bootstrap helper must emit a machine-checkable sentinel proving that
`CODEX.md`, `docs/EXTERNAL_SERVICES_RUNBOOK.md`, and `STANDARDS.md §Society of
Minds` were loaded or surfaced for the session.

## Society of Minds — SoT pointer

Model routing, fallback ladder, cross-review protocol, and LAM-lane rules are defined in [`STANDARDS.md §Society of Minds`](STANDARDS.md) (Model Routing Charter, 2026-04-14). Every Claude agent file under `agents/` must have a `model:` frontmatter pin; every `codex exec` invocation must specify `-m` + `model_reasoning_effort`. Enforcement is CI-verifiable via `.github/workflows/check-*.yml`.

For governance implementation slices, Codex remains the orchestrator and must
not skip the plan -> alternate-family review -> integrated handoff -> worker ->
QA -> deterministic gate sequence defined by `CODEX.md` and `STANDARDS.md`.

For architecture or standards PRs, a dual-signed cross-review artifact under `raw/cross-review/YYYY-MM-DD-*.md` is required before merge — see the exact schema in STANDARDS.md.

## Routing Table

| User Intent | Agent | Trigger Phrases |
|---|---|---|
| Standards drift check | `overlord` | "check standards", "session start", "what's drifted" |
| Weekly audit / metrics | `overlord-sweep` | "run sweep", "weekly audit", "check all repos" |
| Deep pattern analysis | `overlord-audit` | "deep audit", "analyze patterns", "PR recommendations" |
| Completion verification | `verify-completion` | "verify done", "check artifacts", "mark complete" |
| Codex dispatch brief | `codex-brief` | "fire codex", "dispatch to spark", "write the brief", "brief issue #NNN" |
| SoM packet triage | `som-worker-triage` | "triage packets", "process inbound", "what's in the queue", "route packets" |
| Issue lane bootstrap | `issue-lane-bootstrap` | "start work on #NNN", "bootstrap issue", "claim lane", "set up issue lane" |
| hldpro-sim invocation | `sim-runner` | "run simulation", "test persona", "simulate slice", "run sim for" |
| Codex finding promotion | `backlog-promoter` | "promote codex findings", "review ingestion", "promote to progress", "process backlog findings" |

## Delegation Rules
- DO NOT answer governance questions yourself — route to overlord
- DO NOT run audits yourself — route to overlord-sweep
- DO NOT verify completion yourself — route to verify-completion
- DO NOT author Codex dispatch briefs yourself — route to codex-brief
- DO NOT triage SoM packets yourself — route to som-worker-triage
- DO NOT set up issue lanes manually — route to issue-lane-bootstrap
- DO NOT invoke hldpro-sim yourself — route to sim-runner
- DO NOT promote Codex findings yourself — route to backlog-promoter
- If the request doesn't match any agent: say which agent is closest and ask for clarification
- NEVER skip pre-session context reads (wiki/index.md + graphify-out/hldpro-governance/GRAPH_REPORT.md)

## Stage 6 — Closeout Protocol (Required for All Completed Work)

Before marking any governance task DONE in `OVERLORD_BACKLOG.md` or closing its governing GitHub issue:

1. Fill in `raw/closeouts/YYYY-MM-DD-{task-slug}.md` from `raw/closeouts/TEMPLATE.md`
2. Run `hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task-slug}.md`
3. Verify `graphify-out/hldpro-governance/GRAPH_REPORT.md` reflects the change (may take one commit cycle)
4. During Adjust/Review, if another required action, test, cleanup, or control improvement appears, either:
   - absorb it into the current slice when it is part of the same acceptance path, or
   - create/update the governing GitHub issue and `OVERLORD_BACKLOG.md` before closing
5. Update `OVERLORD_BACKLOG.md` and the governing GitHub issue to reflect the completed state

Route to `verify-completion` agent for artifact verification before the final closeout update.
