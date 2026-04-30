# AGENT_REGISTRY.md
<!-- registry-source: this file -->
<!-- policy-source: STANDARDS.md §DA -->
<!-- on-conflict: STANDARDS.md §DA wins -->

Cross-repo canonical inventory of all Claude-native agents. Updated when agents are added/removed.
Self-approval prohibited. Orchestrator may not perform tasks owned by Tier 2 agents.

| Agent | Repo | Tier | Role | Model | Max Loops | Write Paths | Authority |
|-------|------|------|------|-------|-----------|-------------|-----------|
| overlord | hldpro-governance | 0 | supervisor | haiku | 1 | (read-only) | read-only |
| overlord-sweep | hldpro-governance | 0 | supervisor | sonnet | 3 | reports/ | bounded: wiki/index.md, OVERLORD_BACKLOG.md, raw/ |
| overlord-audit | hldpro-governance | 0 | supervisor | sonnet | 1 | (read-only) | read-only |
| verify-completion | hldpro-governance | 1 | worker | haiku | 1 | (read-only) | read-only |
| som-worker-triage | hldpro-governance | 1 | worker | haiku | 1 | (read-only) | read-only |
| codex-brief | hldpro-governance | 2 | worker | haiku | 1 | raw/packets/inbound/ | bounded: raw/packets/inbound/ |
| issue-lane-bootstrap | hldpro-governance | 2 | worker | haiku | 1 | raw/execution-scopes/ | bounded: raw/execution-scopes/ |
| backlog-promoter | hldpro-governance | 2 | worker | claude-sonnet-4-6 | 1 | docs/PROGRESS.md docs/FAIL_FAST_LOG.md | bounded: docs/PROGRESS.md, docs/FAIL_FAST_LOG.md |
| sim-runner | hldpro-governance | 2 | worker | sonnet | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| gov-specialist-planner | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| gov-specialist-auditor | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| gov-specialist-qa | hldpro-governance | 2 | worker | gpt-5.4-mini | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| gov-specialist-local-repo-researcher | hldpro-governance | 2 | worker | gpt-5.4-mini | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| gov-specialist-web-researcher | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ | bounded: raw/packets/outbound/ |
| hldpro-watcher | ai-integration-services | 1 | supervisor | sonnet | 3 | .claude/agents/output/ + ../hldpro-governance/reports/ai-integration-services/ | bounded: .claude/agents/output/, reports/ |
| migration-validator | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/migration-validator/ | bounded: .claude/agents/output/migration-validator/ |
| edge-fn-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/edge-fn-reviewer/ | bounded: .claude/agents/output/edge-fn-reviewer/ |
| schema-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/schema-reviewer/ | bounded: .claude/agents/output/schema-reviewer/ |
| test-writer | ai-integration-services | 2 | worker | sonnet | 1 | e2e/ __tests__/ .claude/agents/output/test-writer/ | bounded: e2e/, __tests__/, .claude/agents/output/test-writer/ |
| diagram-writer | ai-integration-services | 2 | worker | sonnet | 1 | docs/diagrams/ .claude/agents/output/diagram-writer/ | bounded: docs/diagrams/, .claude/agents/output/diagram-writer/ |
| docs-writer | ai-integration-services | 2 | worker | sonnet | 1 | docs/narratives/ .claude/agents/output/docs-writer/ | bounded: docs/narratives/, .claude/agents/output/docs-writer/ |
| codex-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/codex-reviewer/ | bounded: .claude/agents/output/codex-reviewer/ |
| debug-researcher | ai-integration-services | 2 | worker | sonnet | 1 | (read-only) | read-only |
| doc-audit-agent | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ | bounded: .claude/agents/output/doc-audit-agent/ |
| preflight-probe | ai-integration-services | 2 | worker | haiku | 1 | (read-only) | read-only |
| report-orchestrator | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/report-orchestrator/ | bounded: .claude/agents/output/report-orchestrator/ |
| debug-researcher | local-ai-machine | 2 | worker | sonnet | 1 | (read-only) | read-only |
| doc-audit-agent | local-ai-machine | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ | bounded: .claude/agents/output/doc-audit-agent/ |
| debug-researcher | HealthcarePlatform | 2 | worker | sonnet | 1 | (read-only) | read-only |
| doc-audit-agent | HealthcarePlatform | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ | bounded: .claude/agents/output/doc-audit-agent/ |
