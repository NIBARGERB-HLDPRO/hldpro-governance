# Overlord Backlog

> Cross-repo governance improvements tracked here. Per-repo work goes in each repo's docs/PROGRESS.md.
> GitHub Issues are the execution backlog/system of record for governance work. This file is the local roadmap/status mirror for cross-repo planning, active issue-backed work, and completed-history entries that still need governance-level visibility.

## Planned

| Item | Priority | Est. Hours | Notes |
|------|----------|-----------|-------|
| Living Knowledge Base — Phase 8: Qwen3-32B fine-tune on wiki data | LOW | TBD | Issue [#49](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/49). Fine-tune Qwen3-32B on wiki data (Karpathy "Train a Custom Model on Wiki Data" step). Gate: wiki must have 6+ months of compounding data minimum. |

## In Progress

None currently. Active governance execution now lives in GitHub Issues; open cross-repo roadmap items remain in the `Planned` table above until a new slice starts.

## Done

| Item | Date | Notes |
|------|------|-------|
| 8-gap governance closure (P0-P6) | 2026-04-01 | All merged. P0: FAIL_FAST_LOG hard gate + schema guard. P1: single source of truth. P2: backlog-first hook. P3: content quality CI. P4: cross-repo deps. P5: rollback runbooks. P6: deploy pipeline. |
| 6 feature PRs merged (v1.5-v1.8) | 2026-04-01 | #233-244: corpus infra, CoS admin, proactive monitoring, reactive conversation, booking pipeline, corpus health + LLM router |
| Cross-repo governance bootstrap (all 4 repos) | 2026-04-01 | CLAUDE.md, PROGRESS.md, FAIL_FAST_LOG.md, hooks, CI workflows |
| verify-completion agent created | 2026-04-01 | Post-incident: false completion report |
| Overlord agents created (overlord, sweep, audit) | 2026-04-01 | ~/.claude/agents/ |
| STANDARDS.md created | 2026-04-01 | ~/.claude/STANDARDS.md |
| Create `hldpro-governance` GitHub repo | 2026-04-05 | Repo live, agents + standards + deps + backlog. Branch merged with fail-fast loop closure standards. |
| Fail-fast loop closure standards | 2026-04-05 | Added to STANDARDS.md — 3 requirements for repos with test/heal cycles |
| Fail-fast loop closure implementation | 2026-04-05 | 3 items: gate surfacing (verified), logs-watcher (cron every 15min), failure-pattern-writeback. memory-writer dedup bug fixed. |
| Overlord-sweep cron | 2026-04-05 | Weekly Monday 9am CT via GitHub Actions. Checks all 5 repos against STANDARDS.md, posts issue report. |
| GitHub Enterprise security | 2026-04-05 | Secret scanning, push protection, dependabot, dependency graph, org rulesets (protect main + develop). |
| Schedule overlord-sweep as recurring agent | 2026-04-05 | Live via GitHub Actions weekly cron in `hldpro-governance`. |
| Branch-safe overlord sweep + session-start Codex backlog surfacing | 2026-04-06 | Merged in PR #9. Added branch-switch guard, worktree-safe sweep execution, and Codex backlog surfacing. Validation issue: [#10](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/10). |
| Overlord sweep production hardening | 2026-04-07 | Merged in PRs #11 and #12. Fixed count normalization crash and aligned ASC-Evaluator handling with exempt status in STANDARDS.md. |
| Harden overlord metrics quality | 2026-04-07 | Merged in PR #16. Full-history checkouts + cross-repo CI token usage now produce real commit and CI metrics in issue [#10](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/10). |
| Nightly overlord cleanup workflow | 2026-04-07 | Merged in PRs #13 and #15. Added nightly artifact cleanup + stale merged branch reporting. Validation issue: [#14](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/14). |
| Codex subagent/persona routing baseline | 2026-04-07 | Updated shared standards and overlord docs so repo-required specialists can be satisfied with spawned Codex subagents/personas mapped from repo-local definitions. |
| GitHub Actions Node 20 deprecation cleanup | 2026-04-07 | Merged in PR #18. Upgraded governance workflows from `actions/checkout@v4` to `actions/checkout@v6`; production sweep run `24059154210` completed without the prior Node 20 deprecation annotation. |
| Operationalize Codex ingestion review flow | 2026-04-09 | Shared helper, auth probe, canary gate, bounded timeout, and stdin/schema review path were already live; a fresh governed-repo validation against `knocktracker` completed successfully and wrote `review-2026-04-09.json`, `qualified-2026-04-09.json`, and `backlog-2026-04-09.md` under a bounded temporary ingestion root. |
| Living Knowledge Base — Phase 1 bootstrap | 2026-04-09 | graphify installed via Python 3.11, CLAUDE/settings pointers added in AIS, git hooks installed in the main AIS checkout, initial AIS code graph built (1883 nodes / 2533 edges / 111 communities), and graph artifacts synced into governance `graphify-out/` + `wiki/hldpro/`. |
| Living Knowledge Base — Phase 2 dispatcher + wiki write-back | 2026-04-09 | `CLAUDE.md` now dispatches instead of answering directly, `wiki/index.md` is the pre-session entrypoint, and overlord agents/sweep are wired for governance-hosted graph/wiki reads and write-back. |
| Living Knowledge Base — Phase 3 Karpathy Loop + closeout hook | 2026-04-09 | `raw/`, `wiki/`, closeout template, `closeout-hook.sh`, raw-feed sync, and weekly graph refresh/write-back are now implemented in governance. |
| Living Knowledge Base — Phase 4 slice (HealthcarePlatform) | 2026-04-09 | Full-repo HealthcarePlatform graph built on isolated worktree via repo-local builder (1549 nodes / 2396 edges / 176 communities), synced into governance `graphify-out/healthcareplatform/` + `wiki/healthcareplatform/`, and Phase 4 governance plan updated to reflect explicit full-repo approval. |
| Living Knowledge Base — Phase 5 slice (ASC-Evaluator) | 2026-04-09 | ASC-Evaluator adopted the governance pointer/hook pattern, and governance now hosts `graphify-out/asc-evaluator/` plus `wiki/asc-evaluator/`. |
| Required-check baseline verification | 2026-04-09 | Issue [#39](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/39). Live PR/workflow review resolved the three open policy questions: knocktracker `governance-check` skip is intentional, local-ai-machine specialized checks stay repo-specific/conditional, HealthcarePlatform `build` is baseline-safe while `playwright-gate` remains conditional. |
| Sprint 1 repo `CODEOWNERS` rollout | 2026-04-09 | Issue [#41](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/41). Default-branch recheck completed and first-wave repo rollout is now finished: AIS was already covered; HealthcarePlatform, knocktracker, and local-ai-machine all merged `.github/CODEOWNERS` on their default branches. |
| Governance doc consistency rollout | 2026-04-09 | Issue [#45](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/45). Shared governance checker and standards contract are now aligned with repo-specific exceptions, and the issue is closed. |
| Effectiveness engine baseline metrics | 2026-04-09 | Issue [#43](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/43). Weekly sweep metrics now persist as reproducible dated and latest snapshots in `metrics/effectiveness-baseline/` via `scripts/overlord/build_effectiveness_metrics.py`. |
| Living Knowledge Base — Phase 6.5: Neo4j runtime bootstrap | 2026-04-09 | Issue [#62](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/62). Governance now has a deterministic local Neo4j bootstrap command in `scripts/knowledge_base/bootstrap_neo4j.sh`, validated against a live Docker-backed runtime on this machine. |
| Living Knowledge Base — Phase 7: Neo4j graph push | 2026-04-09 | Issue [#48](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/48). Governance-hosted `graph.json` now pushes into local Neo4j through `scripts/knowledge_base/push_graph_to_neo4j.py`, with scoped node ids and a documented operator-context mapping contract. |
| Structured agent cycle plan schema org-wide | 2026-04-09 | Issue [#67](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/67). Governance now owns the canonical structured-plan schema and validator, and reusable governance CI can fail invalid `*structured-agent-cycle-plan.json` files before execution-ready issue/riskfix branches proceed. |
| Staged ruleset recommendation pack rollout | 2026-04-09 | Issue [#40](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/40). The draft was replaced with an actionable rollout sequence based on live org/repo ruleset state, exact baseline checks, owner communication, rollback guidance, and current-state drift notes. |
| GitHub governance exception register rollout | 2026-04-09 | Issue [#42](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/42). The register now has explicit approval authority, monthly review cadence, and seeded current exceptions for repo exemptions and conditional-check deferrals. |
| GitHub Enterprise adoption plan closeout | 2026-04-09 | Issue [#44](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/44). The missing adoption-plan artifact was restored, Sprint 1 inventory was reconciled to merged default-branch truth, and future enterprise changes are now routed through specific issue-backed rollout slices instead of a permanently open umbrella plan. |
| Nightly cleanup timezone policy | 2026-04-09 | Issue [#58](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/58). Nightly cleanup now schedules both candidate UTC hours and only executes at 11:00 PM America/Chicago via an in-workflow timezone guard. |
| Living Knowledge Base — Phase 6: remaining governed repos | 2026-04-09 | Issue [#47](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/47). local-ai-machine and knocktracker now follow the governance-hosted graphify pointer/hook pattern, and governance hosts their graph reports, HTML, JSON, and wiki articles. |
| Governance gate wrong diff range under `workflow_call` | 2026-04-09 | Issue [#74](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/74). CODEX-FLAGGED. Base SHA now passed as explicit input to reusable governance workflow. |
| Raw-feed sync republishes unredacted issue bodies | 2026-04-09 | Issue [#75](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/75). CODEX-FLAGGED. Security fix: issue bodies redacted/excluded before commit. |
| Codex finding qualification does not validate cited code | 2026-04-09 | Issue [#76](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/76). CODEX-FLAGGED. `validate_location()` now checks code content matches the finding claim. |
| Weekly sweep silently discards failed pushes | 2026-04-09 | Issue [#77](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/77). CODEX-FLAGGED. `git push \|\| true` replaced with explicit failure handling. |
| Structured agent cycle plan rollout across governed repos | 2026-04-09 | Issue [#68](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/68). HealthcarePlatform schema path converged with governance-owned contract; remaining repos aligned on reusable validator/workflow. |
| Phase 1 critic diff-mode extension | 2026-04-09 | Issue [#411](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/issues/411). PR [#410](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/pull/410). Extended `/v2/critic/evaluate` with diff-mode, `phi_redaction_gate` mask, `caller_mask_policy.json`, SQL migration 036, synthesizer, issue creation worker, 18 contract tests. Follow-up: [#412](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/issues/412) (Phase 1.5 PHI redactor). |
