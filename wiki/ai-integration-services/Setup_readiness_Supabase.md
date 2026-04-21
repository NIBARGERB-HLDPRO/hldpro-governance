# Setup readiness Supabase

> 120 nodes · cohesion 0.03

## Key Concepts

- **index.ts** (38 connections) — `ai-integration-services/backend/supabase/functions/portal-provision/index.ts`
- **setup-connection-tasks.ts** (22 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-connection-tasks.ts`
- **portal-purchase.ts** (20 connections) — `ai-integration-services/backend/supabase/functions/_shared/portal-purchase.ts`
- **setup-compliance-gates.ts** (20 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-compliance-gates.ts`
- **setup-readiness.ts** (19 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-readiness.ts`
- **finalizePortalPurchase()** (17 connections) — `ai-integration-services/backend/supabase/functions/_shared/portal-purchase.ts`
- **index.ts** (14 connections) — `ai-integration-services/backend/supabase/functions/reseller-manager/index.ts`
- **syncSetupConnectionTasksForClient()** (13 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-connection-tasks.ts`
- **CalcomClient** (12 connections) — `ai-integration-services/backend/supabase/functions/_shared/calcom-client.ts`
- **calcom-finalization.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/calcom-finalization.ts`
- **optional-product-setup.ts** (11 connections) — `ai-integration-services/backend/supabase/functions/_shared/optional-product-setup.ts`
- **.calFetch()** (10 connections) — `ai-integration-services/backend/supabase/functions/_shared/calcom-client.ts`
- **provisioning-service-matrix.ts** (9 connections) — `ai-integration-services/backend/supabase/functions/_shared/provisioning-service-matrix.ts`
- **buildCalcomFinalizeDefaults()** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/calcom-finalization.ts`
- **provisioning-plan.ts** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/provisioning-plan.ts`
- **provisioning-probes.ts** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/provisioning-probes.ts`
- **setup-plan.ts** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-plan.ts`
- **runStep()** (8 connections) — `ai-integration-services/backend/supabase/functions/portal-provision/index.ts`
- **syncSetupComplianceGatesForClient()** (8 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-compliance-gates.ts`
- **calcom-client.ts** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/calcom-client.ts`
- **nonEmpty()** (7 connections) — `ai-integration-services/backend/supabase/functions/_shared/portal-purchase.ts`
- **syncClientSetupReadiness()** (6 connections) — `ai-integration-services/backend/supabase/functions/portal-provision/index.ts`
- **syncOneClient()** (6 connections) — `ai-integration-services/backend/supabase/functions/sync-compliance-gates/index.ts`
- **ensureReferralTracking()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/portal-purchase.ts`
- **derivePlaidGate()** (6 connections) — `ai-integration-services/backend/supabase/functions/_shared/setup-compliance-gates.ts`
- *... and 95 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `ai-integration-services/backend/supabase/functions/_shared/calcom-client.ts`
- `ai-integration-services/backend/supabase/functions/_shared/calcom-finalization.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/calcom-finalization.ts`
- `ai-integration-services/backend/supabase/functions/_shared/forwarding-instructions.ts`
- `ai-integration-services/backend/supabase/functions/_shared/optional-product-setup.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/optional-product-setup.ts`
- `ai-integration-services/backend/supabase/functions/_shared/portal-purchase.ts`
- `ai-integration-services/backend/supabase/functions/_shared/provisioning-plan.ts`
- `ai-integration-services/backend/supabase/functions/_shared/provisioning-probes.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/provisioning-probes.ts`
- `ai-integration-services/backend/supabase/functions/_shared/provisioning-service-matrix.ts`
- `ai-integration-services/backend/supabase/functions/_shared/setup-compliance-gates.ts`
- `ai-integration-services/backend/supabase/functions/_shared/setup-connection-tasks.ts`
- `ai-integration-services/backend/supabase/functions/_shared/setup-plan.ts`
- `ai-integration-services/backend/supabase/functions/_shared/setup-readiness.test.ts`
- `ai-integration-services/backend/supabase/functions/_shared/setup-readiness.ts`
- `ai-integration-services/backend/supabase/functions/_shared/vapi-brain-tool.ts`
- `ai-integration-services/backend/supabase/functions/portal-provision/index.ts`
- `ai-integration-services/backend/supabase/functions/reseller-auth/index.ts`
- `ai-integration-services/backend/supabase/functions/reseller-manager/index.ts`

## Audit Trail

- EXTRACTED: 439 (89%)
- INFERRED: 57 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*