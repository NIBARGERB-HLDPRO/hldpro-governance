# Windows Host Ollama — Operator Runbook

Version: 2026-04-15
Owner: Operator (nibarger.ben@gmail.com)
Origin: promoted from `local-ai-machine` issue #68 (closed 2026-03-16) — see that runbook for full integration history.
Scope: SoM Tier-2 Worker fallback (this PR) + existing HP critic role.

## Endpoint

- URL: `http://172.17.227.49:11434`
- API base path: `/api/generate` (Ollama native), `/v1/` (OpenAI-compatible)
- LAN-only — invariant #14. Tunnel deferred.

## Operating contract (do not change without re-validating)

- `keep_alive=15m`
- `num_ctx<=4096`
- Adaptive offload ladder `99 -> 80 -> 60`
- Per-call timeout: 45000 ms
- VRAM envelope target: 12288 MB (12 GB; physical 16 GB)

## Pinned model roster (live inventory)

Discover live with: `curl -s http://172.17.227.49:11434/api/tags | jq '.models[].name'`

Charter-required baseline:

| Model | Role | Pull command |
|---|---|---|
| `qwen2.5-coder:7b` | Tier-2 Worker (SoM) | `ollama pull qwen2.5-coder:7b` |
| `llama3.1:8b` | HP critic | `ollama pull llama3.1:8b` |

Optional / operator-approved:

| Model | Role | Pull command | VRAM (~Q4) |
|---|---|---|---|
| `qwen3:14b-q4_K_M` | M4 Worker-LAM remote option | `ollama pull qwen3:14b-q4_K_M` | ~8.5 GB |

(Operator may have additional models loaded; the live `/api/tags` query is authoritative.)

## Preflight

`bash scripts/windows-ollama/preflight.sh`
- exit 0: endpoint reachable + at least one pinned model present
- exit 1: endpoint unreachable
- exit 2: reachable but no pinned models present

## Adding / removing models

On the Windows host (PowerShell or `wsl`):
```
ollama pull <model:tag>
ollama list
ollama rm <model:tag>
```

Update this runbook's "Pinned model roster" table after any add/remove.

## Operating rules (proven in LAM #68)

- Use the adaptive ladder `99 -> 80 -> 60` as default; fixed-profile overrides reserved for diagnostic isolation only.
- Schema-failure response shape: `{"status":"...", "label":"...", "rationale":"<MUST be non-empty>", "findings":[]}`. Empty `rationale` will trigger the local fail-closed reject contract.
- Single-role and dual-role critic paths both proven; SoM Tier-2 Worker uses single-call-per-job submission.

## PII gate (invariant #8)

**WINDOWS RUNG NOT APPROVED FOR SoM ROUTING UNTIL SPRINT 5.**

Submission script (`scripts/windows-ollama/submit.py`, Sprint 2) MUST run `pii-patterns.yml` against the prompt before any HTTP call and block PII-tagged payloads entirely (route to LAM only or halt). Governed by exception `SOM-WIN-OLLAMA-PII-001` (expires 2026-05-15).

## Audit (invariant #10)

**WINDOWS RUNG NOT APPROVED FOR SoM ROUTING UNTIL SPRINT 5.**

Sprint 2–3 will land:
- `scripts/windows-ollama/audit.py` — append-only writer to `raw/remote-windows-audit/YYYY-MM-DD.jsonl` with hash-chain + HMAC + daily manifest
- `scripts/windows-ollama/verify_audit.py` — local chain validator
- `.github/workflows/check-windows-ollama-audit-schema.yml` (Sprint 4) — CI schema + chain validation

Governed by exception `SOM-WIN-OLLAMA-AUDIT-001` (expires 2026-05-15). Until then, ad-hoc submissions are NOT audit-compliant.

## Failure response

| Symptom | Triage | Action |
|---|---|---|
| Preflight exit 1 (endpoint unreachable) | Mac off LAN? Windows asleep? Network interface flapped? | Confirm LAN; ping `172.17.227.49`; if Windows asleep, manual wake (WoL future epic) |
| Preflight exit 2 (no pinned models) | Operator forgot to pull after fresh OS install? | `ollama pull qwen2.5-coder:7b` on Windows |
| Calls succeed but rationale empty | Prompt contract drift | Re-check the operating rule §"Schema-failure response shape" — usually needs prompt tightening |
| Generation slow / OOM | VRAM envelope exceeded | Use fixed profile `60` as diagnostic; check `nvidia-smi` on Windows side |
| Adaptive ladder selects fewer than 99 | Expected when other GPU work is running | None — proven behavior |

## Stage B acceptance criteria (Sprint 2–5)

Windows-Ollama rung activation (Sprint 5) requires:

1. **submit.py** — Submission script with PII pattern matching + model allowlist validation (Sprint 2)
2. **PII middleware** — `pii-patterns.yml` blocking PII-tagged payloads + hardening for Windows/cloud fallback routes (Sprint 2)
3. **Audit writer** — `audit.py` writing hash-chained, HMAC-signed, daily-manifested audit logs (Sprint 3)
4. **CI validator** — `verify_audit.py` + `check-windows-ollama-audit-schema.yml` enforcing chain integrity (Sprints 3–4)
5. **Firewall allowlist** — Windows firewall binding to Mac host IP or trusted subnet (Sprint 4 CI gate)
6. **Failover rules** — PII-tagged payloads halt instead of falling through to cloud (Sprint 5 decision.sh)
7. **Integration tests** — End-to-end test of submit.py + audit.py + decide.sh (Sprint 5)

## Future epics (Phase 3, deferred)

- **Cloudflare Tunnel exposure** — would mirror `docs/runbooks/qwen-coder-driver.md`; requires Cloudflare Access mandatory per invariant #9.
- **Wake-on-LAN provisioning** — BIOS auto-on / magic-packet sender on Mac side. Until then, expect always-on operation.
- **Health-check workflow** — periodic CI ping to flag endpoint outages.

## Cross-references

- `STANDARDS.md` §"Windows Host Inference (Tier-2 fallback)" + invariants 8–10
- `docs/exception-register.md` entries `SOM-WIN-OLLAMA-PII-001`, `SOM-WIN-OLLAMA-AUDIT-001`, `SOM-WIN-OLLAMA-DISABLED-001`
- `docs/EXTERNAL_SERVICES_RUNBOOK.md` §4e
- `wiki/decisions/2026-04-14-society-of-minds-charter.md`
- LAM issue #68 closeout (full integration history)

## Changelog

| Date | Change |
|---|---|
| 2026-04-15 | Stage A: Promoted Windows host from HP-critic-only to documented SoM Tier-2 fallback. Renumbered invariants 13–15 to 8–10. Added three exceptions covering PII middleware, audit trail, and activation gate. Windows rung marked "documented / disabled until Sprint 5." |
