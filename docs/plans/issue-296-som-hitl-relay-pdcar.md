# PDCAR: Always-On SoM HITL Relay For Local CLI Sessions

Date: 2026-04-18
Repo: `hldpro-governance`
Branch: `issue-296-som-hitl-relay-planning-20260418`
Epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: PLANNING_PACKAGE
Canonical plan: `docs/plans/issue-296-structured-agent-cycle-plan.json`

## Problem

Local CLI sessions can complete epics or stop at human-in-the-loop checkpoints, but the current governed path does not provide an always-on relay that can notify the operator outside the terminal, collect review or approval through AIS-backed messaging channels, normalize that response, and route a bounded instruction back to the correct local session.

Without a governed relay, the risks are:

- completed or blocked local sessions can wait silently in a terminal;
- operator feedback can be disconnected from the session that needs it;
- external messaging could become unsafe if freeform text is injected into a terminal;
- an always-on LLM could accidentally become an approval actor instead of a relay/normalizer;
- notification success could be mistaken for end-to-end governed session control.

## Plan

Build the capability as a queue-first HITL relay:

```text
local CLI session
-> governed session/HITL packet
-> always-on SoM/MCP orchestrator
-> AIS outbound notification
-> operator reply by SMS/Slack/other channel
-> AIS inbound reply event
-> orchestrator response normalization and governance gates
-> structured session instruction packet
-> local CLI session resumes or creates a resume packet
```

Repo ownership:

- `hldpro-governance`: packet contracts, deterministic validators, acceptance criteria, issue/plan/scope policy, and closeout evidence.
- `local-ai-machine`: always-on MCP/orchestrator runtime, session registry, queue watcher, LLM normalizer runtime, and local resume path.
- `ai-integration-services`: outbound notifications, inbound webhooks, sender verification, correlation, retries, and delivery audit.

Design guardrails:

- external replies become bounded decisions, never terminal input;
- AIS remains transport, not governance authority;
- the always-on LLM may summarize and normalize, but cannot self-approve or waive gates;
- queue-first packet flow comes before MCP push or live terminal adapters;
- final acceptance requires E2E evidence across approval, request-changes, ambiguous-response, stale-session, and audit replay paths.

## Do

Planning sequence:

1. Create GitHub epic issue #296.
2. Create the canonical structured JSON plan and this PDCAR companion.
3. Create planning execution-scope evidence for the artifact surface.
4. Mirror active planning status in backlog/progress files.
5. Validate the planning package locally.
6. Update issue #296 with artifact links and current status.
7. Hold implementation and child issue creation until cross-review or explicit operator approval.

Implementation phases after planning approval:

| Phase | Purpose | Implementation Timing |
|---|---|---|
| Phase 1 | Governance HITL packet contracts | After planning review |
| Phase 2 | Governance validators and policy gates | After packet contract approval |
| Phase 3 | Queue-first local relay prototype | After validator contract exists |
| Phase 4 | AIS outbound/inbound messaging bridge | After transport contract approval |
| Phase 5 | SoM/MCP orchestrator and LLM normalizer | After queue and AIS contracts are stable |
| Phase 6 | Local CLI adapter and session consumption | After orchestrator instruction contract is stable |
| Phase 7 | Final E2E HITL relay proof | Final epic acceptance gate |

## Check

Planning checks:

- `python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root . --branch-name issue-296-som-hitl-relay-planning-20260418 --require-if-issue-branch`
- Governance-surface plan gate over changed files.
- Planner-boundary execution-scope check over changed files.
- JSON parse for `docs/plans/issue-296-structured-agent-cycle-plan.json`.
- Git status confirms no runtime code or sibling repo files changed.

Implementation check families:

- schema validation for HITL request, response, decision, audit, and instruction packets;
- no-self-approval validation;
- sender identity and notification correlation validation;
- allowed-action validation;
- ambiguity confidence threshold validation;
- stale-session and wrong-session refusal tests;
- PII/channel policy fail-closed tests;
- replay/audit reconstruction tests;
- closeout and gate evidence before done state.

## Act

Act rules for this epic:

- If the planning package fails validation, revise the PDCAR/structured plan before any child issue creation.
- If alternate-family review rejects or requires changes, apply those changes before implementation slices begin.
- If a slice proposes raw message-to-terminal input, halt and redesign around structured instruction packets.
- If AIS design starts carrying governance authority, move that authority back to the governance/MCP contract.
- If a session is stale or disconnected, create a resume packet rather than targeting another active session.
- If E2E proof finds a policy gap, create a follow-up issue and keep #296 open.

## Review

Required before implementation:

- alternate-family/cross-review of the planning package;
- security/privacy review of SMS/Slack/other channel handling;
- SoM governance review for no-self-approval and tier boundaries;
- AIS transport review for sender verification, correlation, retry, duplicate, and expired-notification handling;
- MCP/local runtime review for session identity, stale session handling, and local-only PII behavior.

Current review state:

- Operator approved beginning the PDCAR loop on 2026-04-18.
- This planning package is not runtime implementation approval.
- Child implementation issues should be created only after review or explicit operator approval.

## Acceptance Criteria

- [ ] Issue #296 exists as the governing epic.
- [ ] Canonical structured plan exists and validates.
- [ ] PDCAR companion exists and matches the JSON plan.
- [ ] Planning execution-scope evidence exists for the changed governance-surface files.
- [ ] Backlog and progress mirrors reference issue #296.
- [ ] Phase decomposition records repo ownership, acceptance criteria, validation expectations, and closeout expectations.
- [ ] No runtime code, AIS code, local-ai-machine code, or sibling repo files are changed in the planning slice.
- [ ] Alternate-family/cross-review is required before implementation slices modify governed runtime or transport surfaces.

## Final E2E Acceptance Criterion

Issue #296 must remain open until an evidence-backed E2E run proves:

```text
local CLI checkpoint
-> HITL packet
-> orchestrator validation
-> AIS outbound notification
-> operator reply
-> AIS inbound event
-> LLM normalization
-> governance gate
-> session instruction packet
-> local CLI consumes instruction or creates resume packet
-> closeout evidence
```

The final E2E suite must include:

- approval path: a validated operator approval produces a bounded instruction consumed by the correct local session;
- request-changes path: feedback is routed back without being treated as approval;
- ambiguous-response path: clarification is requested and no instruction is emitted;
- stale-session path: a resume packet is created instead of injecting into the wrong session;
- audit replay path: the decision can be reconstructed from packet, AIS, normalization, validation, and session evidence.

## Initial Child Issue Map

Child issues should be created after planning review or explicit operator approval:

| Slice | Repo | Purpose | Final AC |
|---|---|---|---|
| HITL packet contracts | `hldpro-governance` | Define request/response/decision/audit/instruction schemas | Contract fixtures validate and reject malformed packets |
| HITL validators | `hldpro-governance` | Enforce allowed action, provenance, no-self-approval, ambiguity, stale-session, and PII/channel policy | Negative-control tests fail closed |
| Queue-first prototype | `hldpro-governance` / `local-ai-machine` | Prove local queue relay without external messaging | Local fixture path emits instruction/resume/clarification packets |
| AIS outbound/inbound bridge | `ai-integration-services` | Deliver notifications and receive correlated replies | Sender/correlation/retry/expired/duplicate paths tested |
| SoM/MCP normalizer | `local-ai-machine` | Normalize replies into bounded decisions and emit instruction packets | Low-confidence and disallowed actions refused |
| Local CLI adapter | governed CLI/session layer | Emit checkpoints and consume addressed instruction packets | Raw text is never executed; stale sessions resume safely |
| E2E HITL relay proof | cross-repo | Full local-to-human-to-local run | All final E2E paths pass with evidence |
