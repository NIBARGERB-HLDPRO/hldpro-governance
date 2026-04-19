# hldpro-governance — Progress & Backlog

**Last Updated:** 2026-04-19
**Scope:** Cross-repo governance standards, CI enforcement, audit agents, and knowledge base infrastructure.

> This file is the single source of truth for planned work, open bugs, feature requests, and operational items in hldpro-governance.
> The `OVERLORD_BACKLOG.md` at repo root is the cross-repo roadmap mirror; this file is the per-repo execution tracker.

## Plans

| Plan | Issue | Status | Priority | Est. Hours | Deliverables | Notes |
|------|-------|--------|----------|------------|--------------|-------|
| Fix execution-scope validation in detached PR checkouts | #324 | IN PROGRESS | HIGH | 1 | Branch fallback in `assert_execution_scope.py`, regression test, EmailAssistant#1 unblock | Planning scope: docs/plans/issue-324-structured-agent-cycle-plan.json |
| Org-wide active repository governance coverage epic | #298 | IN PROGRESS | HIGH | TBD | Active org repo registry policy, live inventory drift detector, seek-and-ponder intake, EmailAssistant discovery, registry-driven surface reconciliation, final e2e closeout gate | Final closeout PR pending for #314; plan: docs/plans/issue-298-structured-agent-cycle-plan.json |
| Always-on SoM HITL relay for local CLI sessions | #296 | IN PROGRESS | HIGH | TBD | HITL packet contracts, AIS notification bridge, SoM/MCP response normalization, structured session instruction flow, final e2e proof | Plan: docs/plans/issue-296-structured-agent-cycle-plan.json; PDCAR: docs/plans/issue-296-som-hitl-relay-pdcar.md |
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
| Codex review template default persona path repair | #337 | 2026-04-19 | Restored `docs/agents/codex-reviewer.md`, preserved `CODEX_REVIEW_PERSONA` override coverage, added fake-Codex default-path e2e proof that audit reaches `codex-fire.sh`, and recorded validation/closeout evidence. |
| seek-and-ponder registry memory-integrity follow-up | #331 | 2026-04-19 | `seek-and-ponder` memory_integrity is enabled in the governed repo registry after downstream seek-and-ponder#23 memory bootstrap. Validation and closeout are recorded in `raw/validation/2026-04-19-issue-331-seek-ponder-memory-registry.md` and `raw/closeouts/2026-04-19-issue-331-seek-ponder-memory-registry.md`. |
| Governance tooling package v0.1.0 release coordinate | #332 | 2026-04-19 | Documents the first package release tag `governance-tooling-v0.1.0`, preserves mandatory SHA pinning in consumer records, validates package docs through local gates and PR GitHub Actions, and creates the annotated tag after merge. |
| Org-level governance tooling distribution epic | #288 | 2026-04-19 | Planning PR #289, contract PR #291, deployer PR #293, and downstream pilot planning PR #295 landed the package contract, deployer, and pilot plan. Final downstream e2e AC was satisfied through fallback consumer knocktracker after local-ai-machine#461 halted before writes on unrelated startup preflight/global worktree hygiene blockers. Fallback proof: knocktracker#175, knocktracker PR #176, merge `8c035a28347575a699b3d564b5c13df69501d72b`, governance package ref `3a0adef059ce8593767810f0f4cdd8bccddd180d`, deployer dry-run/apply/verify, generated consumer record, managed shim invocation, negative-control local blocker, local pass after remediation, rollback/reapply proof, and downstream GitHub Actions pass. Closeout: raw/closeouts/2026-04-19-issue-288-governance-tooling-distribution-final.md. |
| Downstream governance tooling pilot planning | #294 | 2026-04-18 | PR #295 added the downstream pilot plan selecting local-ai-machine by default, defining fallback criteria, and requiring final e2e evidence before parent #288 closeout. Final downstream proof was later recorded on #288 and mirrored in raw/closeouts/2026-04-19-issue-288-governance-tooling-distribution-final.md. |
| Final org repo governance e2e closeout | #298 #314 | 2026-04-19 | Final gate proved live org inventory coverage, registry validation, graphify/registry-surface reconciliation, compendium generation, subsystem selections, memory integrity, metrics smoke, branch/ruleset evidence, Stage 6 closeout, and Local CI evidence. Residual downstream work remains issue-backed by seek-and-ponder#23, EmailAssistant#1, and #176. |
| Registry-driven surface reconciliation | #313 | 2026-04-19 | PR #320 reconciled workflow/document/helper surfaces with the governed repo registry and added `validate_registry_surfaces.py` to CI/local gates. |
| EmailAssistant discovery and classification | #312 | 2026-04-19 | PR #319 added adoption-blocked registry coverage, sensitive municipal email classification, live inventory closure, downstream blocker EmailAssistant#1, and review/validation evidence. Parent epic #298 remains open. |
| seek-and-ponder governance intake | #311 | 2026-04-19 | PR #318 added seek-and-ponder registry, graph/wiki artifacts, branch/ruleset/check evidence, live inventory reduction, downstream follow-up in seek-and-ponder#23, and review/validation evidence. Parent epic #298 remains open. |
| Governed repo classification schema | #310 | 2026-04-19 | PR #317 added schema-enforced lifecycle/governance classifications, validator and inventory drift tests, archived lifecycle handling, and Claude review evidence. Parent epic #298 remains open. |
| Org inventory drift detector | #309 | 2026-04-18 | PR #315 added fixture/live org inventory drift detection, weekly sweep warn-only reporting, and evidence that seek-and-ponder and EmailAssistant remain missing active repos pending #311/#312. Parent epic #298 remains open. |
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
