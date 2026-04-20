# Service Registry

**Last Updated:** 2026-04-20
**Scope:** hldpro-governance — meta-governance repo
**Source of truth:** This file inventories the scripts, agents, CI workflows, and hooks that constitute the active "services" enforced or provided by hldpro-governance across the governed org.

---

## Agents

| Agent | File | Model | Role |
|-------|------|-------|------|
| overlord | `agents/overlord.md` | claude-sonnet-4-6 | Session-start standards drift check |
| overlord-sweep | `agents/overlord-sweep.md` | claude-sonnet-4-6 | Weekly cross-repo audit + metrics |
| overlord-audit | `agents/overlord-audit.md` | claude-sonnet-4-6 | Deep cross-repo pattern analysis |
| verify-completion | `agents/verify-completion.md` | claude-haiku-4-5-20251001 | Hard-gate artifact verification |

---

## CI Workflows (Reusable / Governance)

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| governance-check | `.github/workflows/governance-check.yml` | PR / push | Doc co-staging, structured planning, governance-surface, planner write-boundary, and registry gates |
| check-backlog-gh-sync | `.github/workflows/check-backlog-gh-sync.yml` | PR / push (OVERLORD_BACKLOG.md) | Backlog ↔ GH issue sync gate |
| check-pr-commit-scope | `.github/workflows/check-pr-commit-scope.yml` | PR to main | Stale-worktree contamination guard |
| remote-mcp-live-health | `.github/workflows/remote-mcp-live-health.yml` | Daily / manual | Recurring Remote MCP fixture harness and optional configured live health/audit monitor; local launchd is the selected live-authoritative surface |
| overlord-sweep | `.github/workflows/overlord-sweep.yml` | Weekly (Mon 9am CT) | Cross-repo standards sweep |
| overlord-nightly-cleanup | `.github/workflows/overlord-nightly-cleanup.yml` | Nightly | Stale branch cleanup |
| graphify-governance-contract | `.github/workflows/graphify-governance-contract.yml` | PR / push | Graphify usage logging contract tests |
| require-cross-review | `.github/workflows/require-cross-review.yml` | PR | Dual-planner cross-review artifact gate |
| check-agent-model-pins | `.github/workflows/check-agent-model-pins.yml` | PR | SoM Tier enforcement: agent model pins |
| check-no-self-approval | `.github/workflows/check-no-self-approval.yml` | PR | SoM invariant #1: no self-approval |
| check-remote-mcp-audit-schema | `.github/workflows/check-remote-mcp-audit-schema.yml` | PR / manual | Remote MCP audit hash-chain, HMAC, and manifest validation |

---

## Overlord Scripts

| Script | Path | Purpose |
|--------|------|---------|
| validate_backlog_gh_sync.py | `scripts/overlord/validate_backlog_gh_sync.py` | Validates OVERLORD_BACKLOG.md Planned rows reference open GH issues |
| validate_structured_agent_cycle_plan.py | `scripts/overlord/validate_structured_agent_cycle_plan.py` | Validates structured plan JSON against org schema |
| assert_execution_scope.py | `scripts/overlord/assert_execution_scope.py` | Asserts issue work runs from the declared root/branch, enforces planning-only `allowed_write_paths`, and requires accepted pinned-agent handoff evidence for non-planning diffs |
| validate_governed_repos.py | `scripts/overlord/validate_governed_repos.py` | Validates `docs/governed_repos.json` and reconciles it with graphify targets |
| governed_repos.py | `scripts/overlord/governed_repos.py` | Shared adapter for executable governed repo registry consumers |
| codex_ingestion.py | `scripts/overlord/codex_ingestion.py` | Codex review ingestion: generate, qualify, promote |
| build_effectiveness_metrics.py | `scripts/overlord/build_effectiveness_metrics.py` | Weekly effectiveness baseline snapshots |
| build_org_governance_compendium.py | `scripts/overlord/build_org_governance_compendium.py` | Generates the org-level governance rules compendium from canonical governed repos |
| worktree_shared_dependencies.sh | `scripts/overlord/worktree_shared_dependencies.sh` | Approved dependency symlink helper for worktrees |
| audit_remote.sh | `scripts/overlord/audit_remote.sh` | Reads a file from any repo's remote HEAD via GH API |

---

## Orchestrator Scripts

| Script | Path | Purpose |
|--------|------|---------|
| read_only_observer.py | `scripts/orchestrator/read_only_observer.py` | Generates deterministic read-only governance health reports under `projects/<repo_slug>/reports/` |
| packet_queue.py | `scripts/orchestrator/packet_queue.py` | Validates and transitions governance packets through auditable filesystem queue states without executing payloads |
| self_learning.py | `scripts/orchestrator/self_learning.py` | Looks up cited prior mistake patterns, enriches packets, records novel failures append-only, and builds weekly learning reports |

---

## Local Runtime Scripts

| Script | Path | Purpose |
|--------|------|---------|
| runtime_inventory.py | `scripts/lam/runtime_inventory.py` | No-payload Mac/Windows model runtime and PII guardrail inventory |

## Remote MCP Scripts

| Script | Path | Purpose |
|--------|------|---------|
| som_client.py | `scripts/som-client/som_client.py` | Thin Remote MCP operator client with Cloudflare Access headers, `SOM_MCP_TOKEN` / `SOM_REMOTE_MCP_JWT` bearer auth, safe errors, and retry handling |
| verify_audit.py | `scripts/remote-mcp/verify_audit.py` | Deterministic verifier for Remote MCP audit JSONL hash chains, HMACs, and manifests |
| operator_connectivity.py | `scripts/remote-mcp/operator_connectivity.py` | No-secret fixture/live operator preflight for `som.ping` request/response readiness, launchd status, missing live config names, and recommended action |
| operator_inbound_preflight.py | `scripts/remote-mcp/operator_inbound_preflight.py` | No-secret fixture/live operator-message receive preflight for the HITL relay session inbox path, missing live queue config names, and recommended action |
| live_health_monitor.py | `scripts/remote-mcp/live_health_monitor.py` | Recurring Remote MCP monitor composing Stage D smoke/security checks, strict audit verification, tamper-negative proof, and evidence-safety scan |
| monitor_alert.py | `scripts/remote-mcp/monitor_alert.py` | Payload-safe alert/report formatter for Remote MCP monitor JSON results |

---

## launchd Templates

| Label | File | Purpose |
|-------|------|---------|
| com.hldpro.governance-observer | `launchd/com.hldpro.governance-observer.plist` | Optional macOS user-agent template for periodic read-only observer runs |
| com.hldpro.remote-mcp-monitor | `launchd/com.hldpro.remote-mcp-monitor.plist` | Selected macOS live operating-mode template for recurring Remote MCP health and audit monitor runs; runs monitor `--mode live` so missing live inputs fail closed |

---

## Knowledge Base Scripts

| Script | Path | Purpose |
|--------|------|---------|
| build_graph.py | `scripts/knowledge_base/build_graph.py` | Builds graphify knowledge graph for a repo |
| graphify_hook_helper.py | `scripts/knowledge_base/graphify_hook_helper.py` | Resolves manifest-defined graphify paths, dry-runs refresh commands, and installs managed graphify refresh hooks into governed repo checkouts |
| log_graphify_usage.py | `scripts/knowledge_base/log_graphify_usage.py` | Appends graphify usage events to JSONL log |
| measure_graphify_usage.py | `scripts/knowledge_base/measure_graphify_usage.py` | A/B comparison: graphify vs repo-search retrieval |
| update_knowledge_index.py | `scripts/knowledge_base/update_knowledge_index.py` | Regenerates wiki/index.md from graph summaries |

---

## Hooks

| Hook | Path | Scope | Purpose |
|------|------|-------|---------|
| code-write-gate.sh | `hooks/code-write-gate.sh` | Local Claude Code write hook | Blocks unplanned governance-surface writes, enforces SoM new-code routing, and surfaces planner-boundary drift as early warning (CI is authoritative) |
| closeout-hook.sh | `hooks/closeout-hook.sh` | Repo-wide | Validates closeout artifact on Stage 6 completion |
