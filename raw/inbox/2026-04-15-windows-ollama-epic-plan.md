---
date: 2026-04-15
planner: claude-opus-4-6
role: tier-1-planner-claude
execution_mode: autonomous-loop-no-hitl
orchestrator: claude-haiku-4-5-20251001
worker_primary: gpt-5.3-codex-spark (available after ~03:30 CDT 2026-04-15)
worker_fallback_now: claude-sonnet-4-6 (cost-flagged, per Tier-2 step 4)
qa: claude-sonnet-4-6 (separate subagent — distinct identity via fresh context)
cross_reviewer: gpt-5.4 @ model_reasoning_effort=high (via codex exec)
gate: gpt-5.4 @ model_reasoning_effort=medium (distinct from drafter + QA)
related_pr: 112 (REJECTED by gpt-5.4 — this plan revises)
---

# Epic — Windows-Ollama SoM Tier-2 integration

End state: Windows host (`172.17.227.49:11434`, 64 GB RAM / 16 GB VRAM) is a fully-controlled, active SoM Tier-2 Worker fallback. PII middleware, audit trail, CI validation, firewall binding, and failover PII-preservation all enforced. Ladder rung activated only after controls land.

## Phases

| Phase | Goal | Sprints | Deliverable |
|---|---|---|---|
| 1 — Standards & Documentation | Revise PR #112 to "documented / disabled" per gpt-5.4 REJECTED verdict | Sprint 1 | PR #112 merged as Stage A |
| 2 — Runtime Controls | Land PII middleware + audit + CI + activation | Sprints 2-5 | Windows rung active |
| 3 — Future Features | Off-LAN, WoL, health-check | Stubbed in Stage A; issues opened in Phase 1 | Deferred epics |

## Orchestration contract (Haiku executes)

```
for each sprint in [1, 2, 3, 4, 5]:
    1. open GH issue for sprint (title + body per §Sprint N below)
    2. create worktree from origin/main with branch per §Sprint N
    3. log fallback (if applicable) via scripts/model-fallback-log.sh
    4. spawn WORKER subagent with §Sprint N worker brief
       - if codex-spark available (preflight): use gpt-5.3-codex-spark high
       - else: use sonnet (cost-flagged)
       - on worker report STOP/BLOCKED: escalate to §Escalation rules
    5. spawn QA subagent (always sonnet) with §Sprint N QA checklist
       - if QA REJECTS: re-spawn worker with QA findings; max 3 rounds
    6. fire Tier-1 cross-review (gpt-5.4 high via codex exec) with §Sprint N cross-review brief
       - if REJECTED: re-spawn worker with must-fixes; max 2 rounds
    7. fire Tier-4 gate (gpt-5.4 medium via codex exec) with §Sprint N gate brief
       - if FAIL: escalate
    8. commit + push all artifacts; merge PR
    9. file Stage 6 closeout + wiki cross-link per §Sprint N closeout
    10. update MEMORY.md / OVERLORD_BACKLOG.md
    11. next sprint
```

**Halt conditions (Haiku stops and reports):**
- gpt-5.4 quota-blocked (check after every 2 cross-reviews)
- Any sprint exceeds 4 round-trips (worker → QA → worker → QA → cross-review → worker → cross-review)
- Merge blocked by infrastructure (ruleset, CI missing) not resolvable without operator
- Any negative test fails in Sprint 5 (real security — must not silently bypass)

**Opportunistic switch to codex-spark:** Haiku MUST re-run `bash scripts/codex-preflight.sh --log` between sprints. If codex-spark is OK, subsequent sprints use spark as worker (switching mid-sprint is NOT required — finish the current sprint with whatever worker started it).

## Sprint 1 — Revise PR #112 per gpt-5.4 REJECTED verdict

**GH issue title:** `Epic Phase 1 Sprint 1: revise PR #112 (Windows-Ollama Stage A) for gpt-5.4 must-fixes`

**GH issue body:**
```
Parent epic: Windows-Ollama SoM Tier-2 integration
Depends on: PR #112 (open, DRAFT, REJECTED by Tier-1 cross-review gpt-5.4)
Cross-review artifact: raw/cross-review/2026-04-15-windows-ollama-tier2.md (commit 2e3f968)

## Scope

Apply all 13 must-fixes from the gpt-5.4 cross-review. Change Stage A from "activated" to "documented / disabled until Stage B controls land."

## Acceptance criteria

1. Invariants renumbered 13→8, 14→9, 15→10 (Remote MCP Bridge's #8-12 don't exist yet).
2. Tier-2 ladder cell does NOT activate Windows rung. Adds explicit "activated in Sprint 5" marker.
3. Invariant #8 (PII floor reinforcement) makes PII-tagged payloads block BOTH Windows AND Sonnet cloud fallback. LAM-only or halt.
4. Invariant #9 adds Windows firewall binding requirement (Mac host IP or trusted subnet allowlist). No public bind / port-forward.
5. Invariant #10 declares audit; notes enforcement via Sprint 3 CI workflow; endpoint disabled until then.
6. Enforcement index gets 3 new rows (one per invariant) pointing at Sprint 2/3 artifacts with halt semantics.
7. Exception register expanded to 3 entries expiring 2026-05-15: SOM-WIN-OLLAMA-PII-001, SOM-WIN-OLLAMA-AUDIT-001, SOM-WIN-OLLAMA-DISABLED-001.
8. Runbook: remove "manual PII confirm" language; add explicit "not approved for SoM routing until Sprint 5"; add Stage B acceptance-criteria stub.
9. Preflight script split into `--worker` (requires qwen2.5-coder:7b) and `--critic` (requires llama3.1:8b) modes. Parse /api/tags with jq.
10. Fallback log entry reworded: cite SOM-WIN-OLLAMA-DISABLED-001 instead of "momentum."
11. External services runbook §4e matches corrected preflight contract.
12. gpt-5.4 round-2 cross-review APPROVED.
13. Tier-3 Sonnet QA APPROVED.
14. Tier-4 gate (gpt-5.4 medium) PASS.
15. PR merged, closeout filed.
```

**Labels:** `epic:windows-ollama`, `phase:1`, `sprint:1`, `priority:p1`.

**Worktree:** existing `_worktrees/gov-windows-ollama` on branch `feat/windows-ollama-tier2`. One new commit on top of current HEAD `d144776`.

**Worker brief:**
```
You are the Tier-2 Worker applying gpt-5.4's round-1 must-fixes to PR #112.
Read raw/cross-review/2026-04-15-windows-ollama-tier2.md for the full findings.
Apply the 13 must-fixes exactly as specified in the issue ACs (numbered 1-11 above; 12-15 are gate outcomes not code changes).
Do not redesign beyond what the ACs specify.
Preserve existing cross-review artifact — do not overwrite or modify.
Single commit with message: "fix(standards): Windows-Ollama Stage A round-2 revision per gpt-5.4 cross-review"
Report: files touched, line-count deltas, any spec ambiguities (STOP if any).
```

**QA checklist (Sonnet):**
- Each of the 13 ACs satisfied? Pull the PR diff and verify line-by-line against `raw/cross-review/2026-04-15-windows-ollama-tier2.md` must-fixes.
- Markdown tables render; invariant numbering coherent (no gaps); enforcement index rows align with invariants.
- Preflight `--worker` and `--critic` both parse `/api/tags` output correctly; exit codes correct for both modes.
- Exception register entries follow the schema (rule_id, repo, deferral_reason, approver, expiry_date, review_cadence).
- Runbook Stage B acceptance-criteria stub lists: submit.py, PII middleware, audit writer, CI validator, allowlist, failover rules.
- Verdict: APPROVED / APPROVED_WITH_CHANGES / REJECTED with line-level findings.

**Cross-review brief (gpt-5.4 high):**
Re-fire using the same prompt as round 1 (see the existing cross-review artifact). Scope: same 5 checks (charter consistency, security, operational soundness, integration, scope discipline). Must produce a new artifact `raw/cross-review/2026-04-15-windows-ollama-tier2-round2.md`.

**Gate brief (gpt-5.4 medium):**
```
You are the Tier-4 Gate verifier for PR #112 round-2.
Check only: (a) cross-review artifact round 2 verdict == APPROVED or APPROVED_WITH_CHANGES, (b) all must-fixes from round 2 applied if APPROVED_WITH_CHANGES, (c) no net-new files outside scope, (d) markdown lints clean, (e) preflight script bash -n clean.
PASS / FAIL only. No other commentary.
```

**Closeout:**
- `raw/closeouts/2026-04-15-windows-ollama-stage-a.md` from TEMPLATE.md
- Wiki cross-link: `wiki/decisions/2026-04-15-windows-ollama-stage-a.md` linking to SoM charter wiki
- Update `OVERLORD_BACKLOG.md` moving this sprint to "Done"

## Sprint 2 — Worker submission script + PII middleware + model allowlist

**GH issue title:** `Epic Phase 2 Sprint 2: Windows-Ollama submit.py + PII middleware + model allowlist`

**GH issue body:**
```
Parent epic: Windows-Ollama SoM Tier-2 integration
Depends on: Sprint 1 merged

## Scope

Land `scripts/windows-ollama/submit.py` — the authoritative SoM Tier-2 Worker submission path for the Windows host endpoint. Includes PII pre-check middleware, model allowlist, and failover PII-preservation rules.

## Acceptance criteria

1. `scripts/windows-ollama/submit.py` — Python 3.11, stdlib + requests only. Entrypoint accepts prompt JSON + target model from allowlist. Rejects with structured error if PII detected, model not in allowlist, endpoint unreachable.
2. `scripts/windows-ollama/pii_patterns.yml` — regex pattern set mirroring Remote MCP Bridge `scripts/lam/pii-patterns.yml`. Covers: ssn, phone, email, dob, credit_card, field_marker.
3. `scripts/windows-ollama/model_allowlist.yml` — explicit allowlist: `qwen2.5-coder:7b` for worker role; extensible per runbook.
4. Failover PII-preservation: if payload PII-tagged and Windows unreachable, submit.py exits with `pii_halt` error. Never falls through to cloud.
5. `scripts/windows-ollama/tests/test_submit.py` — negative tests: PII in prompt, non-allowlisted model, unreachable endpoint, malformed /api/generate response, empty rationale from model.
6. All tests pass locally via pytest.
7. Tier-3 Sonnet QA APPROVED.
8. Tier-1 gpt-5.4 cross-review APPROVED.
9. Tier-4 gate PASS.
```

**Labels:** `epic:windows-ollama`, `phase:2`, `sprint:2`, `priority:p1`.

**Worktree:** new `_worktrees/gov-windows-ollama-sprint2` off `origin/main` after Sprint 1 merges. Branch `feat/windows-ollama-sprint2`.

**Worker brief:**
```
You are the Tier-2 Worker implementing Sprint 2.
Reference: scripts/windows-ollama/preflight.sh (existing) — follow the same style (stdlib + minimal deps).
Reference: docs/runbooks/windows-ollama-worker.md (post-Sprint-1) for the endpoint contract.
Reference: Remote MCP Bridge PII middleware design (see `raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` §"Application-layer PII enforcement") for pattern.
Deliver: submit.py + pii_patterns.yml + model_allowlist.yml + tests/test_submit.py.
Use requests 2.31+. Include __all__, type hints, no bare exceptions.
Do NOT activate the Tier-2 ladder rung — that's Sprint 5.
Commit message: "feat(windows-ollama): submission path + PII middleware + allowlist"
Report: file paths + line counts + test-pass evidence.
```

**QA checklist (Sonnet):**
- PII patterns match Remote MCP Bridge pattern set byte-for-byte where applicable
- Failover PII preservation: verify by dry-run with PII-tagged prompt + Windows unreachable (mock) → must exit with pii_halt
- Allowlist enforces qwen2.5-coder:7b for worker role; rejects everything else
- Empty rationale rejected via local schema check (mirror LAM #68 operating rule)
- Tests cover the 5 negative cases from AC #5
- No logging of prompt payload; no echo of request body in error messages (PII-safe)
- Verdict + line-level findings

**Cross-review brief (gpt-5.4 high):**
Same 5-check framework. Especially: does the PII middleware mirror Remote MCP Bridge patterns tightly? Does the failover rule preserve invariant #8 (no PII to cloud)? Is the allowlist enforceable (no way to bypass)?

**Gate brief (gpt-5.4 medium):**
Check: all tests pass via `pytest scripts/windows-ollama/tests/`, no new files outside scope, no active ladder change, cross-review round-2 APPROVED.

**Closeout:** `raw/closeouts/2026-04-15-windows-ollama-sprint2.md` + wiki cross-link.

## Sprint 3 — Audit writer + daily manifest + local verifier

**GH issue title:** `Epic Phase 2 Sprint 3: Windows-Ollama audit writer + hash-chain + daily manifest`

**GH issue body:**
```
Parent epic: Windows-Ollama SoM Tier-2 integration
Depends on: Sprint 2 merged

## Scope

Land audit trail for every Windows-Ollama call per invariant #10. Hash-chained, HMAC-signed, daily-manifested. Matches Remote MCP Bridge audit format.

## Acceptance criteria

1. `scripts/windows-ollama/audit.py` — append-only writer to `raw/remote-windows-audit/YYYY-MM-DD.jsonl`.
2. Entry shape: `{ts, seq, prev_hash, principal, session_jti, tool, args_hmac, status, reject_reason, latency_ms, entry_hmac}`.
3. HMAC key via env `SOM_WINDOWS_AUDIT_HMAC_KEY`; signing via hmac_sha256 over canonical JSON.
4. Per-line hash chain; entry 0 prev_hash = zero.
5. Daily manifest `raw/remote-windows-audit/YYYY-MM-DD.manifest.json` with {first_hash, last_hash, entry_count, sha256_of_file}.
6. File permissions 0600; append-only flag where possible (`chflags uappnd` on macOS).
7. Local verifier `scripts/windows-ollama/verify_audit.py` — same logic as future CI workflow. Exit 0 pass, 1 fail.
8. submit.py from Sprint 2 now calls audit.py per request.
9. Tests for: chain integrity, HMAC forgery detection, manifest mismatch, file truncation, replay detection.
10. All standard tiers pass.
```

**Labels, worktree, worker brief, QA, cross-review, gate, closeout:** same structure as Sprint 2. Worktree `gov-windows-ollama-sprint3`, branch `feat/windows-ollama-sprint3`. Reference Remote MCP Bridge audit design (`raw/inbox/2026-04-14-remote-mcp-bridge-plan.md` §"Audit trail — tamper-evident"). Closeout at `raw/closeouts/2026-04-15-windows-ollama-sprint3.md`.

## Sprint 4 — CI workflows (audit schema + exposure check)

**GH issue title:** `Epic Phase 2 Sprint 4: Windows-Ollama CI workflows (audit + exposure)`

**GH issue body:**
```
Parent epic: Windows-Ollama SoM Tier-2 integration
Depends on: Sprint 3 merged

## Scope

CI enforcement for invariants #9 and #10.

## Acceptance criteria

1. `.github/workflows/check-windows-ollama-audit-schema.yml` — runs verify_audit.py on any PR touching raw/remote-windows-audit/**; also workflow_dispatch. Fails on any audit chain break or HMAC mismatch.
2. `.github/workflows/check-windows-ollama-exposure.yml` — runs a static check against docs/runbooks/windows-ollama-worker.md + scripts/windows-ollama/submit.py to assert (a) no public-internet bind documented, (b) endpoint URL still `172.17.227.49:11434` (change requires explicit approval PR), (c) Cloudflare Tunnel section remains stubbed.
3. Both workflows registered in STANDARDS.md enforcement-index table.
4. Sprint 1 exception-register entries updated: SOM-WIN-OLLAMA-AUDIT-001 now has active CI enforcement; can be closed or scope-reduced.
5. Both workflows pass on this branch (self-green).
6. actionlint clean on both YAML files.
7. All tiers pass.
```

**Labels, worktree, etc.:** Sprint 4 worktree `gov-windows-ollama-sprint4`. Branch `feat/windows-ollama-sprint4`. Closeout `raw/closeouts/2026-04-15-windows-ollama-sprint4.md`.

## Sprint 5 — Activation + decision script + integration tests

**GH issue title:** `Epic Phase 2 Sprint 5: activate Windows-Ollama as Tier-2 rung + decision script`

**GH issue body:**
```
Parent epic: Windows-Ollama SoM Tier-2 integration
Depends on: Sprint 4 merged

## Scope

Flip the Tier-2 ladder rung from "documented / disabled" to ACTIVE. Add the decision script that routes between local warm daemon / Windows / cloud.

## Acceptance criteria

1. `scripts/windows-ollama/decide.sh` — decision tree: returns LOCAL / WINDOWS / CLOUD / HALT based on (a) packet PII flag, (b) local warm daemon status, (c) Windows preflight, (d) codex-spark availability. Never routes PII to WINDOWS or CLOUD.
2. `scripts/windows-ollama/tests/test_decide.sh` — covers 8 decision states (PII-yes/no × local-up/down × windows-up/down × spark-yes/no). All pass.
3. STANDARDS.md Tier-2 ladder cell updated: Windows rung now ACTIVE. Remove "activated in Sprint 5" marker.
4. Close all 3 Sprint 1 exceptions (SOM-WIN-OLLAMA-PII-001, SOM-WIN-OLLAMA-AUDIT-001, SOM-WIN-OLLAMA-DISABLED-001) — controls are live.
5. Runbook updated: replace "not approved for SoM routing" language; document the decision-script entry point.
6. Integration test: submit.py + audit.py + decide.sh in end-to-end flow on a synthetic (non-PII) prompt against live Windows host (preflight gate — skip if unreachable with clear skip marker, not hard fail).
7. All tiers pass.
```

**Worktree:** `gov-windows-ollama-sprint5`. Branch `feat/windows-ollama-sprint5`. Closeout `raw/closeouts/2026-04-15-windows-ollama-sprint5.md`.

## Phase 3 future epics (open as issues only, not executed in this run)

### Issue: Cloudflare Tunnel exposure for Windows-Ollama (off-LAN access)

```
Parent epic: Windows-Ollama SoM Tier-2 integration
Phase: 3 — deferred

## Scope

Expose Windows-Ollama beyond LAN via Cloudflare Tunnel. Requires Cloudflare Access mandatory per invariant #9. Mirrors Remote MCP Bridge tunnel pattern.

## Gate

Priority: LOW. Trigger: operator needs off-LAN access (working from a different network than the Windows host). Until then, LAN-only is fine.
```

Labels: `epic:windows-ollama`, `phase:3`, `status:deferred`.

### Issue: Wake-on-LAN for Windows-Ollama host

```
Parent epic: Windows-Ollama SoM Tier-2 integration
Phase: 3 — deferred

## Scope

BIOS auto-on + magic-packet sender on Mac side + launchd wake-timer. Makes the Windows host resilient to sleep states.

## Gate

Priority: LOW. Trigger: operator observes repeated preflight-unreachable events because Windows has slept. Until then, assume always-on.
```

### Issue: Windows-Ollama health-check workflow

```
Parent epic: Windows-Ollama SoM Tier-2 integration
Phase: 3 — deferred

## Scope

Periodic CI workflow (cron) that pings the Windows endpoint from a GitHub-hosted runner (via Cloudflare Tunnel — depends on Phase 3 tunnel issue landing first) and emits an issue if unreachable for > 1 hour.

## Gate

Priority: LOW. Depends on Cloudflare Tunnel issue.
```

## Escalation rules

1. **Worker report BLOCKED** — Haiku inspects block reason. If it's a spec gap, log + halt. If it's a quota/env issue, retry once on fallback tier; if still blocked, halt.
2. **QA REJECTED 3× in a row** on same sprint — halt. Indicates plan drift.
3. **gpt-5.4 REJECTED 2× in a row** on same sprint — halt. Escalate with the two artifacts attached.
4. **Tier-4 gate FAIL** — halt. Gate failures are definitive.
5. **CI red on merge** — re-fire worker for fix; if red persists after fix attempt, halt.

In all halt cases: Haiku writes final report to `raw/handoff/2026-04-15-windows-ollama-halt-<sprint>.md` and stops.

## Reporting contract

Haiku reports back to Opus:
- After each sprint: one-paragraph status (merged SHA, PR #, closeout path)
- On halt: full halt artifact content
- On epic completion: end-to-end summary + 5 merged PR numbers + memory update (spark-back-online confirmation if applicable)

No HITL. No questions back to Opus between sprints.
