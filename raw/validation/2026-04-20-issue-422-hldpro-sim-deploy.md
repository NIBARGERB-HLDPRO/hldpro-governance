# Validation Evidence: hldpro-sim v0.1.0 Deployment Readiness

Date: 2026-04-20
Issue: #422
Branch: issue-422-hldpro-sim-deploy-20260420

## Sprint 1: Version tag + distribution contract

### Tag verification
```
git rev-list -n 1 hldpro-sim-v0.1.0
fed5ead670cf6834e5c73bffcaf64e41cc483fce
```
Expected: `fed5ead670cf6834e5c73bffcaf64e41cc483fce` ✓

Tag pushed to remote: confirmed via `git push origin hldpro-sim-v0.1.0` → `[new tag]`

### Consumer pull state contract
File: `docs/hldpro-sim-consumer-pull-state.json`
- Package: hldpro-sim 0.1.0
- 5 managed personas declared
- consumer_record_path: `.hldpro/hldpro-sim.json`
- deployer_script: `scripts/deployer/deploy-hldpro-sim.sh`

## Sprint 2: Deployer dry-run

Command:
```bash
bash scripts/deployer/deploy-hldpro-sim.sh /tmp/sim-consumer-test --dry-run
```

Output (abbreviated):
```
[deploy-hldpro-sim] Installing hldpro-sim 0.1.0 into /tmp/sim-consumer-test
[DRY-RUN] would: pip install -e .../packages/hldpro-sim ...
[DRY-RUN] would: mkdir -p /tmp/sim-consumer-test/sim-personas/shared
[DRY-RUN] would: cp .../personas/*.json → /tmp/sim-consumer-test/sim-personas/shared/
[DRY-RUN] would: chmod 444 /tmp/sim-consumer-test/sim-personas/shared/*.json
[deploy-hldpro-sim] dry-run consumer record written to /tmp/sim-consumer-test/.hldpro/hldpro-sim.json
[deploy-hldpro-sim] Done. hldpro-sim 0.1.0 deployed to /tmp/sim-consumer-test
```

### Consumer record (dry-run output)
```json
{
    "package": "hldpro-sim",
    "version": "0.1.0",
    "tag": "hldpro-sim-v0.1.0",
    "pinned_sha": "fed5ead670cf6834e5c73bffcaf64e41cc483fce",
    "install_method": "pip-editable",
    "installed_at": "2026-04-20T19:58:33Z",
    "personas_path": "sim-personas/shared/",
    "governance_source": "hldpro-governance"
}
```

## Result: PASS

All PDCAR Check criteria satisfied:
- Tag points to correct commit ✓
- Deployer dry-run completes without error ✓
- Consumer record written with correct fields ✓
- Deployer degrades gracefully (fallback to directory-copy documented) ✓
