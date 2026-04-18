# HITL Relay Security And Data-Handling Policy

Issue: [#302](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/302)
Parent epic: [#296](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/296)
Status: ACTIVE POLICY

## Purpose

This policy defines what the always-on SoM HITL relay may send through AIS-backed messaging channels, what must stay local, how inbound replies are verified and retained, and what evidence must exist for audit replay.

The relay path is:

```text
local CLI checkpoint
-> HITL packet
-> local SoM/MCP orchestrator
-> AIS outbound notification
-> operator reply
-> AIS inbound event
-> local normalizer and governance gate
-> session instruction or resume packet
```

AIS is transport only. Governance policy, normalization, validation, and session instruction emission remain outside AIS.

## Data Classification

| Classification | May leave local control? | Rule |
|---|---:|---|
| `public` | Yes | May be included in notification bodies if relevant. |
| `internal` | Yes, minimized | Send only the decision prompt, issue/PR links, check status, and short summary. |
| `sensitive` | Conditional | Redact payload details; send only references and a minimal decision prompt. |
| `pii` | No by default | Must fail closed unless a local-only operator channel is explicitly approved. |

PII-tagged or PII-detected packets must not be sent to cloud LLMs, Windows fallback, SMS, Slack, email, or other external channels unless a later issue records an explicit exception and local-only route.

## Payload Minimization

Outbound notification bodies must prefer references over content:

- include issue number, repo, branch, PR/check links, requested decision, and allowed response actions;
- include short summaries only when data classification permits it;
- omit raw diffs, logs, secrets, patient/client/user data, tokens, local paths containing sensitive names, and unredacted exception traces;
- include `notification_id` so replies can be correlated without repeating sensitive context.

For `sensitive` packets, AIS receives a minimized message and opaque references. The local orchestrator retains the richer context.

## Redaction Before AIS Or AI Hops

Before a HITL notification leaves the local orchestrator:

1. Classify the packet with `policy.data_classification` and `policy.pii_mode`.
2. Redact secrets, tokens, credentials, phone numbers, email addresses, access keys, patient/client identifiers, and raw message bodies.
3. Replace redacted fields with evidence references or hashes when audit replay requires proof.
4. Refuse dispatch if classification or redaction cannot complete.

The LLM normalizer may receive raw inbound reply content only through a local route unless the reply is classified non-sensitive and policy allows cloud processing.

## Raw Message Retention

Raw inbound and outbound message bodies are not stored in executable packets.

Required retention rules:

- executable packets store `raw_message_ref`, not `raw_message_body`;
- raw message stores must be access-controlled and scoped to the relay service;
- retention defaults to 30 days unless a narrower channel policy applies;
- deletion must preserve audit references, IDs, hashes, timestamps, sender verification result, and normalized decision;
- final closeout must not paste raw sensitive message bodies.

## Sender Verification

Inbound replies must fail closed unless AIS records:

- channel;
- sender reference;
- message ID;
- notification ID or correlation key;
- received timestamp;
- sender verification result;
- duplicate/replay status;
- expiration status.

Unknown senders, unsigned webhooks, failed signatures, expired replies, and uncorrelated replies cannot produce session instructions.

## Webhook Replay And Duplicate Handling

AIS inbound events must be idempotent by `message_id` and `notification_id`.

Required behavior:

- duplicate valid replies return the existing response event or a duplicate marker;
- replayed webhook payloads are refused or marked duplicate;
- expired notification replies are refused or converted into a clarification event;
- conflicting replies for the same notification require local orchestrator clarification.

## Token And Secret Scope

AIS and MCP integration credentials must use the narrowest workable scope:

- AIS outbound sender credentials may send messages only through configured channels;
- AIS inbound webhook secrets may verify signatures only;
- local orchestrator tokens may read/write only the approved relay queues and packet artifacts;
- GitHub tokens used in closeout or issue comments must not be exposed to AIS payloads;
- secrets must never be included in notification text, packet fields, closeouts, or audit excerpts.

## Channel Rules

| Channel | Initial status | Notes |
|---|---|---|
| Local fixture | Allowed | Required for dry-run and CI-safe E2E. |
| SMS | Planned | Allowed only for non-PII minimized prompts after sender verification exists. |
| Slack | Planned | Allowed only for non-PII minimized prompts after app signing and sender verification exist. |
| Email | Deferred | Requires a separate retention and sender-verification review. |
| Other | Disabled | Must be added by issue-backed policy update. |

Initial epic acceptance requires at least one real or sandboxed AIS-backed transport. SMS and Slack are not both mandatory unless a later issue makes both mandatory.

## Audit Replay Evidence

The final E2E proof must reconstruct a decision using:

- session ID;
- HITL request packet ID;
- notification ID;
- sender verification result;
- inbound message/event ID;
- raw message reference or hash;
- normalized decision;
- governance validator result;
- instruction or resume packet ID;
- local session consumption or resume evidence.

Audit replay should prove the decision path without exposing unnecessary raw content.

## Fail-Closed Conditions

The relay must refuse or halt when:

- `pii_mode` is `tagged`, `detected`, or `lam_only` and no local-only route is approved;
- data classification is missing or unknown;
- sender verification fails;
- webhook signature is missing or invalid;
- notification ID is missing, expired, replayed, or uncorrelated;
- normalized decision action is outside the allowed vocabulary;
- session ID does not match the target session;
- raw human text would be used as terminal input;
- required audit evidence is missing.

## Closeout Requirement

Every implementation slice that touches AIS, MCP, validators, or session adapters must cite this policy and record whether it changed the data classification, retention, sender verification, token scope, or channel rule.
