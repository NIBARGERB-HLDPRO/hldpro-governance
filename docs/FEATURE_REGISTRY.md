# hldpro-governance — Feature Registry

**Last Updated:** 2026-04-19
**Scope:** Shared governance standards, reusable CI enforcement, and cross-repo audit agents.

---

## Status Taxonomy

| Implementation Status | Meaning |
|---|---|
| `COMPLETE` | Built and in active use |
| `IN_PROGRESS` | Actively being changed or expanded |
| `PLANNED` | Intended but not yet implemented |

| Readiness | Meaning |
|---|---|
| `REQUIRED` | Expected baseline for governed repos |
| `OPS_READY` | Ready for operational use by repo maintainers |
| `INTERNAL_ONLY` | Internal tooling, not a repo baseline |

---

## Summary Table

| Feature ID | Domain | Feature | Status | Readiness |
|---|---|---|---|---|
| GOV-001 | STANDARDS | Shared standards manifest in `STANDARDS.md` | COMPLETE | REQUIRED |
| GOV-002 | CI_ENFORCEMENT | Reusable GitHub governance workflow | COMPLETE | REQUIRED |
| GOV-003 | AGENT_AUDIT | Overlord audit agents (`overlord`, `overlord-sweep`, `overlord-audit`) | COMPLETE | OPS_READY |
| GOV-004 | COMPLETION_VERIFICATION | `verify-completion` agent and artifact verification protocol | COMPLETE | OPS_READY |
| GOV-005 | BACKLOG_CONTROL | Cross-repo backlog coordination in `OVERLORD_BACKLOG.md` | COMPLETE | OPS_READY |
| GOV-006 | FEATURE_REGISTRY_POLICY | Feature-registry requirement and co-staging enforcement | IN_PROGRESS | REQUIRED |
| GOV-007 | KNOWLEDGE_BASE | Living Knowledge Base: graphify integration, wiki, raw feeds, Karpathy Loop, local graph runtime bootstrap, and Neo4j push path | IN_PROGRESS | OPS_READY |
| GOV-008 | DISPATCHER | Agent dispatcher CLAUDE.md (MBIF Crew pattern) | COMPLETE | OPS_READY |
| GOV-009 | CLOSEOUT | Stage 6 closeout hook and template | COMPLETE | OPS_READY |
| GOV-010 | RAW_FEEDS | Nightly GitHub issue feed sync via GitHub Actions | COMPLETE | INTERNAL_ONLY |
| GOV-011 | ISSUE_BACKLOG_ALIGNMENT | Governance backlog must remain GitHub-issue-backed | COMPLETE | REQUIRED |
| GOV-012 | CODEX_INGESTION | Codex second-opinion ingestion and backlog surfacing loop | COMPLETE | OPS_READY |
| GOV-013 | EFFECTIVENESS_BASELINE | Reproducible weekly effectiveness metrics snapshots in `metrics/effectiveness-baseline/` | COMPLETE | OPS_READY |
| GOV-014 | STRUCTURED_PLAN_SCHEMA | Governance-owned structured plan schema and validator for issue execution | COMPLETE | REQUIRED |
| GOV-015 | GRAPHIFY_MEASUREMENT | Graphify retrieval measurement and usage-event telemetry | IN_PROGRESS | OPS_READY |
| GOV-016 | SOM_ENFORCEMENT | Society of Minds routing, review, packet, and closeout enforcement | IN_PROGRESS | REQUIRED |
| GOV-017 | ORG_GOVERNANCE_COMPENDIUM | Org-level governance rules compendium generated from governed repo rule files and graph nodes | COMPLETE | OPS_READY |
| GOV-018 | GOVERNED_REPO_REGISTRY | Executable governed repository registry and validator | COMPLETE | REQUIRED |
| GOV-019 | PLANNING_SCOPE_GATEKEEPER | Issue-backed governance-surface planning and execution-scope gatekeeper | COMPLETE | REQUIRED |
| GOV-020 | READ_ONLY_GOVERNANCE_OBSERVER | Deterministic per-repo governance observer reports without packet enqueue authority | COMPLETE | OPS_READY |
| GOV-021 | LOCAL_MODEL_RUNTIME_INVENTORY | No-payload local/Windows model runtime inventory and PII guardrail readiness | COMPLETE | REQUIRED |
| GOV-022 | PACKET_QUEUE_ORCHESTRATOR | Filesystem packet queue with dispatch gate, PII halt, and replayable audit log | COMPLETE | REQUIRED |
| GOV-023 | SELF_LEARNING_LOOP | Pre-dispatch mistake lookup, packet context injection, append-only failure write-back, and weekly learning drift report | COMPLETE | REQUIRED |
| GOV-024 | E2E_AUTONOMOUS_DELIVERY_PILOT | Low-risk governance pilot from issue-backed plan through packet, review, gate, closeout, PR checks, and readiness conclusion | COMPLETE | REQUIRED |
| GOV-025 | GRAPHIFY_HOOK_HELPER | Governance-owned graphify hook helper and installer for governed repo graph refresh hooks | COMPLETE | OPS_READY |
| GOV-026 | PENTAGI_SWEEP_STATUS | Registry-aware PentAGI freshness and trigger status for overlord sweep report/dashboard source alignment | IN_PROGRESS | OPS_READY |

---

## Domain Notes

### STANDARDS

| Feature ID | Notes |
|---|---|
| GOV-001 | Defines the baseline governance contract for all HLDPRO code repos, including hooks, CI, security tiers, and verification rules. |

### CI_ENFORCEMENT

| Feature ID | Notes |
|---|---|
| GOV-002 | Reusable workflow enforces doc co-staging, placeholder scans, migration documentation, and other shared merge gates. |
| GOV-002 | The reusable governance workflow now accepts a caller-provided `base_sha` and resolves one shared diff base internally so all range-based checks run against the full PR delta under `workflow_call`, not just the most recent commit. |
| GOV-002 | Governance doc consistency rollout now requires source-of-truth metadata plus non-placeholder `DATA_DICTIONARY` and `SERVICE_REGISTRY` bodies in governed repos, while preserving repo-specific exceptions such as AIS backlog shape and the HealthcarePlatform backend pointer. |
| GOV-002 | `graphify-governance-contract.yml` is the governance repo’s local graphify contract gate: it validates the manifest-defined target set, helper scripts, and generated `wiki/index.md` synchronization before graph contract changes merge. |
| GOV-006 | Current rollout adds `docs/FEATURE_REGISTRY.md` as a governed artifact and blocks stale code-only changes when the registry is not updated. |

### AGENT_AUDIT

| Feature ID | Notes |
|---|---|
| GOV-003 | Agent set performs repo sweeps, standards audits, and backlog-quality checks across the portfolio. |
| GOV-004 | Completion verifier exists to prevent false “done” claims by checking artifacts, PR state, and standards compliance. |
| GOV-004 | Completion verification now explicitly requires PDCA/R Adjust/Review to capture any newly discovered required action as either part of the current acceptance path or an issue-backed follow-up before closure. |

### BACKLOG_CONTROL

| Feature ID | Notes |
|---|---|
| GOV-005 | `OVERLORD_BACKLOG.md` tracks cross-repo governance work; per-repo execution details stay in each repo’s `docs/PROGRESS.md`. |
| GOV-011 | `OVERLORD_BACKLOG.md` is now a roadmap/status mirror only. Actionable `Planned` and `In Progress` rows must carry GitHub issue references, and governance CI enforces that alignment. |
| GOV-011 | Governed product repos now also have a `docs/PROGRESS.md` ↔ GitHub issue staleness gate: open backlog-labeled issues must appear in active backlog sections and closed backlog-labeled issues must not remain listed as active. The reusable governance workflow enforces it in CI and the weekly sweep reports drift counts per repo. |

### KNOWLEDGE_BASE

| Feature ID | Notes |
|---|---|
| GOV-007 | Three-tool system: graphify (knowledge graph), Karpathy Loop (compounding write-back), MBIF Crew (dispatcher pattern). Infrastructure in `graphify-out/`, `wiki/`, `raw/`. AIS, HealthcarePlatform, ASC-Evaluator, local-ai-machine, and knocktracker are now graphified into governance, `docs/graphify_targets.json` is the executable refresh-target manifest, `scripts/knowledge_base/bootstrap_neo4j.sh` provides the local runtime bootstrap path, and `scripts/knowledge_base/push_graph_to_neo4j.py` validates the first local Neo4j push path with scoped graph ids. |
| GOV-007 | `scripts/knowledge_base/graphify_hook_helper.py` is the governed hook installer/runner. It resolves repo slug, source/output/wiki paths, and hook locations through the governance root and `docs/graphify_targets.json`; refuses product-checkout graph outputs before `build_graph.py`; and installs managed hooks only after refusing or backing up unmanaged hooks. AIS and knocktracker adoption PRs must prove raw graphify hooks are removed or absent and record helper dry-run output. |
| GOV-008 | `CLAUDE.md` rewritten as pure dispatcher — routes to overlord agents, never answers directly. Pre-session reads now point to `wiki/index.md` plus the governance repo’s scoped report at `graphify-out/hldpro-governance/GRAPH_REPORT.md` instead of the legacy root compatibility report. |
| GOV-009 | `hooks/closeout-hook.sh` validates Stage 6 closeout template, refreshes the manifest-defined closeout graph target through the repo-local builder, rebuilds `wiki/index.md`, and prompts for `operator_context` write-back. Template at `raw/closeouts/TEMPLATE.md`. |
| GOV-010 | `raw-feed-sync.yml` fetches open GitHub issues from all governed repos daily and writes metadata-only markdown summaries to `raw/github-issues/` (issue number, title, labels, created/updated dates, URL). Issue bodies are intentionally excluded so raw feeds do not create durable secondary copies of sensitive ticket content. |
| GOV-012 | `scripts/overlord/codex_ingestion.py` now supports real governed-repo `generate`, `qualify`, `status`, and `promote` flows with bounded timeouts, precomputed diff context, CI auth/canary support, session-start backlog surfacing, and strong-anchor cited-code validation during qualification so hallucinated line references are rejected before backlog promotion. |
| GOV-013 | `scripts/overlord/build_effectiveness_metrics.py` persists bug rate, revert rate, and CI pass rate baselines into governance, and `overlord-sweep.yml` refreshes the dated and latest snapshots weekly. |
| GOV-013 | Weekly sweep issue bodies now include a `BASELINE REFRESH` status block so operators can tell whether graph/metrics artifacts were actually persisted, and the workflow fails after publication when commit or push persistence fails. |
| GOV-014 | `docs/schemas/structured-agent-cycle-plan.schema.json` defines the canonical org-wide execution-plan contract, and `scripts/overlord/validate_structured_agent_cycle_plan.py` enforces it in reusable governance CI for issue/riskfix execution branches. |
| GOV-015 | `scripts/knowledge_base/measure_graphify_usage.py` compares graphify-guided retrieval with baseline repo search across tracked scenario files, and `metrics/graphify-evals/` stores the resulting quality and estimated token-footprint artifacts. |
| GOV-015 | `docs/schemas/graphify-usage-event.schema.json` and `scripts/knowledge_base/log_graphify_usage.py` define the append-only event path for auditing graphify, repo-search, and hybrid usage in governed workflows, including optional prompt/query/candidate telemetry for live A/B traces. |
| GOV-015 | The fail-fast retrieval slice now uses a repo-local governance graph when the scenario repo is governance itself, applies graph-aware ranking with one-hop link propagation, and scores relevance using both owning-file hits and expected evidence terms. The validated guidance is to pair symptom terms with mechanism/owner terms, then use bounded repo search only on the graph-returned files for code-centric cases. |
| GOV-015 | Workflow/doc-heavy fail-fast scenarios now use a deterministic `hybrid` retrieval path: graph-guided owner discovery plus bounded ranking over `.github/workflows/`, `docs/`, `metrics/`, and `raw/`, with primary workflow YAML favored over derivative plan and measurement artifacts. The updated 2026-04-09 corpus materially improved both workflow-heavy governance scenarios while staying below baseline repo-search token footprint. |
| GOV-015 | The graphify measurement outputs now surface per-scenario query traces (`prompt`, `query_terms`, graphify candidates, baseline candidates) so 5-10 run comparisons can be reviewed at retrieval-input level instead of only through aggregate hit-rate summaries. |
| GOV-015 | `measure_graphify_usage.py` now emits append-only usage events by default for each scenario and retrieval strategy, so current-work A/B runs automatically leave auditable query-trace telemetry instead of relying on separate manual logger calls. |
| GOV-015 | The fail-fast scenario corpus no longer depends on stale absolute governance worktree paths. `measure_graphify_usage.py` now resolves governance scenarios from the current checkout by default and falls back safely when an explicit `repo_path` no longer exists, so refreshed A/B evidence reflects current runs instead of abandoned-worktree noise. |

### ORG_GOVERNANCE_COMPENDIUM

| Feature ID | Notes |
|---|---|
| GOV-017 | `scripts/overlord/build_org_governance_compendium.py` generates `docs/ORG_GOVERNANCE_COMPENDIUM.md` from canonical governed repo rule files, graphify node summaries, workflows, hooks, agents, schemas, and PDCA/R docs. `overlord-sweep.yml` refreshes and stages it with weekly graph and metrics updates. |

### GOVERNED_REPO_REGISTRY

| Feature ID | Notes |
|---|---|
| GOV-018 | `docs/governed_repos.json` is the executable source of truth for governed repo metadata, including GitHub repo, local and CI paths, graph/wiki/project paths, tiers, and enabled subsystems. |
| GOV-018 | `scripts/overlord/validate_governed_repos.py` validates the registry and reconciles graphify targets; `scripts/overlord/governed_repos.py` is the shared adapter used by sweep metrics, memory integrity, and the org governance compendium. |
| GOV-026 | `scripts/overlord/pentagi_sweep.py` evaluates PentAGI-tier sweep repos from `docs/governed_repos.json`, emits one JSON/Markdown payload from the audited checkout root, and records explicit trigger/skip statuses for missing/stale reports, missing `PENTAGI_API_TOKEN`, and missing repo-local runners. `overlord-sweep.yml` persists the latest payload under `metrics/pentagi/latest.json` and appends the same Markdown to the weekly report. |

### PLANNING_SCOPE_GATEKEEPER

| Feature ID | Notes |
|---|---|
| GOV-019 | `scripts/overlord/validate_structured_agent_cycle_plan.py` classifies governance-surface paths and requires issue-specific canonical structured plans with implementation-ready handoff and accepted alternate review before those paths can change. |
| GOV-019 | `.github/workflows/governance-check.yml` and `hooks/code-write-gate.sh` call the shared validator so CI and local write-time enforcement use the same governance-surface planning gate. |
| GOV-019 | `scripts/overlord/validate_structured_agent_cycle_plan.py --enforce-planner-boundary-scope` provides a local E2E simulation of CI planner-boundary scope resolution by requiring issue-matching execution-scope JSON under `raw/execution-scopes/` whenever planner-boundary files change. |
| GOV-019 | `scripts/overlord/assert_execution_scope.py` remains the root/branch/write-scope guard, with tests proving wrong checkout roots, dirty forbidden roots, and out-of-scope paths fail locally. |
| GOV-019 | `scripts/overlord/assert_execution_scope.py` resolves detached PR checkouts through `GITHUB_HEAD_REF`/`GITHUB_REF_NAME` so reusable governance checks can validate trusted scopes while preserving local wrong-branch failures. |
| GOV-019 | Planner write-boundary enforcement now treats Tier 1 sessions as planning-only by default (`execution_mode: planning_only`), with `allowed_write_paths` as the planning artifact allowlist. |
| GOV-019 | Non-planning diffs now require accepted pinned-agent handoff evidence, and same-model or same-family planner/implementer pairs require an active exception reference with expiry. |
| GOV-019 | For planner-boundary enforcement, CI in `.github/workflows/governance-check.yml` is authoritative while local `hooks/code-write-gate.sh` output is warning/early-signal only. |

### READ_ONLY_GOVERNANCE_OBSERVER

| Feature ID | Notes |
|---|---|
| GOV-020 | `scripts/orchestrator/read_only_observer.py` reads registry, graphify, wiki, compendium, closeout, backlog, and raw issue metadata artifacts, then writes per-repo JSON/Markdown reports under `projects/<repo_slug>/reports/`. |
| GOV-020 | `launchd/com.hldpro.governance-observer.plist` and `docs/runbooks/always-on-governance.md` define the disabled-by-default macOS user-agent path, health checks, logs, and kill/disable SOP. |
| GOV-020 | The observer reports source commit SHAs, artifact SHA-256 hashes, stale knowledge signals, planning-gate state, and daemon readiness while keeping `packet_enqueue_enabled: false`. |

### LOCAL_MODEL_RUNTIME_INVENTORY

| Feature ID | Notes |
|---|---|
| GOV-021 | `scripts/lam/runtime_inventory.py` reports Mac hardware, MLX availability, Windows Ollama metadata reachability, PII pattern readiness, memory budgets, and fail-closed routing boundaries without sending prompt payloads. |
| GOV-021 | `docs/runbooks/local-model-runtime.md` defines the Mac M5 Pro 48 GB steady-state and on-demand model budget. |
| GOV-021 | `docs/runbooks/windows-ollama.md` resolves the prior Windows VRAM assumption as unverified and keeps Windows LAN-only fallback/batch/health until direct host telemetry exists. |

### PACKET_QUEUE_ORCHESTRATOR

| Feature ID | Notes |
|---|---|
| GOV-022 | `scripts/orchestrator/packet_queue.py` creates queue states under `raw/packets/queue/` and supports `inbound`, `dispatched`, `review`, `gate`, `done`, and `halted` transitions. |
| GOV-022 | Dispatch requires the existing SoM packet validator plus governance metadata: issue number, structured plan reference, execution scope reference, model identity, fallback log field, validation commands, review artifacts, PII mode, and explicit dispatch authorization. |
| GOV-022 | Dispatch scope evidence is fail-closed: when `governance.execution_scope_ref` is present, it must be a JSON artifact under `raw/execution-scopes/`; PDCAR Markdown and other arbitrary files are refused. |
| GOV-022 | State changes are recorded in `raw/packets/queue/audit.jsonl` with timestamp, source, destination, packet id, SHA-256, dry-run flag, allowed flag, status, and reason so queue movement can be replayed without executing packet payloads. |

### HITL_RELAY_QUEUE

| Feature ID | Notes |
|---|---|
| GOV-025 | `scripts/orchestrator/hitl_relay_queue.py` provides the queue-first HITL relay prototype for issue #301, using local request, response, decision, session-inbox, session-resume, dead-letter, and audit directories under `raw/hitl-relay/queue/`. |
| GOV-025 | The prototype writes packets with temp-file-then-rename semantics and validates every emitted HITL packet through `scripts/packet/validate_hitl_relay.py` before it reaches a session inbox or resume queue. |
| GOV-025 | Approval, request-changes, clarification, stale-session, duplicate, expired, dead-letter, and replay paths are covered by `scripts/orchestrator/test_hitl_relay_queue.py`; live AIS transport and MCP session control remain separate repo slices. |

### SELF_LEARNING_LOOP

| Feature ID | Notes |
|---|---|
| GOV-023 | `scripts/orchestrator/self_learning.py` indexes `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`, raw closeouts, raw operator context, graphify attention, and the org compendium before dispatch. |
| GOV-023 | Worker packets can be enriched with `governance.known_failure_context`, including cited direct evidence paths and repeat counts. |
| GOV-023 | `packet_queue.py` halts dispatch when known-failure context reports `repeat_count >= 2`, forcing planning-gate escalation before repeating a documented mistake. |
| GOV-023 | `record-failure` writes novel failures to `raw/operator-context/self-learning/` as new issue-backed files and never overwrites human-authored logs. |
| GOV-023 | `overlord-sweep.yml` builds `metrics/self-learning/latest.json` and `latest.md`, appends the markdown report to the weekly issue, and persists the metric with other weekly generated artifacts. |

### E2E_AUTONOMOUS_DELIVERY_PILOT

| Feature ID | Notes |
|---|---|
| GOV-024 | Issue #231 records the first low-risk end-to-end pilot of the always-on governance orchestrator flow using governance-owned artifacts only. |
| GOV-024 | Pilot artifacts include structured plan, PDCAR, SoM packet, metrics, alternate-family review, completion gate, closeout, PR checks, and merge evidence. |
| GOV-024 | The pilot conclusion is readiness for a follow-up planning issue to define broader autonomous execution authority; this slice does not grant that authority. |

### SOCIETY_OF_MINDS

| Feature ID | Notes |
|---|---|
| GOV-016 | The original SoM charter landed under umbrella #99; enforcement-drift closure now runs under epic #214 with issue-backed slices #215-#221. Active enforcement work covers Codex model/reasoning pin checks, ladder consistency, cross-review gate identity, architecture tier evidence, packet schema/runtime-boundary accuracy, operational closeout evidence, and execution-root/write-scope validation. |
| GOV-016 | Future SoM closeouts must identify the wired checks actually run, schema/artifact version, model identities, reviewer and gate identity, issue links, validation commands, and residual risks or deferrals. The closeout contract lives in `raw/closeouts/TEMPLATE.md`, with the current Slice 6 record under `raw/closeouts/2026-04-17-som-enforcement-drift-closeout-loop.md`. |
