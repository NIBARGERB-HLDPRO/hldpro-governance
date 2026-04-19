# Issue #213 - PentAGI Sweep Source PDCA/R

Branch: `issue-213-pentagi-sweep-source`
Issue: [#213](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/213)

## Plan

Move PentAGI freshness and trigger status out of ad hoc sweep prose into a deterministic helper that reads the audited checkout root, evaluates PentAGI-tier repos from the governed repo registry, and emits Markdown plus JSON from the same source data.

## Do

- Add `scripts/overlord/pentagi_sweep.py`.
- Add regression tests for missing/stale reports, missing `PENTAGI_API_TOKEN`, missing runner, fresh reports, and audited-root resolution.
- Wire `.github/workflows/overlord-sweep.yml` to include a PentAGI Trigger Status section and persist `metrics/pentagi/latest.json`.
- Update `agents/overlord-sweep.md` so local sweeps use the helper and do not count untracked canonical checkout reports for detached audit freshness.

## Check

Final acceptance requires:

- `python3 -m pytest scripts/overlord/test_pentagi_sweep.py`
- Relevant existing overlord tests
- structured plan validation
- execution-scope validation
- backlog/GitHub sync validation
- workflow/local contract tests
- `python3 -m py_compile scripts/overlord/pentagi_sweep.py`
- `git diff --check`
- Local CI Gate against the changed-file list
- focused review acceptance
- GitHub PR checks

## Act

If validation and review pass, publish #213 as a focused PR and merge only after CI is green. Any live downstream PentAGI execution remains operator-controlled through `PENTAGI_API_TOKEN` plus a repo-local `scripts/pentagi-run.sh` runner.
