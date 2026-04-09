# hldpro-governance — Feature Registry

**Last Updated:** 2026-04-09
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
| GOV-008 | `CLAUDE.md` rewritten as pure dispatcher — routes to overlord agents, never answers directly. Pre-session reads now point to `wiki/index.md` plus the governance repo’s scoped report at `graphify-out/hldpro-governance/GRAPH_REPORT.md` instead of the legacy root compatibility report. |
| GOV-009 | `hooks/closeout-hook.sh` validates Stage 6 closeout template, refreshes the manifest-defined closeout graph target through the repo-local builder, rebuilds `wiki/index.md`, and prompts for `operator_context` write-back. Template at `raw/closeouts/TEMPLATE.md`. |
| GOV-010 | `raw-feed-sync.yml` fetches open GitHub issues from all governed repos daily and writes metadata-only markdown summaries to `raw/github-issues/` (issue number, title, labels, created/updated dates, URL). Issue bodies are intentionally excluded so raw feeds do not create durable secondary copies of sensitive ticket content. |
| GOV-012 | `scripts/overlord/codex_ingestion.py` now supports real governed-repo `generate`, `qualify`, `status`, and `promote` flows with bounded timeouts, precomputed diff context, CI auth/canary support, session-start backlog surfacing, and strong-anchor cited-code validation during qualification so hallucinated line references are rejected before backlog promotion. |
| GOV-013 | `scripts/overlord/build_effectiveness_metrics.py` persists bug rate, revert rate, and CI pass rate baselines into governance, and `overlord-sweep.yml` refreshes the dated and latest snapshots weekly. |
| GOV-013 | Weekly sweep issue bodies now include a `BASELINE REFRESH` status block so operators can tell whether graph/metrics artifacts were actually persisted, and the workflow fails after publication when commit or push persistence fails. |
| GOV-014 | `docs/schemas/structured-agent-cycle-plan.schema.json` defines the canonical org-wide execution-plan contract, and `scripts/overlord/validate_structured_agent_cycle_plan.py` enforces it in reusable governance CI for issue/riskfix execution branches. |
| GOV-015 | `scripts/knowledge_base/measure_graphify_usage.py` compares graphify-guided retrieval with baseline repo search across tracked scenario files, and `metrics/graphify-evals/` stores the resulting quality and estimated token-footprint artifacts. |
| GOV-015 | `docs/schemas/graphify-usage-event.schema.json` and `scripts/knowledge_base/log_graphify_usage.py` define the append-only event path for auditing graphify, repo-search, and hybrid usage in governed workflows. |
| GOV-015 | The fail-fast retrieval slice now uses a repo-local governance graph when the scenario repo is governance itself, applies graph-aware ranking with one-hop link propagation, and scores relevance using both owning-file hits and expected evidence terms. The validated guidance is to pair symptom terms with mechanism/owner terms, then use bounded repo search only on the graph-returned files for code-centric cases. |
| GOV-015 | Workflow/doc-heavy fail-fast scenarios now use a deterministic `hybrid` retrieval path: graph-guided owner discovery plus bounded ranking over `.github/workflows/`, `docs/`, `metrics/`, and `raw/`, with primary workflow YAML favored over derivative plan and measurement artifacts. The updated 2026-04-09 corpus materially improved both workflow-heavy governance scenarios while staying below baseline repo-search token footprint. |
