# hldpro-governance — Feature Registry

**Last Updated:** 2026-04-21
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
| GOV-009 | CLOSEOUT | Stage 6 closeout hook, template, and merge-enforced evidence gate | COMPLETE | REQUIRED |
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
| GOV-027 | CODEX_FIRE_FAILFAST | Fail-fast Codex dispatcher wrapper with bounded model preflight and structured failure logging | IN_PROGRESS | OPS_READY |
| GOV-028 | REMOTE_MCP_BRIDGE_GOVERNANCE | Remote MCP Bridge standards, thin client contract, audit verifier, Stage D proof runner, recurring health monitor, payload-safe alerts, and operator runbook | IN_PROGRESS | REQUIRED |
| GOV-029 | PAGES_DEPLOY_GATE | Pages Deploy Gate (governance-owned, issue #469) | COMPLETE | OPS_READY |
| GOV-030 | PAGES_DEPLOYMENT_PARITY | Cloudflare Pages deployment freshness and domain parity verifier | COMPLETE | OPS_READY |
| GOV-031 | SECRET_PROVISIONING_EVIDENCE | No-secret provisioning evidence validator and Local CI Gate check | COMPLETE | REQUIRED |
| GOV-032 | CLI_SESSION_AND_PR_CONTRACTS | CLI supervisor native argv contracts and GitHub-native PR merge/check evaluator | COMPLETE | REQUIRED |
| GOV-033 | CONSUMER_WORKER_ACCEPTANCE | Consumer verifier evidence required before accepted Worker handoff for consumer-managed governance surfaces | COMPLETE | REQUIRED |

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
| GOV-029 | `scripts/pages-deploy/pages_deploy_gate.py` provides a reusable Cloudflare Pages Direct Upload gate for governed consumers. It validates consumer config, preflights `node`/`wrangler`, checks required env names without printing values, emits canonical Secret Provisioning UX guidance for missing Cloudflare credentials, requires `PAGES_DEPLOY_APPROVED=1` for live deploys, runs optional pre-deploy hooks before build/upload, rejects stale or oversized artifacts, invokes Wrangler with `CI=true` without the removed Wrangler 4.x `--non-interactive` flag, and emits redacted deployment evidence. |
| GOV-030 | `scripts/bootstrap-repo-env.sh` includes Cloudflare Pages deploy names in Seek and Ponder bootstrap targets so local worktrees can receive `CLOUDFLARE_PAGES_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` through the approved generated-env path instead of inline export commands. |
| GOV-030 | `scripts/bootstrap-repo-env.sh` includes staged core smoke seeded-login names in Seek and Ponder bootstrap targets so post-deploy smoke can use generated env files instead of inline export commands. |
| GOV-030 | `scripts/pages-deploy/inventory_direct_upload_projects.py` inventories Cloudflare Pages Direct Upload projects, classifies gate adoption state, and links uncovered governed consumers to issue-backed adoption follow-ups. Issue #472 records `seek-and-ponder` as covered, HealthcarePlatform#1478 for `hldpro-dashboard`, and ai-integration-services#1217 for `hldpro-marketing`, `hldpro-pwa`, and `hldpro-reseller`. |
| GOV-031 | `scripts/overlord/validate_provisioning_evidence.py` scans provisioning evidence for token-like strings, JWT fragments, Authorization headers, signed URLs, raw phone numbers, and generated env file contents while reporting only file paths and matched classes. |
| GOV-031 | The `hldpro-governance` Local CI Gate profile runs `provisioning-evidence-safety` when standards, env registry, runbooks, validation artifacts, Pages deploy tooling, or Remote MCP tooling change. |
| GOV-032 | `scripts/cli_session_supervisor.py` enforces Claude `--output-format stream-json` with `--verbose`, preserves native Claude/Codex argv construction in tests, and requires Codex native sessions to include `model_reasoning_effort`. `scripts/overlord/automerge_policy_check.py` separates expected pending required checks from final blockers and routes merge guidance through GitHub-native `gh pr update-branch` / `gh pr merge` paths rather than local `main`. |
| GOV-033 | `scripts/overlord/verify_governance_consumer.py` resolves default package manifests from the supplied `--governance-root`, fails typoed roots, and keeps malformed `local_overrides` plus stale reusable workflow SHA as hard failures. `scripts/overlord/validate_handoff_package.py` requires `verify_governance_consumer.py` commands and evidence refs before accepted handoffs touching consumer-managed paths can close. |

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
| GOV-009 | `scripts/overlord/check_stage6_closeout.py` requires issue-matching `raw/closeouts/*issue-NNN*.md` evidence for implementation/governance-surface PRs while preserving planning-only lanes. The reusable governance workflow and `hldpro-governance` Local CI Gate profile both call the same validator. |
| GOV-010 | `raw-feed-sync.yml` fetches open GitHub issues from all governed repos daily and writes metadata-only markdown summaries to `raw/github-issues/` (issue number, title, labels, created/updated dates, URL). Issue bodies are intentionally excluded so raw feeds do not create durable secondary copies of sensitive ticket content. |
| GOV-012 | `scripts/overlord/codex_ingestion.py` now supports real governed-repo `generate`, `qualify`, `status`, and `promote` flows with bounded timeouts, precomputed diff context, CI auth/canary support, session-start backlog surfacing, and strong-anchor cited-code validation during qualification so hallucinated line references are rejected before backlog promotion. |
| GOV-027 | `scripts/codex-fire.sh` is the required local dispatcher path for Codex brief execution. It preflights the selected model within a bounded timeout, writes failures to `raw/fail-fast-log.md`, and emits `CODEX_FAIL` so unavailable models do not look like live work. Dedicated canary/preflight helpers and the Python ingestion helper may keep their own direct Codex calls only when they preserve bounded timeout and structured failure semantics. |
| GOV-028 | Issue #109 completed Remote MCP Bridge invariants 11-15, the thin `scripts/som-client/` operator client, `scripts/remote-mcp/verify_audit.py`, `scripts/remote-mcp/stage_d_smoke.py`, `check-remote-mcp-audit-schema.yml`, and the `docs/runbooks/remote-mcp-bridge.md` operator runbook. Issue #372 adds `scripts/remote-mcp/live_health_monitor.py`, `.github/workflows/remote-mcp-live-health.yml`, and `launchd/com.hldpro.remote-mcp-monitor.plist` for recurring health/audit monitoring. Issue #374 adds `scripts/remote-mcp/monitor_alert.py` and first fixture-run alert evidence for payload-safe operator summaries. Issue #376 selects local `launchd` as the live-authoritative operating mode while keeping GitHub Actions as the scheduled fixture harness and optional configured-live runner. Issue #378 hardens the launchd template to live fail-closed mode and preserves payload-safe launchd render, rehearsal, and missing-config evidence. Issue #380 adds `scripts/remote-mcp/operator_connectivity.py`, a no-secret fixture/live preflight that reports whether this machine can send `som.ping` to Remote MCP and receive a response now. Issue #382 adds `scripts/remote-mcp/operator_inbound_preflight.py`, a no-secret fixture/live preflight for operator-message receive readiness through the HITL relay session inbox path. Issue #385 bootstraps the local operator vault keys, Cloudflare Access service-token policy membership, Stage B/C bridge protocol selection in `SomClient`, local bridge LaunchAgent proof on the tunnel origin port, and live no-secret request/response plus inbound receive evidence. |
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
| GOV-019 | `scripts/overlord/assert_execution_scope.py --require-lane-claim` requires the current branch issue, expected branch issue, and execution-scope `lane_claim.issue_number` to match before implementation work is authorized. |
| GOV-019 | `hooks/branch-switch-guard.sh` blocks unmarked `git worktree add -b issue-*` commands before filesystem side effects; issue-lane worktree creation must use explicit planning bootstrap or a matching claimed execution scope. |
| GOV-019 | `scripts/overlord/assert_execution_scope.py` resolves detached PR checkouts through `GITHUB_HEAD_REF`/`GITHUB_REF_NAME` so reusable governance checks can validate trusted scopes while preserving local wrong-branch failures. |
| GOV-019 | Planner write-boundary enforcement now treats Tier 1 sessions as planning-only by default (`execution_mode: planning_only`), with `allowed_write_paths` as the planning artifact allowlist. |
| GOV-019 | Non-planning diffs now require accepted pinned-agent handoff evidence, and same-model or same-family planner/implementer pairs require an active exception reference with expiry. |
| GOV-019 | For planner-boundary enforcement, CI in `.github/workflows/governance-check.yml` is authoritative while local `hooks/code-write-gate.sh` output is warning/early-signal only. |

### PAGES_DEPLOYMENT_PARITY

| Feature ID | Notes |
|---|---|
| GOV-029 | `scripts/pages-deploy/pages_deploy_verifier.py` verifies Cloudflare Pages freshness across the Pages alias and custom domains using the stable `/cdn-cgi/pages/deployment` endpoint or `cf-deployment-id` header, records redirect/status chains, cache-busts every request, retries transient failures, refuses stale local checkouts before HTTP probes, and treats inactive custom-domain/CNAME findings as nonblocking operator concerns. |

### READ_ONLY_GOVERNANCE_OBSERVER

| Feature ID | Notes |
|---|---|
| GOV-020 | `scripts/orchestrator/read_only_observer.py` reads registry, graphify, wiki, compendium, closeout, backlog, and raw issue metadata artifacts, then writes per-repo JSON/Markdown reports under `projects/<repo_slug>/reports/`. |
| GOV-020 | `launchd/com.hldpro.governance-observer.plist` and `docs/runbooks/always-on-governance.md` define the disabled-by-default macOS user-agent path, health checks, logs, and kill/disable SOP. |
| GOV-020 | The observer reports source commit SHAs, artifact SHA-256 hashes, stale knowledge signals, planning-gate state, and daemon readiness while keeping `packet_enqueue_enabled: false`. |

### LOCAL_MODEL_RUNTIME_INVENTORY

| Feature ID | Notes |
|---|---|
| GOV-021 | `scripts/lam/runtime_inventory.py` reports Mac hardware, MLX availability, deprecated/off-ladder Windows Ollama metadata if probed, PII pattern readiness, memory budgets, and fail-closed routing boundaries without sending prompt payloads. |
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
| GOV-023 | Issue #475 adds an operational proof pattern: stale self-learning reports must be repaired by fixing the pre-sweep blocker, regenerating metrics, and preserving an issue-backed `raw/operator-context/self-learning/` artifact. |
| GOV-023 | Issue #535 adds `docs/runbooks/session-error-patterns.md` as the operator lookup table for exact session error signatures and indexes it in `scripts/orchestrator/self_learning.py` as `session_error_pattern` so lookup/report output can surface the correction path. |

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
| GOV-016 | Issue #432 revises the governance waterfall SSOT: Codex orchestrates and integrates, Opus 4.6 plans, GPT-5.4 high reviews the plan with Spark only as a logged fallback/specialist critique, Sonnet 4.6 is the primary Worker, Codex performs QA, Qwen local models handle bounded implementation chunks, Gemma is A/B shadow-only, and Windows Ollama is off the active fallback ladder. |
| GOV-021 | Runtime inventory now treats Windows Ollama as deprecated/off-ladder, exposes Qwen2.5-Coder/Qwen3-14B/Qwen3.6 as the local worker ladder, and asserts Gemma's `ab_shadow_only` authority. |
## Pages Deploy Gate

- Issue: #469
- Owner: governance-owned
- Status: implementation complete
- Summary: Reusable Cloudflare Pages Direct Upload deploy gate with pre-deploy phase, CI/Wrangler preflight, build freshness checks, Pages limits, secret redaction, and evidence JSON.
