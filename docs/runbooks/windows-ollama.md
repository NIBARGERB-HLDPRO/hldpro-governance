# Windows Ollama Runtime Runbook

## Current Status

Windows Ollama is deprecated/off the active Society of Minds governance waterfall as of issue #432. It remains LAN-only historical batch/health infrastructure unless a future issue explicitly reactivates it. It is not a Worker fallback and it is not allowed to receive PII-tagged or PII-detected payloads.

2026-04-17 governance-side probe:

- Endpoint checked: `http://172.17.227.49:11434/api/tags`
- Result: timeout from the Mac
- Prompt payloads sent: none
- Models verified live from Mac: none

## Hardware Resolution

Prior standards text described the Windows workstation as `64 GB RAM, 16 GB VRAM`. The active #224 plan records an operator conflict: 64 GB RAM with no verified VRAM.

This slice resolves the conflict conservatively:

- RAM: 64 GB remains a prior/operator-reported value until refreshed by direct host telemetry.
- VRAM: unverified; no active governance evidence supports the 16 GB VRAM assertion.
- Model placement: do not place Windows as a primary lane or rely on VRAM-specific placement until direct host telemetry is recorded.

## Health Probe

Run from the governance repo:

```bash
python3 scripts/lam/runtime_inventory.py --endpoint http://172.17.227.49:11434
```

The probe calls `/api/tags` only. It does not call `/api/generate`, `/v1/chat/completions`, or any endpoint that accepts prompt payloads.

Existing role-specific preflight remains available:

```bash
bash scripts/windows-ollama/preflight.sh --worker
bash scripts/windows-ollama/preflight.sh --critic
```

## Routing Boundary

- Windows role: deprecated/off active SoM ladder.
- PII-tagged payload: halt.
- PII detected by local patterns: halt.
- Missing PII patterns: halt.
- Endpoint unreachable: do not route to Windows.
- Endpoint reachable but required model missing: do not route to Windows.
- Endpoint reachable and model present: still do not route to Windows for governance waterfall work.
- Cloud fallback for PII: never allowed.

## Audit Boundary

Windows submissions, when allowed by a later routing decision, must continue through `scripts/windows-ollama/submit.py` so model allowlist, PII middleware, and audit-chain writing remain active.

This slice does not submit any prompt payload to Windows and does not alter the existing audit writer.
