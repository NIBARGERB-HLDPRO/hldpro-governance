# Data Dictionary

**Last Updated:** 2026-04-17
**Scope:** hldpro-governance — meta-governance repo
**Source of truth:** This file documents the canonical schemas, file formats, and data contracts owned or enforced by hldpro-governance. Schema JSON/YAML source files live in `docs/schemas/`.

---

## Schemas

### Structured Agent Cycle Plan
**File:** `docs/schemas/structured-agent-cycle-plan.schema.json`
**Used by:** All governed repos — issue-driven execution branches must have a valid plan before execution is governance-ready.
**Validator:** `scripts/overlord/validate_structured_agent_cycle_plan.py`

Key fields:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sprint` | string | yes | Sprint identifier |
| `task` | string | yes | Task description |
| `acceptance` | array | yes | Acceptance criteria list |
| `specialist_reviews` | array | yes | Required reviewer roles |
| `alternate_model_review` | object | yes | Cross-model review result |
| `execution_handoff` | object | yes | Handoff chain record |
| `material_deviation_rules` | array | yes | Allowed deviation conditions |

---

### SoM Packet
**File:** `docs/schemas/som-packet.schema.yml`
**Used by:** MCP daemon (local-ai-machine), all tier handoffs in the Society of Minds routing chain.

Key fields: `tier`, `model_id`, `model_family`, `payload`, `pii_cleared`, `audit_ref`

---

### Graphify Usage Event
**File:** `docs/schemas/graphify-usage-event.schema.json`
**Used by:** `scripts/knowledge_base/log_graphify_usage.py`, `scripts/knowledge_base/measure_graphify_usage.py`
**Storage:** `metrics/graphify-usage/events/YYYY-MM-DD.jsonl` (append-only)

Key fields:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | string (ISO 8601) | yes | Event time |
| `repo` | string | yes | Target repo |
| `task_id` | string | yes | Issue or task identifier |
| `task_type` | string | yes | e.g. `architecture_retrieval`, `workflow_bug` |
| `strategy` | string | yes | `graphify`, `repo-search`, or `hybrid` |
| `artifacts` | array | yes | Files/paths used as context |
| `estimated_tokens` | integer | yes | Token footprint estimate |
| `experiment_id` | string | no | A/B experiment grouping |
| `session_id` | string | no | Session identifier |
| `prompt` | string | no | Query prompt text |
| `query_terms` | array | no | Search terms used |
| `top_candidates` | array | no | Top-ranked files returned |

---

### OVERLORD_BACKLOG.md Planned Table
**Owner:** hldpro-governance root
**Enforced by:** `check-backlog-gh-sync.yml`

Required columns: `Item`, `Issue`, `Priority`, `Est. Hours`, `Notes`

Contract: Every Planned row must reference an open GitHub issue (`#NNN`). GH is canonical — create the issue before adding to Planned.

---

### FAIL_FAST_LOG / Error Patterns
**File:** `docs/FAIL_FAST_LOG.md`, `docs/ERROR_PATTERNS.md`
**Schema:** `docs/schemas/fail-fast-log.schema.md`, `docs/schemas/error-patterns.schema.md`

Standard columns: `Date`, `Repo`, `Error`, `Root Cause`, `Fix`, `Prevention`

---

### Org Governance Compendium
**File:** `docs/ORG_GOVERNANCE_COMPENDIUM.md`
**Generator:** `scripts/overlord/build_org_governance_compendium.py`
**Refresh path:** weekly `overlord-sweep.yml`

Contract:
- Generated from canonical governed repos only.
- Excludes `_worktrees/` and issue-specific local clones.
- Indexes governance/rules files by repo with category, description, logic, and detected interactions.
- Includes graphify node/community summaries from `graphify-out/<repo>/`.
- `--check` mode fails when the generated markdown is stale.

---

### Governed Repo Registry
**File:** `docs/governed_repos.json`
**Schema:** `docs/schemas/governed-repos.schema.json`
**Validator:** `scripts/overlord/validate_governed_repos.py`

Contract:
- One row per governed repository.
- Required identity fields: `repo_slug`, `display_name`, `repo_dir_name`, and `github_repo`.
- Required path fields: `local_path`, `ci_checkout_path`, `graph_output_path`, `wiki_path`, and `project_path`.
- Required classification fields: `governance_tier`, `security_tier`, and `enabled_subsystems`.
- Graphify targets must reconcile with registry graph output, wiki path, display name, and CI checkout path.
- Temporary duplicate-list exemptions are documented in `docs/governed_repos_exemptions.md`.

---

### Governance-Surface Planning Gate
**Validator:** `scripts/overlord/validate_structured_agent_cycle_plan.py`
**CI:** `.github/workflows/governance-check.yml`
**Local hook:** `hooks/code-write-gate.sh`
**Execution scope guard:** `scripts/overlord/assert_execution_scope.py`

Governance-surface paths include repo rules, standards, workflow files, hooks, agent definitions, schemas, registries, closeouts, cross-review artifacts, graphify/wiki outputs, and overlord/knowledge-base scripts.

Contract:
- Changed governance-surface paths require an issue branch whose branch name contains `issue-<number>`.
- The repo must contain a matching canonical `*structured-agent-cycle-plan.json` whose `issue_number` equals that branch issue number.
- The matching plan must be approved and have `execution_handoff.execution_mode` set to `implementation_ready` or `implementation_complete`.
- If `alternate_model_review.required` is true, status must be `accepted` or `accepted_with_followup`.
- Local execution scope validation declares expected checkout root, branch, allowed write paths, and forbidden dirty roots.

---

### Read-Only Governance Observer Report
**Generator:** `scripts/orchestrator/read_only_observer.py`
**Default storage:** `projects/<repo_slug>/reports/latest.json` and `projects/<repo_slug>/reports/latest.md`
**launchd template:** `launchd/com.hldpro.governance-observer.plist`

Contract:
- One report per governed repo listed in `docs/governed_repos.json`.
- Writes only under `projects/<repo_slug>/reports/` by default.
- Does not write to `raw/packets/` and records `packet_enqueue_enabled: false`.
- Includes `repo_slug`, `display_name`, `generated_at`, `source_commit`, `health`, `stale_knowledge`, `planning_gate`, `daemon_readiness`, and `artifacts`.
- Artifact entries include relative path, existence, SHA-256 hash when present, and detail text.
- Reports use local metadata-only issue feed files from `raw/github-issues/` when present; issue bodies are not read.
