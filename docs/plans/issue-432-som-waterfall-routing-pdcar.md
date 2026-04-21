# PDCA/R - Issue #432 SoM Waterfall Routing

Date: 2026-04-21
Issue: https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/432

## Plan

Revise the governance Society of Minds routing source of truth so Codex
orchestrates, Opus 4.6 plans, GPT-5.4 high reviews plans, Spark remains a
fallback/specialist critique path only when GPT-5.4 is unavailable, Sonnet 4.6
is the primary Worker, Codex QA reviews implementation, local Qwen workers
handle bounded implementation chunks, Gemma remains A/B shadow-only, and
Windows Ollama is off the active governance waterfall.

## Do

- Update `STANDARDS.md` and governance mirrors.
- Update LAM runtime inventory and policy checks.
- Update Windows decision behavior so `WINDOWS` is not a success route.
- Update templates, runbooks, and hook wording.
- Preserve downstream repo propagation as issue-backed follow-up work.

## Check

Focused validation:

- structured plan validation
- execution scope validation
- LAM family / worker ladder / Gemma shadow policy check
- runtime inventory tests
- Windows off-ladder decision tests
- delegation hook tests
- local CI gate

## Adjust

Windows tooling remains in-tree as deprecated historical infrastructure. This
slice changes active governance routing and guardrails; deletion or repurposing
of Windows scripts should be a separate issue if desired.

## Review

Architecture/standards scope uses the cross-review artifact at
`raw/cross-review/2026-04-21-issue-432-som-waterfall-routing.md`. Gemma output
is not used as approval authority.
