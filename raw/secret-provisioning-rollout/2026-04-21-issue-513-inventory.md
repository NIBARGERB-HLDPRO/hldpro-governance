# Secret Provisioning UX Rollout Inventory

Date: 2026-04-21
Epic: #507
Issue: #513

This inventory records rollout state only. No downstream repository files were modified in this lane.

| Repo | Status | Finding | Follow-up |
|---|---|---|---|
| HealthcarePlatform | follow_up_required | Direct Wrangler or Cloudflare Pages workflow guidance needs Secret Provisioning UX audit. | HealthcarePlatform#1470 |
| ai-integration-services | follow_up_required | Bespoke marketing deploy gate needs Secret Provisioning UX alignment. | ai-integration-services#1215 |
| local-ai-machine | adopted | Remote MCP operator vault/bootstrap work is already governed by the name-only contract and no-secret evidence rules. | None |
| knocktracker | not_applicable | No known Cloudflare Pages deploy gate, Remote MCP secret provisioning, or cross-repo credential runbook surface in this epic scope. | None |
| seek-and-ponder | follow_up_required | Cloudflare runbook/token guidance needs Secret Provisioning UX scrub. | seek-and-ponder#167 |
| Stampede | follow_up_required | Direct `.env.shared` sourcing guidance should be replaced with bootstrap/provider-vault guidance. | Stampede#120 |
| EmailAssistant | not_applicable | No known Pages deploy gate, Remote MCP, or shared secret provisioning surface in this epic scope. | None |
| ASC-Evaluator | not_applicable | No known Pages deploy gate, Remote MCP, or shared secret provisioning surface in this epic scope. | None |

## Residual Risk

Residual work is intentionally issue-routed. The owning repo must claim its own lane before any file changes land. Evidence for this inventory is name-only and contains no credential values, generated env files, signed URLs, Authorization headers, raw phone numbers, or screenshots.

## Graph/Wiki Expectation

Graph and wiki write-back should occur through the normal governance graph workflow after merge. The inventory itself is the authoritative Stage 6 evidence for #513.
