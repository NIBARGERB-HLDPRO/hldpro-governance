# Data Dictionary

**Last Updated:** 2026-04-16
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
