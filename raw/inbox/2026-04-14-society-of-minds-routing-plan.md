---
date: 2026-04-14
captured_by: claude-opus-4-6
type: epic-plan
status: in-progress
umbrella_issue: NIBARGERB-HLDPRO/hldpro-governance#99
---

# Epic — HLD Pro Society of Minds (full rollout)

Codifies activity → model-tier routing as a society-of-minds role charter with enforced handoff protocols. One epic, six stages (PDCAR), one umbrella issue.

## Charter summary

### Tiers

| Tier | Role | Primary | Fallback ladder |
|---|---|---|---|
| 1 | **Dual Planner** (required pair) | `claude-opus-4-6` ⇄ `gpt-5.4` high | Claude: Sonnet. Codex: codex-spark high → codex-spark medium. Both down → halt. |
| 2 | Worker (coder) | `gpt-5.3-codex-spark` high | codex-spark medium → **`mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (local)** → Sonnet (cost-flagged) |
| 3 | Reviewer (code) | `claude-sonnet-4-6` | Haiku (degraded-flagged) |
| 3 | Reviewer (non-code) | `gpt-5.4` medium | gpt-5.4 low → Sonnet |
| 4 | Gate / verifier | `claude-haiku-4-5-20251001` | Sonnet (wasteful but safe) |

### LAM lane (local, Apple M5 — MLX runtime)

| Mind | Model ID | Role |
|---|---|---|
| M7 Guardrail-LAM | `mlx-community/Qwen3-8B-4bit` | Always-resident pre-exec PASS/BLOCK |
| M4 Worker-LAM | `mlx-community/Qwen3-14B-4bit` | Local-lane implementation (PII/bulk/offline) |
| M6 Critic-LAM | `mlx-community/gemma-4-26b-a4b-4bit` (outlines) | Adversarial review (hard-block authority) |
| **MCP daemon (NEW)** | `mlx-community/Qwen3-1.7B-4bit` primary / `mlx-community/Phi-4-mini-instruct-4bit` reserve | Intent parsing, packet routing, always-warm local MCP layer |
| **Qwen-Coder (NEW)** | `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` | Tier-2 codex-spark fallback; loaded on-demand |
| Auditor-Claude | `claude-sonnet-4-6` | Manifest-only PII review / content review non-PII |

### Hard-rule invariants

1. No self-approval. Drafter, reviewer, gate identities distinct.
2. No tier skipping. Worker → Reviewer → Gate always.
3. Planning floor. Never below Sonnet (Claude) or codex-spark (Codex). Both down → halt.
4. PII floor. PII content routes through LAM only. Never sent to cloud reviewers.
5. Cross-family independence (Tier 1). Planner-Claude + Planner-Codex must be different model families.
6. Local family diversity. Worker-LAM + Reviewer-LAM must be different model families.
7. Fallback logged. Every fallback writes a schema-validated entry under `raw/model-fallbacks/YYYY-MM-DD.md`.

## Epic stages (PDCAR)

### Plan (complete)
- This capture
- Cross-review artifact: `raw/cross-review/2026-04-14-society-of-minds-charter.md` (Opus ⇄ gpt-5.4 high, APPROVED_WITH_CHANGES → resolved)

### Do — Stage 1: Governance SoT + reusable workflows — PR #100
Status: open, CI partially green.
- `STANDARDS.md §Society of Minds` — full charter
- 10 reusable workflows under `.github/workflows/` (check-agent-model-pins, check-codex-model-pins, require-cross-review, check-no-self-approval, check-pii-routing, check-lam-availability, check-lam-family-diversity, check-claude-md-pointer, check-fallback-log-schema, check-arch-tier)
- 4 scripts (cross-review/require-dual-signature.sh, model-fallback-log.sh, lam/require-lam-dual-signature.sh, lam/pii-patterns.yml)
- `.lam-config.yml`, `docs/exception-register.md`, `.github/pull_request_template.md`

### Do — Stage 2: Repo adoptions — 5 draft PRs
Status: all pushed, waiting on #100 merge.
- ai-integration-services #1020, HealthcarePlatform #1238, ASC-Evaluator #4, knocktracker #154, local-ai-machine #431
- Each adds governance-check calls, CLAUDE.md SoT pointer, PR template, agent pins (local-ai-machine)
- Pinned to `@feat/society-of-minds-charter` branch; follow-up flips to `@main` after #100 merges

### Do — Stage 3: MCP daemon + Qwen-Coder fallback + always-on orchestration — NEW
Implementation repo: `local-ai-machine` (new PR).
- `services/som-mcp/` directory: Python daemon hosting the MCP server
- MCP tools exposed: `som.handoff`, `som.chain`, `som.log_fallback`, `lam.probe`, `lam.embed`, `lam.scrub_pii`
- Primary model: `mlx-community/Qwen3-1.7B-4bit` (routing + intent parsing)
- Upgrade stub: `mlx-community/Phi-4-mini-instruct-4bit` (config-swappable, role_scope extends to reviewer-lam-fallback)
- Tier-2 fallback path: `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` loaded on-demand when codex-spark unavailable
- Eviction policy: M7 privileged (always-resident); MCP model warm-evictable; Qwen-Coder / M4 / M6 on-demand
- Lifecycle: launchd plist for boot-start; daemon survives session restarts
- Memory discipline: deterministic validator behind MCP tools (not LLM-as-validator); LLM used only for intent parsing
- Fallback semantics: halt for arch/PII, degraded-mode for implementation (logged)
- Drafter: Qwen-Coder 7B-4bit (local) — proving the fallback path; Sonnet reviews

### Do — Stage 4: Packet handoff schema + validator + skill enforcement — NEW
Implementation repo: governance (schema + validator) + local-ai-machine (daemon integration).
- Canonical packet shape: carries prior identity, next_tier, pointer to STANDARDS (no embedded rules)
- Validator: deterministic structural check; refuses malformed packets at handoff time
- Skills (`/tier2-work`, `/tier3-review`, `/tier4-gate`) become packet-authoring entrypoints — no packet → no work
- Replaces earlier proposed UserPromptSubmit + PreToolUse hook + verify-completion A/B-attribution
- Audit trail emergent from `parent_packet_id` chain
- Drafter: codex-spark (post-outage) OR Qwen-Coder fallback; Sonnet reviews

### Check — Stage 5
- overlord run on each repo (0 drift expected)
- overlord-sweep dry run (fallback + A/B metrics appear)
- verify-completion against umbrella issue

### Adjust — Stage 6
- Fix CI failures (PR #100 contract failure investigated)
- Exception-register entries for any repo that cannot pass (per Issue #42 pattern)
- Any required re-review rounds

### Review — Stage 7
- Per-stage closeouts under `raw/closeouts/`
- Umbrella closeout: `raw/closeouts/2026-04-14-society-of-minds-epic.md`
- Wiki decision log entry
- Close umbrella + sub-issues
- OVERLORD_BACKLOG update

## Sub-issues under umbrella #99

1. **Governance SoT** → PR #100 (open)
2. **Repo adoptions** → 5 draft PRs (open)
3. **Adoption ref flip** → follow-up after #100 merges
4. **MCP daemon + Qwen-Coder fallback + orchestration** → new local-ai-machine PR
5. **Packet handoff schema + validator + skills** → governance follow-up PR
6. **Full verification pass** (Check+Adjust+Review) → verify-completion-driven

## Execution constraints

- Work locally as much as possible (LAM-first)
- One consolidated PR per repo (minimize GH Actions spend)
- Governance PR lands first; 5 adoption PRs flipped + ready after
- MCP daemon PR depends on #100 + adoption merges so reusable workflows exist
- Packet schema PR depends on MCP daemon PR so there's infrastructure to wire it into
- Tier-2 Worker role: codex-spark down until ~7:30 PM today → Qwen-Coder takes the drafting work now; codex-spark resumes on return

## Round 1 execution protocol (transitional)

- Drafter: codex-spark primary / Qwen-Coder local fallback
- Reviewer: Sonnet always (regardless of drafter)
- Adversarial critic: M6 gemma-4-26b (when available; MLX memory-release bug observed on M4→M6 swap — tracked as runtime issue)
- Gate: Haiku via verify-completion
- Planner cross-review: Opus ⇄ gpt-5.4 high (both sign `raw/cross-review/*.md`)
- A/B log for Round 1: `raw/ab-review/YYYY-MM-DD-{slug}.md` captures Reviewer-Sonnet and M6-Critic side-by-side (when both run). Exit Round 1 when agreement ≥ 90% for 3 consecutive weeks.

## Enforcement mechanism — evolution

**Earlier proposal (retired):** UserPromptSubmit keyword hook + PreToolUse heuristic block + verify-completion A/B-attribution extension. Retired because it's post-hoc tax on every prompt and adds token cost.

**Current direction:** packet-based handoff with front-of-line validation. Each tier receives a packet authored by the prior tier, validates structurally against STANDARDS, refuses if malformed. Packets live in `raw/packets/*.yml`. MCP daemon hosts the validator; all skills invoke the validator before doing work. No post-hoc verification.

## Out of scope (future)

- Fine-tune Qwen3-32B on wiki data (Phase 8)
- Neo4j graph push (Phase 7)
- Fallback-rate dashboard in public wiki

## Plan capture history

- 2026-04-14 v1 — initial routing matrix
- 2026-04-14 v2 — Tier 1 codex identity disambiguated to gpt-5.4 high after gpt-5.4-high cross-review
- 2026-04-14 v3 — PII hard block CI-enforced
- 2026-04-14 v4 — LAM real models (M7/M4/M6) replace placeholders
- 2026-04-14 v5 — Stage 2 fallback to LAM during codex outage
- 2026-04-14 v6 — Qwen-Coder added as Tier-2 local fallback
- 2026-04-14 v7 — MCP daemon architecture with Qwen3-1.7B primary / Phi-4-mini reserve
- 2026-04-14 v8 — packet-handoff enforcement model replaces hook-based drift detection (this version)
