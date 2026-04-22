# Stripe webhook Lifecycle Supabase

> 11 nodes · cohesion 0.29

## Key Concepts

- **lifecycle.ts** (6 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- **lifecycle.ts** (6 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- **updateClientBillingLifecycle()** (5 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- **lifecycle-state.ts** (4 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- **lifecycle-state.ts** (4 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- **auditStripeLifecycleOrphan()** (3 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- **mergeBillingLifecycle()** (3 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- **readinessPatchForPaymentState()** (3 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- **findClientBySubscriptionOrCustomer()** (2 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- **lifecycle.test.ts** (1 connections) — `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.test.ts`
- **lifecycle.test.ts** (1 connections) — `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle.test.ts`

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.test.ts`
- `ai-integration-services/backend/supabase/functions/stripe-webhook/lifecycle.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle-state.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle.test.ts`
- `ai-integration-services/var/worktrees/issue-1211-sweep-claude-supervisor/backend/supabase/functions/stripe-webhook/lifecycle.ts`

## Audit Trail

- EXTRACTED: 32 (84%)
- INFERRED: 6 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*