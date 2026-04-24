# Operator client decommission Supabase

> 130 nodes · cohesion 0.03

## Key Concepts

- **getSupabaseServiceClient()** (69 connections) — `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- **emitAuditLog()** (28 connections) — `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- **jsonResponse()** (25 connections) — `ai-integration-services/backend/supabase/functions/som-hitl-relay-bridge/index.ts`
- **resolveClientId()** (23 connections) — `ai-integration-services/backend/supabase/functions/setup-compliance-sync/index.ts`
- **index.ts** (20 connections) — `ai-integration-services/backend/supabase/functions/operator-client-decommission/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/quickbooks-oauth/index.ts`
- **handleCallback()** (14 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **index.ts** (14 connections) — `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- **index.ts** (14 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/debug-feedback/index.ts`
- **readSecret()** (14 connections) — `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- **handleDemoCheckoutSession()** (13 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/demo-conversion.ts`
- **createFeedback()** (13 connections) — `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- **handleDisconnect()** (12 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **JobberConnector** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/service/jobber.ts`
- **index.ts** (12 connections) — `ai-integration-services/backend/supabase/functions/service-offering-suggest/index.ts`
- **index.ts** (12 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/service-offering-suggest/index.ts`
- **getCorsHeaders()** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/cors.ts`
- **index.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/owner-briefing-line/index.ts`
- **demo-conversion.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/demo-conversion.ts`
- **index.ts** (11 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/owner-briefing-line/index.ts`
- **demo-conversion.ts** (11 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/demo-conversion.ts`
- **handleSync()** (10 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **vapiHandler()** (10 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **refreshAccessToken()** (9 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- *... and 105 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/service/jobber.ts`
- `ai-integration-services/backend/supabase/functions/_shared/cors.ts`
- `ai-integration-services/backend/supabase/functions/_shared/error-handler.ts`
- `ai-integration-services/backend/supabase/functions/_shared/esign.ts`
- `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- `ai-integration-services/backend/supabase/functions/_shared/memory-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/preference-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/rate-limiter.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- `ai-integration-services/backend/supabase/functions/assistant-chat/index.ts`
- `ai-integration-services/backend/supabase/functions/consent-confirm/index.ts`
- `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- `ai-integration-services/backend/supabase/functions/demo-upgrade-link/index.ts`
- `ai-integration-services/backend/supabase/functions/email-triage/index.ts`
- `ai-integration-services/backend/supabase/functions/finance-api/index.ts`
- `ai-integration-services/backend/supabase/functions/minute-threshold-checker/index.ts`
- `ai-integration-services/backend/supabase/functions/operator-client-decommission/helpers.test.ts`
- `ai-integration-services/backend/supabase/functions/operator-client-decommission/helpers.ts`

## Audit Trail

- EXTRACTED: 575 (70%)
- INFERRED: 247 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*