# Issue #581 PDCAR: Governed Claude Review Path

Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/581
Branch: `issue-581-claude-review-path`

## Plan

Repair the governed Claude specialist-review path so bounded
alternate-family packet reviews reliably return a markdown verdict through the
approved `scripts/codex-review.sh claude` operator path, without reintroducing
repo-exploration defaults or alternate entrypoints.

## Do

Implementation scope for issue #581:

- preserve the issue-backed planning packet while promoting the lane to a
  bounded implementation scope after governed Claude review succeeded
- keep `scripts/codex-review.sh claude` as the only operator-facing path
- make the shared Claude review template treat the caller prompt as the full
  packet scope instead of asking Claude to explore the repo
- default the reviewer lane to `claude-opus-4-6`, `bypassPermissions`, no tool
  access, `max_turns=8`, and a longer silence timeout so bounded packet review
  returns markdown instead of max-turn or idle-timeout failures
- document the rationale and override mechanism in `STANDARDS.md` and
  `docs/EXTERNAL_SERVICES_RUNBOOK.md`
- add a dry-run regression check for the revised contract

## Check

Before implementation:

- the issue-581 packet and reproduction evidence validate
- base Claude CLI preflight proves token/bootstrap health separately from the
  governed wrapper defect
- alternate-family review is captured through the governed wrapper path

After implementation:

- `scripts/codex-review.sh claude` returns a bounded markdown review artifact
  for a self-contained packet prompt
- the template defaults no longer rely on repo exploration or hidden tool-use
  behavior
- docs and dry-run output agree on the canonical packet-review contract
- validation proves the original `max turns` / `idle_timeout` failure mode is
  replaced by a successful governed review replay

## Adjust

If larger packets still need more than `max_turns=8`, keep the SSOT path and
require execution scopes to raise `CLAUDE_REVIEW_MAX_TURNS` explicitly rather
than widening the default contract. Do not add a second operator-facing review
path or reintroduce repo-exploration defaults.

## Review

Alternate-family review is now recorded through the governed wrapper path in
`docs/codex-reviews/2026-04-29-claude.md` and summarized in
`raw/cross-review/2026-04-29-issue-581-claude-review-path.md`.
Review outcome: `APPROVED_WITH_CHANGES`, requiring the repo docs to explain why
`bypassPermissions` remains read-only in practice for this lane and to document
the opt-in override path for larger packets or explicit tool access. Those
follow-ups are folded into this implementation slice.
