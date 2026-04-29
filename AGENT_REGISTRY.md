# AGENT_REGISTRY.md
<!-- registry-source: this file -->
<!-- policy-source: STANDARDS.md §DA -->
<!-- on-conflict: STANDARDS.md §DA wins -->

Cross-repo canonical inventory of all Claude-native agents. Updated when agents are added/removed.
Self-approval prohibited. Orchestrator may not perform tasks owned by Tier 2 agents.

| Agent | Repo | Tier | Role | Model | Max Loops | Write Paths |
|-------|------|------|------|-------|-----------|-------------|
| overlord-sweep | hldpro-governance | 0 | supervisor | sonnet | 3 | reports/ |
| som-worker-triage | hldpro-governance | 1 | worker | haiku | 1 | (read-only) |
| sim-runner | hldpro-governance | 2 | worker | sonnet | 1 | raw/packets/outbound/ |
| gov-specialist-planner | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ |
| gov-specialist-auditor | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ |
| gov-specialist-qa | hldpro-governance | 2 | worker | gpt-5.4-mini | 1 | raw/packets/outbound/ |
| gov-specialist-local-repo-researcher | hldpro-governance | 2 | worker | gpt-5.4-mini | 1 | raw/packets/outbound/ |
| gov-specialist-web-researcher | hldpro-governance | 2 | worker | gpt-5.4 | 1 | raw/packets/outbound/ |
| hldpro-watcher | ai-integration-services | 1 | supervisor | sonnet | 3 | .claude/agents/output/ + ../hldpro-governance/reports/ai-integration-services/ |
| migration-validator | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/migration-validator/ |
| edge-fn-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/edge-fn-reviewer/ |
| schema-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/schema-reviewer/ |
| test-writer | ai-integration-services | 2 | worker | sonnet | 1 | e2e/ __tests__/ .claude/agents/output/test-writer/ |
| diagram-writer | ai-integration-services | 2 | worker | sonnet | 1 | docs/diagrams/ .claude/agents/output/diagram-writer/ |
| docs-writer | ai-integration-services | 2 | worker | sonnet | 1 | docs/narratives/ .claude/agents/output/docs-writer/ |
| codex-reviewer | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/codex-reviewer/ |
| debug-researcher | ai-integration-services | 2 | worker | sonnet | 1 | (read-only) |
| doc-audit-agent | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ |
| preflight-probe | ai-integration-services | 2 | worker | haiku | 1 | (read-only) |
| report-orchestrator | ai-integration-services | 2 | worker | sonnet | 1 | .claude/agents/output/report-orchestrator/ |
| debug-researcher | local-ai-machine | 2 | worker | sonnet | 1 | (read-only) |
| doc-audit-agent | local-ai-machine | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ |
| debug-researcher | HealthcarePlatform | 2 | worker | sonnet | 1 | (read-only) |
| doc-audit-agent | HealthcarePlatform | 2 | worker | sonnet | 1 | .claude/agents/output/doc-audit-agent/ |
