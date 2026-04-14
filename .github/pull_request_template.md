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
- [ ] Worker (code author) model: `_______________` (e.g. `gpt-5.3-codex-spark high`)
- [ ] Reviewer (code review) model: `_______________` (e.g. `claude-sonnet-4-6`)
- [ ] If `architecture` or `standards`: cross-review artifact at `raw/cross-review/YYYY-MM-DD-*.md` with dual signatures (Architect-Claude + Architect-Codex, different model families, both signed)
- [ ] No PII in diff, OR if present, LAM-routed with `raw/lam-audit/*.manifest.json` attached
- [ ] No architecture/standards work performed on Haiku tier
- [ ] Any model fallbacks logged under `raw/model-fallbacks/YYYY-MM-DD.md`

## Test plan
- [ ] ...
- [ ] ...

## Cross-review artifact (architecture / standards PRs only)
<!-- Paste path: raw/cross-review/YYYY-MM-DD-<slug>.md -->

## Fallback log entries (if any)
<!-- Paste path(s): raw/model-fallbacks/YYYY-MM-DD.md -->

🤖 Generated with [Claude Code](https://claude.com/claude-code)
