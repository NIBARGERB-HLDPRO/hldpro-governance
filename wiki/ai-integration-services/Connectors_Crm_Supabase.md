# Connectors Crm Supabase

> 106 nodes · cohesion 0.03

## Key Concepts

- **getSupabaseServiceClient()** (67 connections) — `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- **index.ts** (27 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **emitAuditLog()** (26 connections) — `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- **NullCRMConnector** (21 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/null.ts`
- **index.ts** (17 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- **index.ts** (15 connections) — `ai-integration-services/backend/supabase/functions/assistant-chat/index.ts`
- **handleDemoCheckoutSession()** (12 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/demo-conversion.ts`
- **index.ts** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/index.ts`
- **executeTool()** (12 connections) — `ai-integration-services/backend/supabase/functions/assistant-chat/index.ts`
- **demo-conversion.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/demo-conversion.ts`
- **plaid-client.ts** (9 connections) — `ai-integration-services/backend/supabase/functions/_shared/plaid-client.ts`
- **getAccessToken()** (8 connections) — `ai-integration-services/backend/supabase/functions/email-search/index.ts`
- **handleTransactionSync()** (8 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- **vapiHandler()** (8 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **plaidFetch()** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/plaid-client.ts`
- **interface.ts** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/interface.ts`
- **llm-router.ts** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- **ghl.ts** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/ghl.ts`
- **demo-reference.ts** (6 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/demo-reference.ts`
- **emitCallAnalytics()** (6 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **getAccountsByItemId()** (6 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- **processWebhook()** (6 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **.id()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/null.ts`
- **twenty.ts** (5 connections) — `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/twenty.ts`
- **getPlaidJWK()** (5 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- *... and 81 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/ghl.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/interface.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/local.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/null.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/crm/twenty.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/index.ts`
- `ai-integration-services/backend/supabase/functions/_shared/corpus.ts`
- `ai-integration-services/backend/supabase/functions/_shared/esign.ts`
- `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- `ai-integration-services/backend/supabase/functions/_shared/memory-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/plaid-client.ts`
- `ai-integration-services/backend/supabase/functions/_shared/preference-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/voice-config.ts`
- `ai-integration-services/backend/supabase/functions/assistant-chat/index.ts`
- `ai-integration-services/backend/supabase/functions/email-search/index.ts`
- `ai-integration-services/backend/supabase/functions/email-triage/index.ts`
- `ai-integration-services/backend/supabase/functions/finance-api/index.ts`
- `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`

## Audit Trail

- EXTRACTED: 331 (64%)
- INFERRED: 188 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*