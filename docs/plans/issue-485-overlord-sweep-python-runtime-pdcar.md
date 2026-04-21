# Issue 485 PDCAR: Overlord Sweep Python Runtime

Issue: NIBARGERB-HLDPRO/hldpro-governance#485  
Date: 2026-04-21

## Plan

Manual sweep run `24739125036` proved the self-learning report step now runs, then failed later in `Update knowledge graph` because the workflow called `python3.11` and the GitHub-hosted runner did not expose that binary.

Expected implementation:

- Replace the hardcoded `python3.11` calls in `.github/workflows/overlord-sweep.yml` with `python3`.
- Keep graphify installation and graph building in the same step.
- Validate the workflow change through local governance gates.
- Re-run the manual sweep after merge.

## Do

Patch the workflow runtime command only, then run workflow/local-governance checks and publish a focused PR.

## Check

Acceptance criteria:

- The workflow no longer depends on a missing `python3.11` binary.
- Local CI and workflow coverage checks pass.
- The next manual Overlord Sweep reaches graph update with an available Python runtime.

## Act

If the sweep fails later, record the concrete downstream blocker in an issue and continue the loop without reclassifying the already-proven self-learning report step as failed.
