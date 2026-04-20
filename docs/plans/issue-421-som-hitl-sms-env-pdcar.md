# PDCAR: Issue #421 SoM HITL SMS Sender Env Propagation

Date: 2026-04-20
Branch: `issue-421-som-hitl-sms-env-20260420`
Issue: [#421](https://github.com/NIBARGERB-HLDPRO/hldpro-governance/issues/421)
Parent: [local-ai-machine #497](https://github.com/NIBARGERB-HLDPRO/local-ai-machine/issues/497)

## Plan

Extend the governance `.env.shared` SSOT/bootstrap contract so local-ai-machine receives a dedicated SoM HITL SMS sender key for approval/reply routing. Keep AIS/Alex and customer-demo sender paths out of the production approval route.

Acceptance criteria:

- `scripts/bootstrap-repo-env.sh` emits `SOM_TWILIO_FROM_NUMBER` plus generic Twilio sender aliases for the local-ai-machine target.
- `docs/ENV_REGISTRY.md` identifies `SOM_TWILIO_FROM_NUMBER` as the dedicated production SoM HITL sender.
- `docs/EXTERNAL_SERVICES_RUNBOOK.md` documents vault storage, bootstrap, sender separation, redacted evidence, and the explicit-approval rule for new Twilio provisioning.
- Focused bootstrap contract validation proves required key names are present and dry-run output remains redacted.
- Final AC: Local CI and GitHub PR checks pass before merge.

## Do

1. Add `SOM_TWILIO_FROM_NUMBER`, `TWILIO_FROM_NUMBER`, and `TWILIO_SMS_FROM` to the local-ai-machine bootstrap output.
2. Extend the bootstrap contract test with placeholder sender values and redaction assertions.
3. Document dedicated SoM HITL sender ownership in the environment registry.
4. Document the SoM HITL SMS route and evidence rules in the external services runbook.

## Check

- Static contract must confirm the bootstrap script and registry include all required sender keys.
- Synthetic and sibling-worktree dry runs must include redacted sender keys without leaking placeholder phone values.
- Shell syntax, structured plan, execution scope, diff whitespace, Local CI, and PR checks must pass.

## Adjust

If no dedicated sender has been provisioned yet, keep `SOM_TWILIO_FROM_NUMBER` empty in generated env artifacts and leave the downstream PR draft until either physical SMS receipt or Twilio delivery-status evidence proves the route.

## Review

Review must confirm this slice does not buy a Twilio number, mutate Twilio dashboards, commit `.env.shared`, reveal raw phone numbers, or collapse the SoM approval route back onto the AIS/Alex/customer-demo sender.
