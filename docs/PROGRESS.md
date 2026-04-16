# hldpro-governance — Progress & Backlog

**Last Updated:** 2026-04-16
**Scope:** Cross-repo governance standards, CI enforcement, audit agents, and knowledge base infrastructure.

> This file is the single source of truth for planned work, open bugs, feature requests, and operational items in hldpro-governance.
> The `OVERLORD_BACKLOG.md` at repo root is the cross-repo roadmap mirror; this file is the per-repo execution tracker.

## Plans

| Plan | Issue | Status | Priority | Est. Hours | Deliverables | Notes |
|------|-------|--------|----------|------------|--------------|-------|
| Harden verify-completion + codex-spark dispatch briefs against stale-checkout contamination | #174 | IN PROGRESS | HIGH | 2-3 | `check-pr-commit-scope.yml`, `check_pr_commit_scope.sh`, STANDARDS.md update | 2026-04-15 incident; (a)+(b) already on main; (c) PR #182 |
| Reconcile SoM branch naming vs local-ai-machine riskfix/* convention | #175 | PLANNED | MEDIUM | 1-2 | STANDARDS.md update, exception register update | Exception SOM-LAM-BRANCH-001 defers enforcement |
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
| Weekly overlord sweep write-back to wiki/index.md | — | PENDING | Last sweep was 2026-04-09; needs live GH Actions run |
| LAM env-var-docs contract debt: SOM_* variables unclassified | #145 | OPEN | local-ai-machine env vars need classification |
