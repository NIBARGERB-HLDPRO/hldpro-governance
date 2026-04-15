# Sprint 5 Closeout — Windows-Ollama Tier-2 Rung Activation

**Date:** 2026-04-15  
**Epic:** Windows-Ollama SoM Tier-2 Integration (Phase 2)  
**Sprint:** 5 (Final / Activation)  
**Status:** COMPLETE  
**PR:** #123 (merged a3f2a4a)

## Objective

Activate the Windows-Ollama Tier-2 Worker fallback rung from documented/disabled to ACTIVE state. Deliver the routing decision tree (`decide.sh`), close all 3 blocking exceptions, and complete the epic.

## Acceptance Criteria — All Met

### 1. Decision routing script
- [x] `scripts/windows-ollama/decide.sh` implemented (109 lines, bash + Python stdlib)
- [x] Decision priority: PII halts → spark primary → local → windows → cloud fallback
- [x] Inputs: pii-flag, prompt-text/file, daemon statuses (all flags supported)
- [x] Output: single line to stdout (LOCAL | WINDOWS | CLOUD | HALT); exit codes correct
- [x] Stderr logging implemented for observability

### 2. Test suite — all 8 cases passing
- [x] test_decide.sh covers all 8 decision paths
  - PII-yes + any other state → HALT (2 cases)
  - PII-no + spark-ok → CLOUD (primary)
  - PII-no + spark-blocked + local-up → LOCAL
  - PII-no + spark-blocked + local-down + windows-ok → WINDOWS
  - PII-no + spark-blocked + local-down + windows-down → CLOUD (fallback)
  - Empty pii-flag defaults to "no"
  - Spark-unknown with windows-ok → WINDOWS
- [x] test_integration.sh E2E smoke test (skip-on-unreachable convention)

### 3. STANDARDS.md activation
- [x] Tier-2 ladder cell updated: Qwen → **Windows Ollama** → Sonnet (now ACTIVE)
- [x] Removed "Sprint 5 deferral" markers from cell
- [x] Cites `scripts/windows-ollama/decide.sh` as routing entry point
- [x] References invariants #8–#10 enforcement

### 4. Exception register — all 3 closed
- [x] SOM-WIN-OLLAMA-PII-001 → CLOSED (Sprint 2 submit.py + Sprint 5 decide.sh)
- [x] SOM-WIN-OLLAMA-AUDIT-001 → CLOSED (Sprint 3 audit.py + Sprint 4 CI)
- [x] SOM-WIN-OLLAMA-DISABLED-001 → CLOSED (rung now ACTIVE)
- [x] All closures justified with live control references
- [x] Entries kept in file for audit trail

### 5. Runbook update
- [x] Removed "not approved for SoM routing" language
- [x] Updated to: "Windows Ollama is an ACTIVE SoM Tier-2 Worker fallback as of Sprint 5 merge"
- [x] New §Decision entry point documents decide.sh flags and output
- [x] Updated §Audit and §PII gate sections to reflect active state
- [x] Changelog entry added

### 6. Code quality
- [x] Bash syntax clean (bash -n on all three scripts)
- [x] No net-new dependencies
- [x] Scripts idempotent and pure (no side effects)
- [x] All files parse cleanly

## Test Results

```
test_decide.sh: 8/8 PASS ✓
test_integration.sh: SKIP (exit 77) — Windows endpoint unreachable in CI (expected) ✓
Bash lint: ✓ Clean
CI gates: ✓ All pass (5 checks)
```

## Deliverables Summary

| File | Type | Lines | Change |
|---|---|---|---|
| scripts/windows-ollama/decide.sh | new | 109 | Routing decision tree |
| scripts/windows-ollama/tests/test_decide.sh | new | 87 | 8 unit tests |
| scripts/windows-ollama/tests/test_integration.sh | new | 23 | E2E smoke test |
| STANDARDS.md | modified | 271 | Tier-2 cell activated |
| docs/exception-register.md | modified | 117 | 3 exceptions closed |
| docs/runbooks/windows-ollama-worker.md | modified | 127 | Updated for active state |

**Total additions:** 269 insertions  
**Commit:** a3f2a4a (squash merge of feat/windows-ollama-sprint5)

## Invariant Enforcement Status

| # | Invariant | Control | Status |
|---|---|---|---|
| 8 | PII floor (Windows-Ollama) | submit.py (Sprint 2) + decide.sh (Sprint 5) | LIVE ✓ |
| 9 | Firewall binding | check-windows-ollama-exposure.yml (Sprint 4) | LIVE ✓ |
| 10 | Audit trail | audit.py (Sprint 3) + verify_audit.py (Sprint 3) + check-windows-ollama-audit-schema.yml (Sprint 4) | LIVE ✓ |

## Epic Complete — All 5 Sprints

| Sprint | PR | SHA | Artifact |
|---|---|---|---|
| 1 (Stage A) | #112 | 52cee63 | Standards + runbook + 3 exceptions seeded |
| 2 (PII) | #116 | 9d3061d | submit.py + pii_patterns.yml + tests |
| 3 (Audit) | #118 | 1cbc0c5 | audit.py + verify_audit.py + tests |
| 4 (CI) | #121 | 4799ada | exposure + audit-schema validators |
| **5 (Activate)** | **#123** | **a3f2a4a** | **decide.sh + 3 exception closures + activation** |

## Tier-2 Ladder State (Final)

```
Tier 2 (Worker): gpt-5.3-codex-spark (high) →[fallback 1]→ gpt-5.3-codex-spark (medium) →[fallback 2]→
  mlx-community/Qwen2.5-Coder-7B-Instruct-4bit (local warm daemon) 
  →[spark blocked & local down]→ Windows Ollama (http://172.17.227.49:11434, qwen2.5-coder:7b)
  →[windows down]→ claude-sonnet-4-6 (cost-flagged)

Routing via: scripts/windows-ollama/decide.sh
Exceptions closed: ALL (3/3)
Status: ACTIVE ✓
```

## Memory / Feedback Updates

**Recommended update to memory:**

> **Windows-Ollama Tier-2 ladder now active** (as of 2026-04-15 Sprint 5 merge).
> 
> Tier-2 Worker fallback chain:
> 1. gpt-5.3-codex-spark (primary, high effort)
> 2. gpt-5.3-codex-spark (medium effort if spark high is quota-blocked)
> 3. mlx-community/Qwen2.5-Coder-7B-Instruct-4bit (local warm daemon on Mac)
> 4. **Windows Ollama** (http://172.17.227.49:11434, qwen2.5-coder:7b, routed via scripts/windows-ollama/decide.sh, PII halts at entry point)
> 5. claude-sonnet-4-6 (cost-flagged final fallback)
>
> PII invariant #8: All payloads validated against pii_patterns.yml. PII-flagged payloads halt, never route to Windows or cloud.
> Audit invariant #10: All calls appended to raw/remote-windows-audit/YYYY-MM-DD.jsonl with hash-chain + HMAC + daily manifest.
> Firewall invariant #9: LAN-only, sase-switch vEthernet adapter (172.17.0.0/16 subnet).

## Phase 3 Future Epics (Queued)

The following epics remain in backlog, queued for Phase 3 (post Sprint 5):

- **Cloudflare Tunnel exposure** (Issue TBD) — Remote access via Cloudflare Access (out-of-band from SoM routing)
- **Wake-on-LAN provisioning** (Issue TBD) — Auto-boot + magic-packet sender (ops convenience, not security-critical)
- **Health-check workflow** (Issue TBD) — Periodic CI ping to flag endpoint outages (observability)

These were planned in the original epic but deferred to Phase 3 per SoM charter. No blockers.

## Sign-Off

- **Orchestrator:** Haiku Orchestrator (Claude Haiku 4.5)
- **Worker:** Claude Sonnet 4.6 (Tier-2 implementation per fallback #5)
- **Reviewer:** gpt-5.4 (cross-review, Tier-3)
- **Gate:** claude-haiku-4-5-20251001 (Tier-4 verification)

**Status:** EPIC COMPLETE ✓

All acceptance criteria met. All 3 exceptions closed. Windows-Ollama Tier-2 rung is now ACTIVE. Epic ready for wiki write-back and memory update.
