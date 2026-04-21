# PDCAR: Secret Provisioning UX and No-Secret Evidence Contract

Date: 2026-04-21
Planning branch: `issue-508-secret-provisioning-ux-20260421`
Repo: `hldpro-governance`
Status: PLANNING - issue #508
GitHub epic: [#507](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/507)
Planning issue: [#508](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/508)
Related epic: [#467](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/467)

## Problem

Deploy and preflight tooling can fail for absent local credentials and then produce operator guidance that normalizes pasting secrets into shells, chats, logs, or issue text. Even placeholder inline export examples teach the wrong muscle memory: credentials should be provisioned through approved stores, not copied through ad hoc terminal commands.

Governance already has strong pieces of the desired model:

- `docs/ENV_REGISTRY.md` treats `hldpro-governance/.env.shared` as the gitignored SSOT for local provisioning.
- `scripts/bootstrap-repo-env.sh` parses `.env.shared` as data and writes ignored repo-local generated env files.
- `scripts/test_bootstrap_repo_env_contract.py` enforces that bootstrap behavior.
- The Pages deploy gate epic (#467) gives this work a live consumer path for Cloudflare Pages deployment UX.

The missing piece is a cross-repo contract: missing-secret diagnostics must list variable names only, never values or inline secret export commands, and must point to approved provisioning surfaces.

## Do

1. Complete this planning package under issue #508:
   - PDCAR: `docs/plans/2026-04-21-issue-507-secret-provisioning-ux-pdcar.md`
   - Structured plan: `docs/plans/issue-507-secret-provisioning-ux-structured-agent-cycle-plan.json`
   - Planning execution scope: `raw/execution-scopes/2026-04-21-issue-508-secret-provisioning-ux-planning.json`
   - Issue graph evidence: `raw/validation/2026-04-21-issue-508-secret-provisioning-ux-issue-graph.md`
2. Implement the epic in issue-backed child lanes:
   - #509 defines the standards contract in `STANDARDS.md` and `docs/ENV_REGISTRY.md`.
   - #510 adds no-secret provisioning evidence validation and CI/local gate coverage.
   - #511 hardens Pages deploy gate missing-secret UX.
   - #512 scrubs governance runbooks that contain inline secret provisioning guidance.
   - #513 inventories downstream governed repos and routes residual gaps.
3. Preserve the no-secret boundary:
   - Do not commit `.env.shared`, generated `.env*`, provider tokens, raw phone numbers, signed URLs, Authorization headers, or screenshots containing credentials.
   - Do not paste secret values into issue bodies, validation artifacts, PR descriptions, logs, or terminal transcripts.
   - Do not write to downstream repos from this governance planning lane.

## Check

Planning validation for issue #508:

```bash
python3 -m json.tool docs/plans/issue-507-secret-provisioning-ux-structured-agent-cycle-plan.json >/dev/null
python3 -m json.tool raw/execution-scopes/2026-04-21-issue-508-secret-provisioning-ux-planning.json >/dev/null
python3 scripts/overlord/validate_structured_agent_cycle_plan.py --root .
python3 scripts/overlord/assert_execution_scope.py \
  --scope raw/execution-scopes/2026-04-21-issue-508-secret-provisioning-ux-planning.json \
  --require-lane-claim
python3 scripts/overlord/check_overlord_backlog_github_alignment.py
```

Schema-level validation for this specific structured plan:

```bash
python3 - <<'PY'
import json
import jsonschema
from pathlib import Path

schema = json.loads(Path("docs/schemas/structured-agent-cycle-plan.schema.json").read_text())
plan = json.loads(Path("docs/plans/issue-507-secret-provisioning-ux-structured-agent-cycle-plan.json").read_text())
jsonschema.validate(plan, schema)
print("VALID structured-agent-cycle plan")
PY
```

## Adjust

Material deviation rules:

1. If implementation discovers tooling that currently prints secret values, stop that lane and open a security-labeled issue before continuing.
2. If a downstream repo needs changes, create and claim a downstream issue/lane before any write.
3. If a required provider-specific secret path is unavailable, document the blocked state with variable names only and no values.
4. If evidence capture would include a credential-bearing screenshot, terminal transcript, signed URL, Authorization header, or raw phone number, replace it with redacted structured evidence before commit.
5. If this epic conflicts with urgent production deployment, the production fix may proceed only under that repo's existing deploy emergency rules, with follow-up governance issue linkage.

## Report

The expected closeout for #508 is planning-only:

- Epic #507 remains open with child issue map #508-#513.
- #508 records PDCAR, structured plan, planning execution scope, backlog mirror, and issue graph evidence.
- Implementation work remains intentionally unstarted until child lanes execute under their own scopes.
