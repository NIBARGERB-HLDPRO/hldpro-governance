# Addon lifecycle Supabase

> 160 nodes · cohesion 0.02

## Key Concepts

- **text()** (103 connections) — `ai-integration-services/scripts/seed-esign-templates.ts`
- **addon-ui-lifecycle.spec.ts** (23 connections) — `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`
- **addon-ui-lifecycle.spec.ts** (23 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/e2e/addon-ui-lifecycle.spec.ts`
- **N8nClient** (18 connections) — `ai-integration-services/backend/supabase/functions/_shared/n8n-client.ts`
- **TwilioClient** (17 connections) — `ai-integration-services/backend/supabase/functions/_shared/twilio-client.ts`
- **operator-context-governance.ts** (16 connections) — `ai-integration-services/backend/supabase/functions/_shared/operator-context-governance.ts`
- **operator-context-governance.ts** (16 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/_shared/operator-context-governance.ts`
- **GoogleCalendarConnector** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/service/google-calendar.ts`
- **.n8nFetch()** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/n8n-client.ts`
- **ServiceTitanConnector** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/service/servicetitan.ts`
- **HousecallProConnector** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/service/housecall.ts`
- **index.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/logs-watcher/index.ts`
- **index.ts** (11 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/logs-watcher/index.ts`
- **writeOperatorContextToGovernance()** (10 connections) — `ai-integration-services/backend/supabase/functions/_shared/operator-context-governance.ts`
- **readEnvSecret()** (10 connections) — `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- **.twilioFetch()** (9 connections) — `ai-integration-services/backend/supabase/functions/_shared/twilio-client.ts`
- **index.ts** (8 connections) — `ai-integration-services/backend/supabase/functions/solar-monitoring-alert/index.ts`
- **handlePostComment()** (7 connections) — `ai-integration-services/apps/marketing/src/portal/pages/gc/GCOwnerPortal.tsx`
- **sendPortalAccessEmail()** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/purchase-access-email.ts`
- **llm-router.ts** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- **llm-router.ts** (7 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/_shared/llm-router.ts`
- **cancelAddonFromUi()** (6 connections) — `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`
- **expectAddonCard()** (6 connections) — `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`
- **expectStripeRedirect()** (6 connections) — `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`
- **fetchJson()** (6 connections) — `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`
- *... and 135 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/apps/marketing/src/portal/pages/gc/GCOwnerPortal.tsx`
- `ai-integration-services/apps/portal/src/pages/gc/GCOwnerPortal.tsx`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/service/google-calendar.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/service/housecall.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/service/servicetitan.ts`
- `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- `ai-integration-services/backend/supabase/functions/_shared/n8n-client.ts`
- `ai-integration-services/backend/supabase/functions/_shared/operator-context-governance.ts`
- `ai-integration-services/backend/supabase/functions/_shared/purchase-access-email.ts`
- `ai-integration-services/backend/supabase/functions/_shared/twilio-client.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- `ai-integration-services/backend/supabase/functions/brain-pdf-parser/index.ts`
- `ai-integration-services/backend/supabase/functions/email-search/index.ts`
- `ai-integration-services/backend/supabase/functions/logs-watcher/index.ts`
- `ai-integration-services/backend/supabase/functions/minute-threshold-checker/index.ts`
- `ai-integration-services/backend/supabase/functions/overage-billing/index.ts`
- `ai-integration-services/backend/supabase/functions/send-pricing-invite/index.ts`
- `ai-integration-services/backend/supabase/functions/solar-monitoring-alert/index.ts`
- `ai-integration-services/backend/supabase/functions/solar-referral-trigger/index.ts`
- `ai-integration-services/e2e/addon-ui-lifecycle.spec.ts`

## Audit Trail

- EXTRACTED: 586 (73%)
- INFERRED: 214 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*