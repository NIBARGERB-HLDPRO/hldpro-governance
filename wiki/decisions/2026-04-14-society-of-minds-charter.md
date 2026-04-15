# Society of Minds Model Routing Charter

**Date:** 2026-04-14  
**Scope:** Org-wide (hldpro-governance + 5 adoption repos)  
**Decision ID:** SOD-2026-04-14-001  
**Author:** Benji (Tier 1 Planner-Claude) + gpt-5.4 (Tier 1 Planner-Codex)  
**Cross-Review:** APPROVED_WITH_CHANGES (round 1); final verdict pending revised plan

## Decision Summary

Codify activity → model routing as a unified Society of Minds charter with enforced handoff protocols. The charter establishes five named tiers (Dual Planner, Worker, Reviewer, Gate, and a lateral LAM lane for local work), each with explicit primary/fallback models, hard-rule invariants enforced by CI, and a deterministic packet handoff protocol that replaces hook-based drift detection. Every governance intent has a CI-verifiable enforcement artifact — no orphan rules.

## Tier Structure

| Tier | Role | Primary | Fallback 1 | Fallback 2 | Floor |
|---|---|---|---|---|---|
| 1 | **Dual Planner — required pair** | Claude: `claude-opus-4-6` **AND** Codex: `gpt-5.4` @ `model_reasoning_effort=high` | Claude → `claude-sonnet-4-6`; Codex → `gpt-5.3-codex-spark` @ `high` | Codex only → `gpt-5.3-codex-spark` @ `medium` | Claude: no Haiku for planning. Codex: no below-spark for planning. Both unavailable → halt. |
| 2 | Worker (coder) | `gpt-5.3-codex-spark` @ `high` | `gpt-5.3-codex-spark` @ `medium` | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (local, unlimited) → `claude-sonnet-4-6` (cost-flagged) | — |
| 3 | Reviewer (code) | `claude-sonnet-4-6` | `claude-haiku-4-5` (review quality flagged) | — | — |
| 3 | Reviewer (non-code long-form) | `gpt-5.4` @ `medium` | `gpt-5.4` @ `low` | `claude-sonnet-4-6` | — |
| 4 | Gate / verifier | `claude-haiku-4-5-20251001` | `claude-sonnet-4-6` (wasteful but safe) | — | — |

## LAM Lane (Local, Apple M5 — MLX Runtime)

LAM is lateral to the tier chain. Never plans (Tier 1), never cross-reviews (independence requires non-local). Used for PII / bulk / embeddings / offline.

| Mind | Model ID | Role | Token cap |
|---|---|---|---|
| M7 Guardrail-LAM | `mlx-community/Qwen3-8B-4bit` | Pre-exec PASS/BLOCK | 64 |
| M4 Worker-LAM | `mlx-community/Qwen3-14B-4bit` | Implementation on local lanes (PII/bulk/offline) | 400 |
| M6 Critic-LAM | `mlx-community/gemma-4-26b-a4b-4bit` | Adversarial review | 256 |
| MCP daemon | `mlx-community/Qwen3-1.7B-4bit` (primary) / `mlx-community/Phi-4-mini-instruct-4bit` (reserve) | Intent parsing + packet routing; always-warm, evictable under pressure | 128 |
| Qwen-Coder fallback | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | Tier-2 worker when codex-spark unavailable | 512 |
| Auditor-Claude | `claude-sonnet-4-6` | Manifest-only review for PII, content review for non-PII | — |

## Fallback Ladder

**Tier 1 Dual Planner**
1. Claude: `claude-opus-4-6` + Codex: `gpt-5.4 high` (primary)
2. Claude: `claude-sonnet-4-6` + Codex: `gpt-5.3-codex-spark high` (fallback 1)
3. Codex only: `gpt-5.3-codex-spark medium` (fallback 2 — Claude unavailable)
4. **HALT** — both Claude AND Codex unavailable for planning

**Tier 2 Worker**
1. `gpt-5.3-codex-spark high` (primary)
2. `gpt-5.3-codex-spark medium` (fallback 1 — reasoning downgrade)
3. `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` local (fallback 2 — quota/cost)
4. `claude-sonnet-4-6` (fallback 3 — cost-flagged, logged)

**Tier 3 Reviewer (code)**
1. `claude-sonnet-4-6` (primary)
2. `claude-haiku-4-5` (fallback 1 — review quality flagged)
3. No further fallback

**Tier 4 Gate**
1. `claude-haiku-4-5-20251001` (primary)
2. `claude-sonnet-4-6` (fallback 1 — wasteful but safe)

## Hard-Rule Invariants (7 enforced rules)

1. **No self-approval.** No mind reviews its own output. Drafter, reviewer, and gate identities must be distinct.
2. **No tier skipping.** No merge without Worker → Reviewer → Gate.
3. **Planning floor.** Tier 1 never drops below `claude-sonnet-4-6` (Claude side) or `gpt-5.3-codex-spark` (Codex side). Both unavailable → halt.
4. **PII floor.** Content tagged or detected as PII routes through LAM only. Never sent to cloud reviewers. Violation = security incident.
5. **Cross-family independence.** Tier 1 Planner-Claude and Planner-Codex MUST be different model families (Anthropic + OpenAI). Never both same family.
6. **Local family diversity.** Worker-LAM and Reviewer-LAM MUST be different model families (e.g., Qwen + Gemma).
7. **Fallback is logged.** Every fallback to a lower tier writes a schema-validated entry under `raw/model-fallbacks/YYYY-MM-DD.md`.

## Key Architectural Decisions

### Model Selection
- **Primary MCP daemon model:** `mlx-community/Qwen3-1.7B-4bit` — smallest model reliably parsing structured routing decisions (0.1–0.3s on intent parsing).
- **Tier-2 local fallback:** `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` — empirically outperforms Qwen3 on code tasks; fills gap when `gpt-5.3-codex-spark` quota-limited.
- **Reserve MCP model:** `mlx-community/Phi-4-mini-instruct-4bit` — fallback if Qwen3 hallucination rate exceeds 2%.

### Handoff Protocol
- **Packet-based, not hook-based.** Old model: reactive error log scraping. New model: proactive structured packet validation at every tier transition. Replaces implicit drift detection with explicit contract enforcement.
- **Deterministic validator, not LLM rule engine.** Validator is pure Python (schema check + assertions). Intent parser feeds validator; validator never feeds back to LLM. Prevents cascading hallucination failures.

### LAM Topology
- **Option A: Monolithic M5 (16GB resident).** All local models fit in single Apple M5 with resident baseline (M7 + daemon always-on; M4/M6 on-demand). Simpler boot-start, faster iteration.
- **Deferred Option B: Distributed 16GB-per-model boxes.** Revisit post-outage phase when single-M5 resource constraints become acute.

### Cross-Review + Enforcement
- **Dual-planner pairing mandatory for architecture/standards.** Tier 1 requires Claude (Opus/Sonnet floor) **AND** Codex (gpt-5.4 high / spark high floor) as distinct, cross-family reviewers.
- **CI-verifiable enforcement for all rules.** 12 enforcement rows in STANDARDS.md §Society of Minds, each mapped to a reusable workflow or script. No orphan governance.
- **Round 1 M6-vs-Sonnet A/B protocol.** Critic-LAM (gemma-4-26b) shadow-runs Sonnet code reviews. Conservative gate: Sonnet wins ties. Exit Round 1 at ≥90% agreement for 3 consecutive weeks.

## Supporting Artifacts

- **STANDARDS.md § Society of Minds** — tiers, LAM lane, MCP daemon responsibilities, handoff chain, hard-rule invariants, cross-review artifact schema, enforcement index, exception register schema, Round 1 protocol.
- **10 reusable workflows** — `check-agent-model-pins.yml`, `check-codex-model-pins.yml`, `require-cross-review.yml`, `check-no-self-approval.yml`, `check-pii-routing.yml`, `check-lam-availability.yml`, `check-lam-family-diversity.yml`, `check-claude-md-pointer.yml`, `check-fallback-log-schema.yml`, `check-arch-tier.yml`.
- **4 scripts** — `scripts/cross-review/require-dual-signature.sh`, `scripts/model-fallback-log.sh`, `scripts/lam/require-lam-dual-signature.sh`, `scripts/lam/pii-patterns.yml`.
- **MCP daemon** (`local-ai-machine/services/som-mcp/`) — always-warm Qwen3-1.7B intent parser + packet validator + 6 MCP tools.
- **Packet schema + validator** (`hldpro-governance/schemas/packet-schema.json` + `packet-validator.py`) — deterministic validation at tier transitions.
- **Exception register** (`hldpro-governance/docs/exception-register.md`) — exceptions tracked with expiry ≤ 90 days, monthly review cadence.
- **Cross-review artifact** (`raw/cross-review/2026-04-14-society-of-minds-charter.md`) — dual-signed plan capture (Opus drafter + gpt-5.4 reviewer).

## Governance Impact

- **Replaces implicit model routing with explicit governance.** Old: ad-hoc model selection per session. New: codified tiers, enforced invariants, logged fallbacks.
- **Enables cross-repo model policy consistency.** All 5 adoption repos (ai-integration-services, HealthcarePlatform, ASC-Evaluator, local-ai-machine, knocktracker) adopt the same tier structure via reusable workflows.
- **Provides audit trail for model selection.** Fallback log + cross-review artifacts + CI workflow runs create a complete record of model routing decisions over time.
- **Operationalizes local AI as tier fallback.** LAM local models are no longer experimental; they are production fallbacks for Tier 2/3 work, reducing cost and improving latency.

## Links To

- Epic umbrella: [#99](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/99)
- STANDARDS.md: `hldpro-governance/STANDARDS.md` §Society of Minds
- Closeout: `raw/closeouts/2026-04-14-society-of-minds-epic.md`
- PRs: #100 (hldpro-governance charter), #106 (packet schema), #107 (CI exceptions), #1020, #1238, #4, #154, #431, #432 (adoption)
- Cross-review: `raw/cross-review/2026-04-14-society-of-minds-charter.md`
- Exception register: `docs/exception-register.md`
- MCP daemon: `local-ai-machine/services/som-mcp/`
