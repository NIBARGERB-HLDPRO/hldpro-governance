---
pr_number: 112
pr_scope: standards
drafter:
  role: architect-claude
  model_id: claude-opus-4-6
  model_family: anthropic
  signature_date: 2026-04-15
cross_drafter:
  role: worker-claude-fallback
  model_id: claude-sonnet-4-6
  model_family: anthropic
  signature_date: 2026-04-15
reviewer:
  role: architect-codex
  model_id: gpt-5.4
  model_family: openai
  signature_date: 2026-04-15
  verdict: REJECTED
invariants_checked:
  dual_planner_pairing: true
  no_self_approval: true
  planning_floor: true
  pii_floor: true
  cross_family_independence: true
---

## Summary
PR #112 is not mergeable as Stage A because it promotes Windows Ollama into the active Tier-2 ladder while the hard controls that make that route defensible are deferred, partially excepted, or not enforced at all. The largest failures are charter consistency and security: new invariants are numbered as 13-15 with no 8-12 hard-rule bridge, no enforcement-index rows, no audit exception, and a direct conflict with the existing PII floor. The operational runbook is useful, but the standard currently creates orphan hard rules and a live fallback path that can be selected before PII middleware, audit logging, model allowlisting, and failover preservation exist.

## Must-fix
- STANDARDS.md:335 — Hard-rule invariants jump from 7 to 13 and reference Remote MCP Bridge invariants #10-#12 that do not exist in this charter section; current #10-#12 are enforcement-index rows with different meanings — Renumber or explicitly introduce invariants 8-12, then update all mirror references so the terminology is internally coherent.
- STANDARDS.md:335 — Invariant #13 says Windows submission is allowed after `pii-patterns.yml`, but invariant #4 says detected/tagged PII routes through LAM only and never leaves that path — State unambiguously that Windows Ollama receives only non-PII/scrubbed payloads, and that PII detection blocks Windows and cloud fallback rather than attempting remote submission.
- STANDARDS.md:337 — Invariant #15 requires every Windows-Ollama call to append hash-chain/HMAC audit records and disables the endpoint on chain break, but the enforcement index has no CI row for this invariant and Stage B defers the artifacts — Add CI-verifiable enforcement now, or keep Windows Ollama disabled from the active ladder until the audit writer and validator land.
- STANDARDS.md:369 — The charter promise says every intent has a CI-verifiable artifact and no orphan rules, but invariants #13-#15 have no enforcement-index entries — Add rows for PII middleware, LAN exposure validation, Windows audit schema/chain validation, model allowlist validation, and failover behavior, with halt semantics.
- STANDARDS.md:271 — The Tier-2 ladder promotes Windows Ollama as an active fallback before the Stage B submission path exists — Either keep the Windows rung explicitly “documented only / disabled until Stage B” or include the Stage B submitter, PII gate, audit writer, allowlist, and fallback controls in this PR.
- STANDARDS.md:336 — “LAN trust assumed only because Mac and Windows share the same private subnet” is not a defensible threat boundary for an unauthenticated HTTP inference endpoint — Require Windows firewall binding/allowlisting to the Mac host or trusted subnet, no public bind/port-forwarding, and a documented exposure check before the endpoint is considered compliant.
- STANDARDS.md:434 — “Decision script falls through to next ladder rung” does not preserve the PII floor; after Windows failure the next rung is Sonnet, which is cloud — Specify that PII-tagged or PII-detected payloads never fall through to Windows or Sonnet; they must remain in LAM or halt.
- docs/exception-register.md:78 — The interim exception covers only PII middleware, while the PR also defers audit compliance, CI validation, submitter allowlisting, and failover controls — Expand the exception set with bounded expiries or remove active ladder promotion until all hard controls are present.
- docs/runbooks/windows-ollama-worker.md:67 — Manual operator PII confirmation contradicts the new fail-closed invariant when `pii-patterns.yml` middleware is unavailable — Make manual submission non-compliant/disabled for SoM payloads, or define a formal temporary exception that explicitly suspends use of the Windows rung.
- docs/runbooks/windows-ollama-worker.md:71 — Audit is declared future Stage B while STANDARDS.md makes it a current hard invariant — Either land the audit artifact path and CI validator now or mark Windows-Ollama SoM use as prohibited until audit is implemented.
- docs/runbooks/windows-ollama-worker.md:87 — Future epics omit the actual mandatory Stage B scope even though the runbook and exception depend on it — Add a Stage B stub with acceptance criteria for `submit.py`, PII middleware, allowlist, audit chain, CI validator, failover rules, and closeout evidence.
- scripts/windows-ollama/preflight.sh:15 — Preflight returns success if either pinned model is present, so a host with only `llama3.1:8b` passes even though the Tier-2 Worker route requires `qwen2.5-coder:7b` — Split worker and critic preflights or require `qwen2.5-coder:7b` for the Worker fallback path.
- scripts/windows-ollama/preflight.sh:31 — Model inventory parsing is ad hoc grep over JSON and will classify malformed/non-Ollama responses as “reachable but no pinned models” — Parse `/api/tags` with `jq` or a small owned parser and reserve exit 2 for a valid inventory with missing required worker model.

## Nice-to-have
- STANDARDS.md:271 — The Tier-2 row is hard to read because Fallback 2 now contains three sequential rungs — Replace the single cell chain with an ordered Tier-2 ladder table showing condition, model, locality, PII eligibility, audit requirement, and cost flag.
- docs/EXTERNAL_SERVICES_RUNBOOK.md:243 — Exit code wording repeats “at least one pinned model” and inherits the worker/critic ambiguity — Make the external runbook match the corrected preflight contract.
- raw/model-fallbacks/2026-04-14.md:37 — The fallback log says the operator skipped Qwen warm daemon “for momentum,” which conflicts with the ladder discipline unless an allowed override condition is documented — Either cite the applicable exception or record it as a policy deviation.

## Notes
- The LAM #68 operating contract is promoted mostly correctly: `keep_alive=15m`, `num_ctx<=4096`, `99 -> 80 -> 60`, and `45000ms` are consistent with the closeout evidence.
- The external-services cross-reference and new runbook are directionally useful, but they cannot compensate for missing enforcement rows on hard invariants.
- Stage A can be acceptable only as documentation if the active ladder is not changed yet. As written, it changes the active standard first and defers the safety machinery, so rejection is required.