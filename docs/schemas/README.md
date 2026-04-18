# SoM Packet Schema & Validator

## Overview

The SoM (Society of Minds) Stage 4 packet system provides deterministic, LLM-free validation for multi-tier AI agent handoffs. Packets carry prior identity, destination tier, and standards compliance markers.

## Schema Definition

**File:** `som-packet.schema.yml`

A JSON Schema YAML describing the canonical handoff packet shape:

- **packet_id** (UUID): Unique identifier for this packet
- **prior** (object): Source agent metadata
  - `tier` (1-4): Source tier
  - `role`: Agent role (architect-claude, architect-codex, worker, reviewer, gate, worker-lam, critic-lam)
  - `model_id`: Model identifier (e.g., claude-opus-4)
  - `model_family`: Family for cross-family validation (anthropic, openai, qwen, gemma, etc.)
  - `timestamp`: ISO-8601 UTC timestamp
- **next_tier** (1-4): Destination tier
- **parent_packet_id** (UUID, optional): Required if prior.tier == 1 (dual-planner)
- **artifacts** (array): File paths or URLs of included artifacts
- **standards_ref** (string): Reference to STANDARDS.md (default: "STANDARDS.md §Society of Minds (SoT)")
- **runbook_ref** (string, optional): Runbook URL or path
- **fallback_ladder_ref** (string, optional): Fallback tier-down scenario reference

**File:** `hitl-relay-packet.schema.json`

A JSON Schema describing the always-on SoM HITL relay packet contract:

- **packet_type**: One of `session_event`, `hitl_request`, `hitl_response`, `normalized_decision`, `session_instruction`, `session_resume`, or `audit_record`
- **session**: CLI session identity, CLI type, and current state
- **correlation**: Request, notification, response, and parent packet IDs for end-to-end traceability
- **policy**: PII mode, data classification, channel policy reference, and optional retention policy reference
- **operator_reply**: Sender/channel/message metadata plus a raw message reference; raw message bodies are not allowed in the packet
- **normalized_decision**: Bounded action, confidence, model identity, raw message reference, and validation-required marker
- **instruction**: Bounded action addressed to an exact target session with audit references
- **resume**: Stale/missing/wrong-target session recovery context
- **audit**: Evidence references and decision trace steps used by the final E2E proof

Examples live under `docs/schemas/examples/hitl-relay/`. Valid examples must pass schema validation; invalid examples must fail closed.

## Validator

**File:** `scripts/packet/validate.py`

### Runtime boundary

Governance enforcement in this repository validates packet metadata and invariants.
MCP runtime execution of these checks is implemented in **local-ai-machine**
(`services/som-mcp`), with this repo supplying the schema and validation policy.

Deterministic validator (no LLM). Enforces:

1. **Schema Validation**: Structural checks via jsonschema
2. **Dual-Planner Rule** (tier==1): Requires `parent_packet_id` and cross-family pairing validation
3. **No-Self-Approval**: Walk parent chain; prevent consecutive same-model in opposite-tier roles
4. **Planning Floor**: Refuse weak models (claude-haiku-4-5, gpt-4-mini, etc.) for tier 1 dual-planner
5. **PII Floor**: Artifacts matching `scripts/lam/pii-patterns.yml` require worker-lam or critic-lam roles
6. **Tier Escalation**: Enforce no tier skipping (`prior.tier + 1 == next_tier` for active tiers)
7. **LAM Family Diversity**: Enforce diverse LAM handoff families when multiple LAM roles appear in chain
8. **Fallback Logging**: If `fallback_ladder_ref` exists, it must resolve to a file under `raw/model-fallbacks/`

### Usage

```bash
python3 scripts/packet/validate.py <packet-file.yml>
python3 scripts/packet/validate.py <packet-file.yml> --json
```

Exit codes:
- `0`: Packet valid
- `1`: Validation failed (error message printed with `::error::` annotation)

JSON output format:
```json
{"status": "ok"|"refused", "reason": "...", "packet_id": "..."}
```

## Packet Emitter

**File:** `scripts/packet/emit.py`

Helper to author packets. Generates packet YAML with UUID and current timestamp.

### Usage

```bash
python3 scripts/packet/emit.py \
  --prior-tier 2 \
  --prior-role worker \
  --prior-model-id claude-opus-4 \
  --prior-model-family anthropic \
  --next-tier 3 \
  --artifact scripts/my-work.md \
  --artifact docs/report.md
```

Output: Path to packet file at `raw/packets/YYYY-MM-DD-<uuid>.yml`

Optional flags:
- `--parent-packet-id <uuid>`: Parent packet (required for tier 1)
- `--standards-ref <ref>`: Override standards reference
- `--runbook-ref <url>`: Runbook URL
- `--fallback-ladder-ref <ref>`: Fallback scenario reference

## Packet Lifecycle

1. **Author** → Operator or agent calls `emit.py` with metadata
2. **Validate** → Validator checks schema + governance rules before handoff
3. **Handoff** → Deterministic transfer to next tier
4. **Chain Audit** → Governance can walk parent chain to audit cross-tier decisions

## Governance Standards

All rules derive from **STANDARDS.md §Society of Minds (SoT)**:

- **Dual-Planner Handoff** (§2.1): Tier 1 requires two different model families to review each other
- **No-Self-Approval** (§2.2): Same model cannot consecutively review own output
- **Planning Floor** (§2.3): Weak models cannot initiate tier-1 planning
- **PII Handling** (§2.4): LAM-tier handlers required for sensitive artifacts

For the full standard, see `STANDARDS.md`.
