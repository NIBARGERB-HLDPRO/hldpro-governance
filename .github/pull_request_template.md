<!--
Society of Minds PR template — mandatory for all PRs.
See STANDARDS.md §Society of Minds for the full charter.
-->

## Summary
<!-- 1-3 bullets on what changed and why -->

## Tier / Scope
- [ ] `implementation` (code changes only)
- [ ] `architecture` — requires Tier 1 cross-review artifact
- [ ] `standards` — requires Tier 1 cross-review artifact

## Society of Minds checklist
- [ ] Orchestrator model/session: `_______________`
- [ ] Planner model: `_______________` (e.g. `claude-opus-4-6`)
- [ ] Plan reviewer model: `_______________` (e.g. `gpt-5.4 high`; Spark only as logged fallback/specialist critique)
- [ ] Worker (code author) model: `_______________` (e.g. `claude-sonnet-4-6` or bounded local Qwen worker)
- [ ] QA reviewer model: `_______________` (e.g. Codex QA with explicit `-m` + `model_reasoning_effort`)
- [ ] If `architecture` or `standards`: cross-review artifact at `raw/cross-review/YYYY-MM-DD-*.md` with dual signatures (Architect-Claude + Architect-Codex, different model families, both signed)
- [ ] No PII in diff, OR if present, LAM-routed with `raw/lam-audit/*.manifest.json` attached
- [ ] No architecture/standards work performed on Haiku tier
- [ ] Any model fallbacks logged under `raw/model-fallbacks/YYYY-MM-DD.md`

## Test plan
- [ ] ...
- [ ] ...

## Handoff package evidence
- [ ] Structured plan: `docs/plans/_______________-structured-agent-cycle-plan.json`
- [ ] Execution scope: `raw/execution-scopes/_______________-implementation.json`
- [ ] Handoff package: `raw/handoffs/_______________-plan-to-implementation.json`
- [ ] Validation artifact: `raw/validation/_______________.md`
- [ ] Review artifact refs: `raw/cross-review/_______________.md` or `N/A - implementation only`
- [ ] Gate artifact refs: `_______________` or `N/A - command result below`
- [ ] Local CI evidence: `cache/local-ci-gate/reports/.../local-ci-*.json` or command result `tools/local-ci-gate/bin/hldpro-local-ci run --profile ... --json`
- [ ] Closeout: `raw/closeouts/_______________.md`
- [ ] Packet queue state: `_______________` or `N/A - no packet dispatch in this PR`

## Cross-review artifact (architecture / standards PRs only)
<!-- Paste path: raw/cross-review/YYYY-MM-DD-<slug>.md -->

## Fallback log entries (if any)
<!-- Paste path(s): raw/model-fallbacks/YYYY-MM-DD.md -->

🤖 Generated with [Claude Code](https://claude.com/claude-code)
