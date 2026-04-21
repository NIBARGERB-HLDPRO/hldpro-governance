# Cross-Review: Cloudflare Pages Deploy Gate — Round 1

Date: 2026-04-21
Epic: #467 (Cloudflare Pages direct-upload deploy gate)
Planning issue: #468
Reviewer: gpt-5.4 @ model_reasoning_effort=high (Tier 1B Plan Reviewer)
Planner: claude-opus-4-6 (Tier 1A)
Artifacts reviewed:
- docs/plans/2026-04-21-issue-467-pages-deploy-gate-pdcar.md
- docs/plans/issue-467-pages-deploy-gate-structured-agent-cycle-plan.json

## VERDICT

REJECTED

## SUMMARY

The governance-owned gate plus consumer-config pattern is directionally sound, and the child issue split is mostly clean. The plan is not yet implementation-ready because it underspecifies the actual first-consumer ordering problem: `persona-respond` is a Supabase Edge Function, not a Cloudflare Pages Function, and must be deployed before the Pages bundle that calls it. It also lacks hard ACs for build freshness, Wrangler/CI preflight, token scope, Cloudflare limits, domain propagation behavior, and rollback evidence.

## REQUIRED_CHANGES

1. Explicitly model seek's deploy order: `scripts/deploy.sh persona-respond` or equivalent Supabase Edge Function deploy must complete before `wrangler pages deploy` for the web bundle.

2. Add gate ACs for build execution and artifact freshness. Direct Upload requires prebuilt assets; the gate must fail if the build command fails or if the deploy output is stale/missing.

3. Add Wrangler/CI preflight ACs: Node/Wrangler availability, version capture, noninteractive CI behavior, required env names, and deterministic failure messages.

4. Specify minimum Cloudflare token scope and no-secret handling. Cloudflare's CI docs call for `Cloudflare Pages: Edit` plus account ID usage; plan must require account IDs, token values, signed URLs, and `Authorization` headers to be redacted from logs and evidence.

5. Extend material deviation rules for Cloudflare failure modes: Pages file/file-size/build quotas, upload failure after successful function deploy, custom domain inactive/CNAME mismatch, and production rollback to previous successful deployment.

6. Tighten verifier ACs for domain parity: retry/backoff window, cache-busting or no-cache request strategy, redirect handling, expected headers/status codes, and a stable commit/deployment-id endpoint so CDN cache or propagation delay does not create false negatives.

7. Clarify Sprint 5 inventory source of truth. "Equivalent marker" is too vague; define whether inventory uses Pages API/project metadata, repo config, registry fields, or all three.

## FOLLOW_UP_NOTES

- Cloudflare primary docs checked: Direct Upload requires prebuilt assets and Wrangler upload; CI examples use `CLOUDFLARE_ACCOUNT_ID` plus `CLOUDFLARE_API_TOKEN`; Wrangler supports `pages deploy --commit-hash`; Pages limits include file/file-size/custom-domain/project limits; Pages rollbacks can revert production to prior successful deployments.
- Sources: https://developers.cloudflare.com/pages/get-started/direct-upload/ | https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/ | https://developers.cloudflare.com/workers/wrangler/commands/pages/ | https://developers.cloudflare.com/pages/platform/limits/ | https://developers.cloudflare.com/pages/configuration/rollbacks/
