# Operator client decommission Supabase

> 153 nodes · cohesion 0.03

## Key Concepts

- **getSupabaseServiceClient()** (68 connections) — `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- **emitAuditLog()** (28 connections) — `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- **index.ts** (28 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **index.ts** (27 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/webhook-receiver/index.ts`
- **jsonResponse()** (25 connections) — `ai-integration-services/backend/supabase/functions/som-hitl-relay-bridge/index.ts`
- **resolveClientId()** (21 connections) — `ai-integration-services/backend/supabase/functions/setup-compliance-sync/index.ts`
- **index.ts** (20 connections) — `ai-integration-services/backend/supabase/functions/operator-client-decommission/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/plaid-webhook/index.ts`
- **index.ts** (17 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/quickbooks-oauth/index.ts`
- **getAccessToken()** (14 connections) — `ai-integration-services/backend/supabase/functions/email-search/index.ts`
- **handleCallback()** (14 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **index.ts** (14 connections) — `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- **index.ts** (14 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/debug-feedback/index.ts`
- **readSecret()** (14 connections) — `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- **createFeedback()** (13 connections) — `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- **handleDisconnect()** (12 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **index.ts** (12 connections) — `ai-integration-services/backend/supabase/functions/service-offering-suggest/index.ts`
- **index.ts** (12 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/service-offering-suggest/index.ts`
- **handleSync()** (10 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **vapiHandler()** (10 connections) — `ai-integration-services/backend/supabase/functions/webhook-receiver/index.ts`
- **handleTransactionSync()** (9 connections) — `ai-integration-services/backend/supabase/functions/plaid-webhook/index.ts`
- **refreshAccessToken()** (9 connections) — `ai-integration-services/backend/supabase/functions/quickbooks-oauth/index.ts`
- **plaidFetch()** (9 connections) — `ai-integration-services/backend/supabase/functions/_shared/plaid-client.ts`
- *... and 128 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/audit.ts`
- `ai-integration-services/backend/supabase/functions/_shared/auth.ts`
- `ai-integration-services/backend/supabase/functions/_shared/connectors/index.ts`
- `ai-integration-services/backend/supabase/functions/_shared/crypto.ts`
- `ai-integration-services/backend/supabase/functions/_shared/error-handler.ts`
- `ai-integration-services/backend/supabase/functions/_shared/llm-router.ts`
- `ai-integration-services/backend/supabase/functions/_shared/memory-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/oauth-state.ts`
- `ai-integration-services/backend/supabase/functions/_shared/plaid-client.ts`
- `ai-integration-services/backend/supabase/functions/_shared/preference-injector.ts`
- `ai-integration-services/backend/supabase/functions/_shared/rate-limiter.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vapi-usage.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vapi-usage.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vault.ts`
- `ai-integration-services/backend/supabase/functions/assistant-chat/index.ts`
- `ai-integration-services/backend/supabase/functions/corpus-exporter/index.ts`
- `ai-integration-services/backend/supabase/functions/debug-feedback/index.ts`
- `ai-integration-services/backend/supabase/functions/email-search/index.ts`
- `ai-integration-services/backend/supabase/functions/email-triage/index.ts`
- `ai-integration-services/backend/supabase/functions/finance-api/index.ts`

## Audit Trail

- EXTRACTED: 755 (75%)
- INFERRED: 258 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*