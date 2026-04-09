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
| GOV-007 | KNOWLEDGE_BASE | Living Knowledge Base: graphify integration, wiki, raw feeds, Karpathy Loop | IN_PROGRESS | OPS_READY |
| GOV-008 | DISPATCHER | Agent dispatcher CLAUDE.md (MBIF Crew pattern) | COMPLETE | OPS_READY |
| GOV-009 | CLOSEOUT | Stage 6 closeout hook and template | COMPLETE | OPS_READY |
| GOV-010 | RAW_FEEDS | Nightly GitHub issue feed sync via GitHub Actions | COMPLETE | INTERNAL_ONLY |
| GOV-011 | ISSUE_BACKLOG_ALIGNMENT | Governance backlog must remain GitHub-issue-backed | COMPLETE | REQUIRED |
| GOV-012 | CODEX_INGESTION | Codex second-opinion ingestion and backlog surfacing loop | COMPLETE | OPS_READY |
| GOV-013 | EFFECTIVENESS_BASELINE | Reproducible weekly effectiveness metrics snapshots in `metrics/effectiveness-baseline/` | COMPLETE | OPS_READY |

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
| GOV-002 | Governance doc consistency rollout now requires source-of-truth metadata plus non-placeholder `DATA_DICTIONARY` and `SERVICE_REGISTRY` bodies in governed repos, while preserving repo-specific exceptions such as AIS backlog shape and the HealthcarePlatform backend pointer. |
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

### KNOWLEDGE_BASE

| Feature ID | Notes |
|---|---|
| GOV-007 | Three-tool system: graphify (knowledge graph), Karpathy Loop (compounding write-back), MBIF Crew (dispatcher pattern). Infrastructure in `graphify-out/`, `wiki/`, `raw/`. AIS and HealthcarePlatform code graphs are now built and synced into governance; the multi-repo weekly sweep/read-path is the next follow-on work. |
| GOV-008 | `CLAUDE.md` rewritten as pure dispatcher — routes to overlord agents, never answers directly. Pre-session reads: `wiki/index.md` + `GRAPH_REPORT.md`. |
| GOV-009 | `hooks/closeout-hook.sh` validates Stage 6 closeout template, triggers repo-local graph rebuild logic, and prompts for `operator_context` write-back. Template at `raw/closeouts/TEMPLATE.md`. |
| GOV-010 | `raw-feed-sync.yml` fetches open GitHub issues from all governed repos daily, writes markdown summaries to `raw/github-issues/`. Initial snapshot files have been seeded locally for the bootstrap loop. |
| GOV-012 | `scripts/overlord/codex_ingestion.py` now supports real governed-repo `generate`, `qualify`, `status`, and `promote` flows with bounded timeouts, precomputed diff context, CI auth/canary support, and session-start backlog surfacing. |
| GOV-013 | `scripts/overlord/build_effectiveness_metrics.py` persists bug rate, revert rate, and CI pass rate baselines into governance, and `overlord-sweep.yml` refreshes the dated and latest snapshots weekly. |
