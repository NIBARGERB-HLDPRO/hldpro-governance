# Governed Repo Registry Exemptions

Date: 2026-04-17
Issue: #225

`docs/governed_repos.json` is the executable source of truth for governed repo
metadata. Some hardcoded repo mentions remain intentionally outside the first
registry migration because they are not executable discovery lists or because
GitHub Actions requires static checkout declarations.

## Approved Temporary Exemptions

| Surface | Reason | Exit Criteria |
|---|---|---|
| `.github/workflows/overlord-sweep.yml` checkout steps | `actions/checkout` repositories are static workflow steps. Runtime sweep variables now derive from the registry, but checkout steps remain explicit until a reviewed matrix or composite checkout helper exists. | Replace static checkout steps with a registry-generated matrix/helper in a later sweep hardening issue. |
| `.github/workflows/raw-feed-sync.yml` loop | Raw-feed sync is a metadata-only issue mirror and was outside #225 file ownership. | Migrate to registry `raw_feed_sync` in a follow-up or #226 if it becomes part of a planning/scope gate. |
| `agents/*.md` and `docs/*.md` prose examples | Human instructions, historical records, and examples mention repo names intentionally. They are not executable discovery sources. | Update opportunistically when the relevant agent/doc is otherwise touched. |
| `docs/graphify_targets.json` | Kept as the graphify manifest contract, but `scripts/overlord/validate_governed_repos.py` reconciles it against the registry. | Replace or generate the manifest from registry after the graphify contract is reviewed for that change. |

No production Python script should carry an independent governed repo list after
#225. Use `scripts/overlord/governed_repos.py` or reconcile against
`docs/governed_repos.json`.
