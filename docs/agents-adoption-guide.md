# Agents Adoption Guide

This guide covers operational procedures for consumer repos that integrate governance-managed packages and agents.

---

## hldpro-sim Version Management

### Check installed version
```bash
cat .hldpro/hldpro-sim.json
```

### Check if current
Compare `pinned_sha` in your consumer record against `docs/hldpro-sim-consumer-pull-state.json` in the governance repo:
```bash
python3 -c "
import json
from pathlib import Path
consumer = json.loads(Path('.hldpro/hldpro-sim.json').read_text())
governance = json.loads(Path('<governance-root>/docs/hldpro-sim-consumer-pull-state.json').read_text())
if consumer['pinned_sha'] == governance['pinned_sha']:
    print('CURRENT:', consumer['pinned_sha'][:8])
else:
    print('STALE — consumer:', consumer['pinned_sha'][:8], '/ governance:', governance['pinned_sha'][:8])
"
```

### Re-deploy
```bash
bash <governance-root>/scripts/deployer/deploy-hldpro-sim.sh <consumer-repo-path>
```

The deployer overwrites the package install (pip-editable or directory-copy), updates `sim-personas/shared/` with latest managed personas, and writes a new `.hldpro/hldpro-sim.json` consumer record with the current pinned SHA. Commit `.hldpro/hldpro-sim.json` after re-deploy.

### Automated drift detection
A standalone drift detector (`scripts/overlord/check_hldpro_sim_version.py`) is tracked in a follow-up issue and will be integrated into the overlord-sweep report when complete.
