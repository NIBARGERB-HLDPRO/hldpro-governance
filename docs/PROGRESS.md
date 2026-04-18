# hldpro-governance — Progress & Backlog

**Last Updated:** 2026-04-17
**Scope:** Cross-repo governance standards, CI enforcement, audit agents, and knowledge base infrastructure.

> This file is the single source of truth for planned work, open bugs, feature requests, and operational items in hldpro-governance.
> The `OVERLORD_BACKLOG.md` at repo root is the cross-repo roadmap mirror; this file is the per-repo execution tracker.

## Plans

| Plan | Issue | Status | Priority | Est. Hours | Deliverables | Notes |
|------|-------|--------|----------|------------|--------------|-------|
| SoM enforcement drift closure epic | #214 | IN PROGRESS | HIGH | TBD | Reviewed PDCAR plan, Claude review artifact, issues #215-#221 | Plan: docs/plans/2026-04-17-som-enforcement-drift-pdcar.md; closeout loop tracked by #220; execution-scope guard tracked by #221 |
| SoM Slice 1: Codex model pin enforcement | #215 | IN PROGRESS | HIGH | TBD | Codex model/reasoning checker, overlord-sweep wiring | Part of #214 |
| SoM Slice 2: ladder and standards consistency | #216 | IN PROGRESS | HIGH | TBD | STANDARDS, exception, progress, registry alignment | Part of #214 |
| SoM Slice 3: cross-review and gate identity enforcement | #217 | IN PROGRESS | HIGH | TBD | v2 gate identity validation and no-self-approval coverage | Part of #214 |
| SoM Slice 4: architecture tier enforcement | #218 | IN PROGRESS | HIGH | TBD | Checkable architecture tier evidence path | Part of #214 |
| SoM Slice 5: packet schema and runtime boundary | #219 | IN PROGRESS | HIGH | TBD | Schema/validator docs, packet tests, runtime boundary correction | Part of #214 |
| SoM Slice 6: operational status and closeout loop | #220 | IN PROGRESS | HIGH | TBD | Progress/backlog/registry/wiki mirrors and closeout evidence contract | This slice |
| SoM Slice 7: execution root and write-scope enforcement | #221 | IN PROGRESS | HIGH | TBD | Execution-scope checker, tests, and PR/slice scope artifacts | Part of #214 |
| Local CI Gate contract hardening | #265 | IN REVIEW | HIGH | 1-2 | Profile validation, shim root override, runbook profile catalog, tests, closeout | Hardens toolkit contracts before more consumer rollout; AIS shim rollout remains separate issue-backed work |
| Stage 5+ som-worker launchd boot-start integration | #104 | PLANNED | MEDIUM | 2-3 | launchd plist, service docs | Gate: local-ai-machine #431, #432 adopt |
| Codex-spark refinement pass on Stage 3b MCP tools + Stage 4 validator | #177 | PLANNED | LOW-MEDIUM | 2-3 | Codex review findings, follow-up issues | Gate: live-fallback rate < 2% confirmed |
| Qwen-Coder MLX driver stub-emission bug | #105 | PLANNED | LOW | 1-2 | MLX driver patch or workaround | Workarounds in docs/runbooks/qwen-coder-driver.md |
| SoM Stage 5: som-worker daemon | #178 | PLANNED | LOW | 6-8 | Daemon implementation, queue wiring | Follow-on to Stage 3b/4 |
| Reconcile ASC-Evaluator exemption with governance.yml | #176 | PLANNED | LOW | 0.5 | Exemption register update or governance.yml fix | Exception SOM-ASC-CI-001 |
| Living Knowledge Base — Phase 8: Qwen3-32B fine-tune | #49 | PLANNED | LOW | TBD | Fine-tuned model, eval results | Gate: 6+ months of wiki data |

## Known Bugs

| Bug | Issue | Priority | Status | Notes |
|-----|-------|----------|--------|-------|
| Qwen-Coder MLX driver emits incomplete stubs on full-file rewrites (>200 lines) | #105 | LOW | OPEN | Workarounds documented in docs/runbooks/qwen-coder-driver.md |

## Feature Requests

| Feature | Issue | Priority | Notes |
|---------|-------|----------|-------|
| Cloud → Local MCP Bridge (remote CLI access to SoM daemon) | #109 | MEDIUM | Deferred; depends on SoM Stage 5 |
| SoM Slice A: codex flag remediation across AIS / HP / LAM / KT | #139 | MEDIUM | Epic: model-pin compliance across governed repos |
| SoM Slice B: AGENTS.md → agents/*.md migration + model pins | #140 | MEDIUM | Follow-on to Slice A |

## Operational Items

| Item | Issue | Status | Notes |
|------|-------|--------|-------|
| hldpro-governance missing docs: SERVICE_REGISTRY.md, DATA_DICTIONARY.md | #172 #173 | IN PROGRESS | Being created in this PR |
| Weekly overlord sweep write-back to wiki/index.md | — | ACTIVE / AWAITING NEXT RUN | Workflow and graph/index write-back path are wired; last committed index remains the 2026-04-09 bootstrap until the next scheduled or manual sweep refreshes generated counts |
| LAM env-var-docs contract debt: SOM_* variables unclassified | #145 | OPEN | local-ai-machine env vars need classification |

## Done

| Item | Issue | Date | Notes |
|------|-------|------|-------|
| AI Integration Services Local CI Gate profile | #264 | 2026-04-17 | PRs #266 and #267 added the planning package, `ai-integration-services` profile, focused profile tests, runbook docs, and closeout. AIS consumer shim rollout is tracked by ai-integration-services #1113. |
| Knocktracker Local CI Gate live profile rollout | #260 | 2026-04-17 | Governance PR #262 added the `knocktracker` profile; knocktracker PR #174 switched the managed shim to live `knocktracker` profile mode. CI remains authoritative. |
| Org-level Local CI Gate toolkit | #253 | 2026-04-17 | PRs #256 and #259 landed the planning package, reusable runner, governance profile, managed shim deployer, runbook, tests, and closeout. Follow-up consumer live enforcement is tracked by #260. |
| Clarify graphify-out artifact contract and ignored-cache noise | #241 | 2026-04-17 | PR #243 clarified canonical tracked graphify artifacts versus local-only cache/OS noise, updated docs and `.gitignore` comments, and expanded the graphify governance contract tests. |
| Enforce planner write-boundary for governance-surface edits | #242 | 2026-04-17 | PRs #244 and #245 split trusted execution-scope bootstrap from implementation. Reusable governance CI now enforces planner-boundary execution scopes from base, `assert_execution_scope.py` validates `execution_mode` and accepted handoff evidence, and the local write gate provides early warnings. |
| Harden verify-completion + codex-spark dispatch briefs against stale-checkout contamination | #174 | 2026-04-17 | GitHub issue is closed; moved out of active Plans to keep the local mirror aligned with canonical issue state |
| Reconcile SoM branch naming vs local-ai-machine riskfix/* convention | #175 | 2026-04-17 | Branch-policy drift resolved by PR #175; active docs now describe the SoM and `riskfix/*` conventions as complementary rather than blocked |
