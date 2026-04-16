# Decision: Windows-Ollama Epic Complete — Tier-2 Rung Activated (2026-04-15)

**Date:** 2026-04-15  
**Authority:** Haiku Orchestrator + Tier-2 Worker (Sonnet 4.6) + Tier-3 Reviewer (gpt-5.4) + Tier-4 Gate (Haiku)  
**Scope:** Governance — Society of Minds routing standard  
**Epic:** Windows-Ollama SoM Tier-2 Integration (Phase 2)  

## Context

The Windows-Ollama Tier-2 Worker fallback underwent a 5-sprint integration phase to transition from documented/disabled to ACTIVE:

1. **Sprint 1 (Stage A, PR #112):** Standards + runbook documentation + 3 blocking exceptions seeded
2. **Sprint 2 (PR #116):** PII middleware (submit.py + pii_patterns.yml validation)
3. **Sprint 3 (PR #118):** Audit trail (audit.py + verify_audit.py + hash-chain + HMAC + manifest)
4. **Sprint 4 (PR #121):** CI validation workflows (exposure + audit-schema gates)
5. **Sprint 5 (PR #123):** Routing decision tree (decide.sh) + all 3 exceptions closed + rung activation

## Decision

**The Windows-Ollama Tier-2 Worker fallback is now ACTIVE.**

The rung transitions from documented/disabled to active status in the Society of Minds Tier-2 ladder. All three invariant controls (#8 PII floor, #9 firewall binding, #10 audit trail) are live end-to-end.

### Rationale

**Invariant #8 (PII floor):** PII-patterns.yml middleware active in submit.py (Sprint 2) + decide.sh routing gate (Sprint 5) enforces: PII-flagged payloads → HALT (never route to Windows or cloud).

**Invariant #9 (firewall binding):** check-windows-ollama-exposure.yml CI gate (Sprint 4) enforces: endpoint bound to LAN-only via sase-switch vEthernet (172.17.0.0/16 subnet), no public bind, no port-forwarding.

**Invariant #10 (audit trail):** audit.py (Sprint 3) + verify_audit.py (Sprint 3) + check-windows-ollama-audit-schema.yml (Sprint 4) enforce: all Windows-Ollama calls appended to raw/remote-windows-audit/YYYY-MM-DD.jsonl with hash-chain + HMAC + daily manifest. Broken chain → CI validator fails, endpoint disabled until chain rebuilt.

### Decision Tree

The `scripts/windows-ollama/decide.sh` routing script implements the Tier-2 ladder priority:

```
1. PII halts first (invariant #8)
2. If spark-ok → CLOUD (spark is primary, skip ladder)
3. Else if local-up → LOCAL (Qwen2.5 on Mac)
4. Else if windows-ok → WINDOWS (this rung)
5. Else → CLOUD (Sonnet cost-flagged fallback)
```

All 8 decision states tested + pass. Integration test skips (exit 77) if Windows unreachable (CI environment expected).

### Exceptions Closed

All 3 blocking exceptions now closed:

- **SOM-WIN-OLLAMA-PII-001:** PII middleware fully enforced via Sprint 2 + 5 controls
- **SOM-WIN-OLLAMA-AUDIT-001:** Audit trail fully enforced via Sprint 3 + 4 controls  
- **SOM-WIN-OLLAMA-DISABLED-001:** Rung activation gate met; status changed from disabled to active

Entries retained in exception-register.md for audit trail.

## Tier-2 Ladder (Final)

```
Primary: gpt-5.3-codex-spark @ high
├─ Fallback 1: gpt-5.3-codex-spark @ medium
└─ Fallback 2: mlx-community/Qwen2.5-Coder-7B-Instruct-4bit (local warm daemon)
   └─ [if spark blocked & local down]
      └─ Windows Ollama (http://172.17.227.49:11434, qwen2.5-coder:7b)
         └─ [if windows down]
            └── claude-sonnet-4-6 (cost-flagged final fallback)
```

**Routing:** `scripts/windows-ollama/decide.sh` (CLI entry point)

## Implications

1. **Usage:** Tier-2 Worker jobs may now automatically route to Windows-Ollama if spark is blocked and local Mac is memory-tight.
2. **Observability:** All Windows-Ollama calls audited in raw/remote-windows-audit/. Audit chain failures block CI.
3. **PII Safety:** PII-flagged payloads halt at decide.sh entry point — never reach Windows endpoint or cloud.
4. **Memory Update:** Feedback_codex_spark_specialist.md should note the 4-rung Tier-2 ladder (spark → local Qwen → Windows Ollama → Sonnet).

## Cross-References

- STANDARDS.md §Society of Minds §Tier 2 (Worker) — row updated to show ACTIVE rung
- STANDARDS.md §Windows Host Inference — invariants #8–#10 live
- docs/exception-register.md — 3 entries marked CLOSED
- docs/runbooks/windows-ollama-worker.md — updated for active state + decide.sh interface
- raw/closeouts/2026-04-15-windows-ollama-sprint5.md — detailed acceptance + test evidence

## Phase 3 Future Work

The following epics remain queued (no blockers):

- **Cloudflare Tunnel exposure** — Remote access via Cloudflare Access
- **Wake-on-LAN provisioning** — Auto-boot + magic-packet convenience
- **Health-check workflow** — Periodic CI ping for observability

These do not block the rung activation and are deferred per SoM charter Phase 3 sequencing.

## Status

**DECISION FINAL:** Epic complete. Windows-Ollama Tier-2 rung is ACTIVE. All invariants enforced. All tests passing. Ready for production routing.

*Post-merge addendum: Sprint 6 (PR #129) remediated an invariant #8 PII regression introduced in Sprint 5. See `raw/closeouts/2026-04-15-windows-ollama-sprint6.md`.*
