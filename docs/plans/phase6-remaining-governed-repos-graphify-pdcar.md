# Phase 6 — Remaining Governed Repos Graphify PDCA/R

## Plan
- apply the existing HealthcarePlatform/ASC governance-hosted graphify pattern to `local-ai-machine` and `knocktracker`
- keep product-repo changes minimal: pointer in `CLAUDE.md`, reminder hook in `.claude/settings.json`, and local `graphify-out/` ignored
- only close the phase if the generated governance graphs remain operator-useful

## Do
- update both repos with the minimal pointer/hook pattern
- build `graphify-out/` and `wiki/` outputs for both repos in governance
- update governance status/index/docs to reflect the expanded graph coverage

## Check
- `local-ai-machine`: 3082 nodes, 5098 edges, 416 communities, 426 wiki articles
- `knocktracker`: 456 nodes, 660 edges, 38 communities, 48 wiki articles
- both repos now surface governance-hosted graph hints before raw search

## Adjust
- the first build attempt failed under the default local `python3` because the `graphify` module is installed under Python 3.11; the actual builds were rerun with the known-good Python 3.11 binary instead of treating that already-documented runtime drift as a new blocker
- no new follow-up issue is required because both generated graphs remain useful enough at the governance-hosted report/wiki layer

## Review
- issue `#47` is complete when the last two governed repos are graphified in governance and product repos remain pointer-only
