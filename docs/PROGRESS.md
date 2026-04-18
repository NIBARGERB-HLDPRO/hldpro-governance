# hldpro-governance — Progress & Backlog

**Last Updated:** 2026-04-18
**Scope:** Cross-repo governance standards, CI enforcement, audit agents, and knowledge base infrastructure.

> This file is the single source of truth for planned work, open bugs, feature requests, and operational items in hldpro-governance.
> The `OVERLORD_BACKLOG.md` at repo root is the cross-repo roadmap mirror; this file is the per-repo execution tracker.

## Plans

| Plan | Issue | Status | Priority | Est. Hours | Deliverables | Notes |
|------|-------|--------|----------|------------|--------------|-------|
| Org-level governance tooling distribution epic | #288 | IN PROGRESS | HIGH | TBD | Versioned governance package contract, pull/deploy mechanism, verification matrix, downstream e2e proof | Plan: docs/plans/issue-288-structured-agent-cycle-plan.json; PDCAR: docs/plans/issue-288-org-governance-tooling-distribution-pdcar.md |
| SoM enforcement drift closure epic | #214 | IN PROGRESS | HIGH | TBD | Reviewed PDCAR plan, Claude review artifact, issues #215-#221 | Plan: docs/plans/2026-04-17-som-enforcement-drift-pdcar.md; closeout loop tracked by #220; execution-scope guard tracked by #221 |
| SoM Slice 1: Codex model pin enforcement | #215 | IN PROGRESS | HIGH | TBD | Codex model/reasoning checker, overlord-sweep wiring | Part of #214 |
| SoM Slice 2: ladder and standards consistency | #216 | IN PROGRESS | HIGH | TBD | STANDARDS, exception, progress, registry alignment | Part of #214 |
| SoM Slice 3: cross-review and gate identity enforcement | #217 | IN PROGRESS | HIGH | TBD | v2 gate identity validation and no-self-approval coverage | Part of #214 |
| SoM Slice 4: architecture tier enforcement | #218 | IN PROGRESS | HIGH | TBD | Checkable architecture tier evidence path | Part of #214 |
| SoM Slice 5: packet schema and runtime boundary | #219 | IN PROGRESS | HIGH | TBD | Schema/validator docs, packet tests, runtime boundary correction | Part of #214 |
| SoM Slice 6: operational status and closeout loop | #220 | IN PROGRESS | HIGH | TBD | Progress/backlog/registry/wiki mirrors and closeout evidence contract | This slice |
| SoM Slice 7: execution root and write-scope enforcement | #221 | IN PROGRESS | HIGH | TBD | Execution-scope checker, tests, and PR/slice scope artifacts | Part of #214 |
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
| Governance tooling deployer implementation | #292 | 2026-04-18 | PR #293 added the Phase 2 package deployer, consumer record writes, dry-run/apply/verify/rollback, managed-path safety refusals, Local CI blocker wiring, real temp-repo e2e tests, and generated graph/wiki evidence. Parent epic #288 remains open for downstream pilot and final e2e proof. Closeout: raw/closeouts/2026-04-18-issue-292-governance-tooling-deployer.md. |
| Governance tooling distribution contract | #290 | 2026-04-18 | PR #291 added the Phase 1 package manifest, org distribution runbook, managed-file/override/rollback contract, validation evidence, and closeout. Parent epic #288 remains open for deployer, downstream pilot, and final e2e proof. Closeout: raw/closeouts/2026-04-18-issue-290-governance-tooling-contract.md. |
| Execution environment preflight for active parallel lanes | #286 | 2026-04-18 | PR #287 added active parallel root declarations, a preflight wrapper, and tests proving declared sibling lanes warn while undeclared dirty roots still fail. Closeout: raw/closeouts/2026-04-18-issue-286-execution-environment-preflight.md. |
| Local-first coverage for governance GitHub workflows | #284 | 2026-04-18 | PR #285 added the workflow coverage inventory, deterministic validator, negative-control tests, Local CI Gate wiring, and independent contract workflow coverage. Closeout: raw/closeouts/2026-04-18-issue-284-local-first-workflow-coverage.md. |
| Local CI Gate enforcement remediation | #275 | 2026-04-18 | PR #278 repaired portable shim targeting, live enforcement proof, governance scope fix, changed-file detection, evidence taxonomy, and retrospective audit. Repo-level hardgate wiring is tracked by #277. |
| Local CI Gate repo-level hardgate enforcement | #277 | 2026-04-18 | PR #280 added the CI-visible `local-ci-gate` workflow, YAML-parsed workflow contract tests, and independent graphify-contract coverage. Repo ruleset `15241047` now requires `local-ci-gate` on `main`. |
| Local AI Machine Local CI Gate profile | #272 | 2026-04-18 | Added governance-owned `local-ai-machine` profile, focused changed-file scope tests, runbook catalog docs, and closeout. LAM shim rollout remains separate issue-backed work. |
| Local CI Gate consumer rollout checklist | #270 | 2026-04-18 | PR #271 added the standard issue-backed consumer rollout sequence to the Local CI Gate toolkit runbook. |
| Local CI Gate contract hardening | #265 | 2026-04-18 | Added profile dependency metadata, duplicate check-id validation, managed shim `HLDPRO_GOVERNANCE_ROOT` override, deployer/runner tests, runbook catalog, and closeout. |
| AI Integration Services Local CI Gate profile | #264 | 2026-04-17 | PRs #266 and #267 added the planning package, `ai-integration-services` profile, focused profile tests, runbook docs, and closeout. AIS consumer shim rollout is tracked by ai-integration-services #1113. |
| Knocktracker Local CI Gate live profile rollout | #260 | 2026-04-17 | Governance PR #262 added the `knocktracker` profile; knocktracker PR #174 switched the managed shim to live `knocktracker` profile mode. CI remains authoritative. |
| Org-level Local CI Gate toolkit | #253 | 2026-04-17 | PRs #256 and #259 landed the planning package, reusable runner, governance profile, managed shim deployer, runbook, tests, and closeout. Follow-up consumer live enforcement is tracked by #260. |
| Clarify graphify-out artifact contract and ignored-cache noise | #241 | 2026-04-17 | PR #243 clarified canonical tracked graphify artifacts versus local-only cache/OS noise, updated docs and `.gitignore` comments, and expanded the graphify governance contract tests. |
| Enforce planner write-boundary for governance-surface edits | #242 | 2026-04-17 | PRs #244 and #245 split trusted execution-scope bootstrap from implementation. Reusable governance CI now enforces planner-boundary execution scopes from base, `assert_execution_scope.py` validates `execution_mode` and accepted handoff evidence, and the local write gate provides early warnings. |
| Harden verify-completion + codex-spark dispatch briefs against stale-checkout contamination | #174 | 2026-04-17 | GitHub issue is closed; moved out of active Plans to keep the local mirror aligned with canonical issue state |
| Reconcile SoM branch naming vs local-ai-machine riskfix/* convention | #175 | 2026-04-17 | Branch-policy drift resolved by PR #175; active docs now describe the SoM and `riskfix/*` conventions as complementary rather than blocked |
