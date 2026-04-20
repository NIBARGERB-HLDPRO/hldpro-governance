# Data Dictionary

**Last Updated:** 2026-04-20
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

Key fields:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `packet_id` | string (UUID) | yes | Unique packet identifier |
| `parent_packet_id` | string or null | no | Parent packet identifier for chain validation |
| `prior.tier` | integer | yes | Source tier |
| `prior.role` | string | yes | Source role, including LAM worker/critic roles |
| `prior.model_id` | string | yes | Exact model identifier |
| `prior.model_family` | string | yes | Model family used for cross-family and LAM diversity checks |
| `next_tier` | integer | yes | Destination tier |
| `artifacts` | array | no | Packet artifact references |
| `standards_ref` | string | yes | Standards section governing the handoff |
| `fallback_ladder_ref` | string or null | no | Existing fallback log reference under `raw/model-fallbacks/` when present |
| `governance` | object | no | Optional dispatch metadata required by the packet queue before execution |

`governance` dispatch fields:
| Field | Type | Required when `governance` exists | Description |
|-------|------|------------------------------------|-------------|
| `issue_number` | integer | yes | GitHub issue authorizing dispatch |
| `structured_plan_ref` | string | yes | Repo-relative structured plan path |
| `execution_scope_ref` | string or null | yes | Scope evidence path under `raw/execution-scopes/*.json`, or null when scope is captured in the plan |
| `validation_commands` | array | yes | Commands required before packet closeout |
| `review_artifacts` | array | yes | Review or gate artifacts required by the packet |
| `fallback_log_ref` | string or null | yes | Queue-level fallback log reference, or null when no fallback occurred |
| `pii_mode` | enum | yes | `none`, `tagged`, `detected`, or `lam_only` |
| `dispatch_authorized` | boolean | yes | True only after issue-backed plan approval and scope review |
| `dry_run_authorized` | boolean | no | True when a packet may dry-run through dispatch validation without live dispatch authority |
| `known_failure_context` | array | no | Prior mistake patterns injected by `scripts/orchestrator/self_learning.py` |

The schema keeps `governance` optional so existing stage-4 packets remain valid. `scripts/orchestrator/packet_queue.py` requires and enforces the full governance object before dispatch.

---

### Packet Queue State And Audit
**Generator:** `scripts/orchestrator/packet_queue.py`
**Storage:** `raw/packets/queue/`
**Audit log:** `raw/packets/queue/audit.jsonl`

Queue states:
| State | Description |
|-------|-------------|
| `inbound` | Validated packet is waiting for dispatch eligibility checks |
| `dispatched` | Packet has passed dispatch validation and can be handled by the next controlled worker layer |
| `review` | Packet output is ready for review |
| `gate` | Packet output passed review and is awaiting gate decision |
| `done` | Packet lifecycle is complete |
| `halted` | Packet is stopped before dispatch or completion |

Allowed transitions: `inbound -> dispatched`, `inbound -> halted`, `dispatched -> review`, `dispatched -> halted`, `review -> gate`, `review -> halted`, `gate -> done`, and `gate -> halted`.

Audit event fields:
| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | UTC event timestamp |
| `packet_id` | string or null | Packet identifier when readable |
| `from_state` | string | Source queue state |
| `to_state` | string | Requested destination state |
| `dry_run` | boolean | True when no packet file was moved |
| `allowed` | boolean | Whether the transition was accepted |
| `status` | string | `dry_run`, `moved`, `refused`, or `halted` |
| `reason` | string | Human-readable decision reason |
| `source` | string | Source packet path |
| `destination` | string or null | Destination packet path |
| `sha256` | string or null | Source packet hash when readable |

Contract:
- Packet schema validation runs before any state move.
- `inbound -> dispatched` additionally requires an approved issue-backed structured plan with implementation-ready handoff.
- When `governance.execution_scope_ref` is present, it must resolve to a JSON execution-scope artifact under `raw/execution-scopes/`; arbitrary existing files such as PDCAR Markdown do not satisfy dispatch scope evidence.
- Packets with `dry_run_authorized: true` and `dispatch_authorized: false` may pass dry-run dispatch validation only; live dispatch still refuses.
- PII modes `tagged`, `detected`, and `lam_only` require `worker-lam` or `critic-lam` role before dispatch.
- `known_failure_context` entries with `repeat_count >= 2` halt dispatch for planning-gate escalation.
- Dry-run transitions write audit events and never execute packet payloads.
- Replay reads the audit log and reconstructs latest accepted packet states.

---

### Remote MCP Monitor Result
**Generator:** `scripts/remote-mcp/live_health_monitor.py`
**Workflow:** `.github/workflows/remote-mcp-live-health.yml`
**Optional scheduler:** `launchd/com.hldpro.remote-mcp-monitor.plist`

Result object fields:
| Field | Type | Description |
|-------|------|-------------|
| `mode` | enum | `fixture` or `live` after auto-mode resolution |
| `results` | array | Stage D proof results plus monitor-specific evidence scan |
| `evidence_dir` | string | Directory scanned for preserved audit evidence |

Each `results[]` entry contains:
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Check name, such as `authenticated-ping`, `audit-valid`, or `evidence-safety-scan` |
| `status` | enum | `pass`, `fail`, or `skip` |
| `detail` | string | Payload-safe detail; never token material or raw user payloads |

Contract:
- `auto` mode runs live only when live configuration markers are present; otherwise it runs fixture mode.
- Partial live configuration fails before any request is sent.
- Live mode composes the Stage D proof runner and requires authenticated smoke, anonymous rejection, origin-spoof rejection, PII rejection, forbidden-tool rejection, strict audit verification, tamper-negative proof, and stdio continuity proof.
- Evidence scanning fails if committed or uploaded evidence contains raw SSNs, bearer tokens, Cloudflare Access token markers, or JWT fragments.
- Fixture mode is valid for scheduled harness regression only; live Remote MCP health still requires configured secrets and copied audit evidence.

---

### Remote MCP Monitor Alert
**Generator:** `scripts/remote-mcp/monitor_alert.py`
**Input:** Remote MCP Monitor Result JSON
**Storage:** workflow artifacts, `raw/remote-mcp-monitor-first-run/*.alert.json`, and optional Markdown summaries

Alert object fields:
| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Alert schema version, currently `1` |
| `generated_at` | string | UTC timestamp |
| `service` | string | Always `remote-mcp` |
| `monitor` | string | Monitor producer, currently `live_health_monitor` |
| `mode` | enum | `fixture` or `live` |
| `health` | enum | `healthy` or `degraded` |
| `summary` | object | Counts for total, passed, failed, skipped, unknown, and sensitive findings |
| `failed_checks` | array | Failed check names and redacted details |
| `unknown_checks` | array | Checks with unexpected status values |
| `sensitive_findings` | array | Pattern labels only; matched sensitive text is never emitted |
| `evidence_dir` | string | Payload-safe evidence directory reference |
| `recommended_action` | string | Operator response summary |

Contract:
- Alert output must not contain bearer tokens, JWT fragments, Cloudflare Access header material, raw SSNs, or raw MCP payloads.

---

### Remote MCP Monitor Operating-Mode Proof
**Producer:** issue-backed operator proof for issue #376
**Storage:** `raw/remote-mcp-monitor-operating-mode/*.json`, `raw/remote-mcp-monitor-operating-mode/*.md`, and validation closeout artifacts
**Selected live surface:** `launchd/com.hldpro.remote-mcp-monitor.plist`
**Scheduled harness:** `.github/workflows/remote-mcp-live-health.yml`

Proof object fields:
| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Operating-mode proof schema version, currently `1` |
| `issue` | integer | Governance issue number for the proof |
| `selected_live_mode` | string | Selected live operating surface; currently `local-launchd` |
| `selected_live_surface` | string | Repo path to the selected scheduler template |
| `github_actions_role` | string | Role of the GitHub workflow for fixture harness and optional configured-live checks |
| `rationale` | array | Payload-safe reasons for the selected mode |
| `required_live_inputs` | array | Environment/configuration names required before live health may be claimed |
| `evidence_policy` | object | Rules for fixture rehearsal, live evidence, fail-closed evidence, and sensitive-material refusal |
| `artifacts` | object | Repo-relative paths to preserved monitor, alert, and validation evidence |

Contract:
- The selected live operating mode is local launchd because live health requires copied audit evidence and a stdio continuity proof command.
- GitHub Actions fixture evidence proves harness regression only unless the complete live configuration and safe evidence source are intentionally configured.
- Live-missing-configuration evidence may include missing environment/configuration names but must not include credential values.
- Preserved operating-mode artifacts must pass the same sensitive-material denylist used by the monitor and alert contracts.

---

### Remote MCP Launchd Live Proof
**Producer:** issue-backed operator proof for issue #378
**Storage:** `raw/remote-mcp-launchd-live-proof/*.json`, `raw/remote-mcp-launchd-live-proof/*.md`, `raw/remote-mcp-launchd-live-proof/*.plist`, and validation closeout artifacts
**Selected live surface:** `launchd/com.hldpro.remote-mcp-monitor.plist`

Proof object fields:
| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Launchd proof schema version, currently `1` |
| `issue` | integer | Governance issue number for the proof |
| `selected_live_mode` | string | Selected live operating mode; currently `local-launchd` |
| `template_path` | string | Repo path to the launchd template |
| `rendered_plist_path` | string | Repo path to the payload-safe rendered plist proof |
| `monitor_mode_argument` | string | Expected launchd monitor mode argument; currently `live` |
| `lint_result` | string | Result of `plutil -lint` for the rendered plist |
| `live_missing_config` | object | Expected and actual exit code for no-secret live fail-closed proof |
| `artifacts` | object | Repo-relative paths to preserved monitor, alert, plist, scan, and validation evidence |

Contract:
- The selected launchd template must invoke `live_health_monitor.py --mode live`, not `--mode auto`.
- Rendered plist evidence must contain repo paths and command arguments only; no credential values may be committed.
- Missing live configuration must fail closed before Remote MCP requests are sent.
- Fixture rehearsal evidence proves launchd pipeline readiness only and must not be described as production live health.
- Preserved launchd proof artifacts must pass the Remote MCP sensitive-material denylist.
- Sensitive input details are replaced with `[redacted-sensitive-detail]` and force `health: degraded`.
- `--fail-on-degraded` exits non-zero after writing redacted artifacts so workflows can both preserve evidence and fail closed.

---

### Remote MCP Operator Connectivity Preflight
**Generator:** `scripts/remote-mcp/operator_connectivity.py`
**Storage:** `raw/remote-mcp-connectivity-preflight/*.json`
**Issue:** #380

Preflight object fields:
| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Preflight schema version, currently `1` |
| `mode` | enum | `fixture` or `live` |
| `ready` | boolean | True only when blocking checks pass and `som.ping` request/response succeeded |
| `message_path` | string | Request/response path being proved, currently `som.ping` |
| `checks` | array | Launchd status checks plus `som.ping` request/response result |
| `missing_live_config` | array | Missing live request configuration names or accepted alternatives, never values |
| `missing_monitor_config` | array | Missing recurring-monitor configuration names, never values |
| `warnings` | array | Non-blocking check names, such as launchd not installed or loaded |
| `recommended_action` | string | Payload-safe operator next action |

Each `checks[]` entry contains:
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Check name, such as `launchd-template-present`, `launchd-loaded`, or `som-ping-request-response` |
| `status` | enum | `pass`, `warn`, or `fail` |
| `detail` | string | Payload-safe detail; missing config names are allowed, credential values are not |

Contract:
- Fixture mode starts a local fixture MCP server and proves `som.ping` through `SomClient`.
- Live mode requires `SOM_MCP_URL`, either `SOM_MCP_TOKEN` or `SOM_REMOTE_MCP_JWT`, `CF_ACCESS_CLIENT_ID`, and `CF_ACCESS_CLIENT_SECRET`.
- Live mode exits `2` before sending a request when required live configuration is missing.
- Launchd install/load warnings do not block one-shot request/response readiness.
- Output must not include bearer-token material, JWT fragments, Cloudflare Access header material, raw SSNs, credential values, or raw MCP payloads.

---

### Remote MCP Operator Inbound Preflight
**Generator:** `scripts/remote-mcp/operator_inbound_preflight.py`
**Storage:** `raw/remote-mcp-operator-inbound-preflight/*.json`
**Issue:** #382

Preflight object fields:
| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Preflight schema version, currently `1` |
| `mode` | enum | `fixture` or `live` |
| `ready` | boolean | True only when the receive-path checks pass |
| `receive_path` | string | Receive path being proved, currently `hitl-relay-session-inbox` |
| `checks` | array | Queue contract, request/response separation, and session-inbox receive checks |
| `missing_live_config` | array | Missing live queue/session configuration names, never values |
| `warnings` | array | Non-blocking check names |
| `received_instruction` | object | Payload-safe summary of the received `session_instruction` |
| `recommended_action` | string | Payload-safe operator next action |

The `received_instruction` summary may contain packet id, packet type, session id, request id, response id, action, target session id, and audit packet types. It must not contain raw message body text.

Contract:
- Fixture mode uses `scripts/orchestrator/hitl_relay_queue.py` to build a valid request, process a deterministic operator response, and prove a validated `session_instruction` reaches `session-inbox`.
- Live mode requires `SOM_OPERATOR_INBOUND_QUEUE_ROOT` and `SOM_OPERATOR_INBOUND_SESSION_ID`.
- Live mode exits `2` before inspecting receive state when required live configuration is missing.
- Live mode exits `1` when the queue is configured but no validated instruction for the configured session is present.
- Output must not include bearer-token material, JWT fragments, Cloudflare Access header material, raw SSNs, credential values, or raw message bodies.

---

### HITL Relay Queue
**Generator:** `scripts/orchestrator/hitl_relay_queue.py`
**Storage:** `raw/hitl-relay/queue/`
**Audit log:** `raw/hitl-relay/queue/audit/events.jsonl`

Queue directories:
| Directory | Description |
|-----------|-------------|
| `requests` | Valid local CLI checkpoint HITL request packets |
| `responses` | Verified local operator response packets |
| `decisions` | Normalized bounded decision packets |
| `session-inbox` | Validated session instruction packets addressed to one local CLI session |
| `session-resume` | Resume packets for stale, blocked, or missing sessions |
| `dead-letter` | Invalid packets with explicit validation reasons |
| `audit` | JSONL replay evidence for the request, response, decision, validation, instruction, and resume path |

Every packet emitted by the relay queue is validated with `scripts/packet/validate_hitl_relay.py` before it is written outside `dead-letter`.

---

### Self-Learning Knowledge Report
**Generator:** `scripts/orchestrator/self_learning.py`
**Default storage:** `metrics/self-learning/latest.json` and `metrics/self-learning/latest.md`
**Weekly workflow:** `.github/workflows/overlord-sweep.yml`

Indexed source paths:
- `docs/FAIL_FAST_LOG.md`
- `docs/ERROR_PATTERNS.md`
- `raw/closeouts/*.md`
- `raw/operator-context/**/*.md`
- `docs/ORG_GOVERNANCE_COMPENDIUM.md`
- `graphify-out/hldpro-governance/GRAPH_REPORT.md`

Contract:
- Graphify and compendium tokens are used for routing attention only.
- Packet-enriched claims cite direct source files through `evidence_paths`.
- Novel failure write-back creates new issue-backed files under `raw/operator-context/self-learning/` and does not edit existing human-authored logs.
- Weekly report JSON includes `generated_at`, `entry_count`, `duplicate_groups`, `stale_entries`, `sources`, and `graphify_attention_only`.
- Weekly markdown is appended to the overlord sweep issue so stale or duplicate learning entries are visible during the sweep.

---

### End-to-End Pilot Metrics
**Generator:** manual pilot closeout workflow for issue #231
**Storage:** `metrics/pilot/issue-231-e2e-pilot.json` and `metrics/pilot/issue-231-e2e-pilot.md`

Contract:
- Records pilot issue number, target repo, isolated worktree, packet id, packet queue mode, validation command count, independent review requirement, completion gate requirement, readiness conclusion, and residual risks.
- `authority_expansion_granted` must remain false unless a separate issue explicitly grants broader autonomous execution authority.
- The markdown companion summarizes the artifact chain used for plan, packet, review, gate, closeout, PR, CI, and merge evidence.

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

### Graphify Hook Helper Resolution
**File:** `scripts/knowledge_base/graphify_hook_helper.py`
**Used by:** governed repo graphify hook adoption and operator dry-runs
**Storage:** not persisted by default; adoption PRs should paste or attach dry-run output as issue/PR evidence

Key fields in `resolve` / `dry-run` JSON:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `repo_slug` | string | yes | `docs/graphify_targets.json` target slug |
| `target_repo` | string | yes | Product or governed repo checkout where hooks are installed |
| `governance_root` | string | yes | Governance checkout that owns the helper and manifest |
| `source_path` | string | yes | Manifest `source_path` resolved relative to `governance_root` |
| `output_path` | string | yes | Manifest `output_path` resolved relative to `governance_root`; product-repo output paths are refused before build |
| `wiki_path` | string | yes | Manifest `wiki_path` resolved relative to `governance_root` |
| `hook_paths` | object | yes | Git-resolved `post-commit` and `post-checkout` hook paths for the target repo |
| `refresh_command` | array | dry-run only | Exact command the managed hook would run |

Adoption evidence for AIS and knocktracker must prove raw graphify hooks are removed or absent and that managed hooks call this helper rather than raw `graphify hook install` output.

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
- Required classification fields: `governance_tier`, `security_tier`, `lifecycle_status`, `governance_status`, `classification.owner`, `classification.rationale`, `classification.review_date`, `classification.issue_refs`, and `enabled_subsystems`.
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
- Local E2E simulation can require issue-specific execution-scope evidence with `--enforce-planner-boundary-scope`; planner-boundary changes then require exactly one issue-matching implementation scope or planning scope under `raw/execution-scopes/`.
- Local execution scope validation declares expected checkout root, branch, allowed write paths, and forbidden dirty roots.
- Tier 1 planner-boundary mode uses execution scope `execution_mode: planning_only`; `allowed_write_paths` is the planning artifact allowlist.
- Non-planning diffs require `handoff_evidence.status: accepted` and pinned planner/implementer metadata before scope assertion passes.
- If planner and implementer use the same model id or model family, handoff evidence must include `active_exception_ref` plus non-expired `active_exception_expires_at`.
- For planner-boundary enforcement, CI (`governance-check.yml`) is authoritative; the local hook is warning/early-signal only.

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

---

### Local Model Runtime Inventory
**Generator:** `scripts/lam/runtime_inventory.py`
**Optional storage:** reviewed caller path via `--output`, for example `metrics/runtime-inventory/latest.json`

Contract:
- Probes Mac hardware and local runtime availability without sending prompt payloads.
- Probes Windows Ollama metadata through `/api/tags` only.
- Reports `probe_payloads_sent: false`.
- Reports PII guardrail readiness from local pattern files.
- Missing or malformed PII patterns must produce `fail_closed: true`.
- Reports routing boundaries: no PII to cloud, no PII to Windows, halt when patterns are missing, halt for PII/architecture/standards if local guardrail is unavailable.
- Reports memory budgets for Mac steady-state guardrail/intent models and one-at-a-time on-demand worker/critic models.
