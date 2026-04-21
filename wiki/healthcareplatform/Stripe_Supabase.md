# Stripe Supabase

> 64 nodes · cohesion 0.07

## Key Concepts

- **stripe.ts** (28 connections) — `healthcareplatform/backend/supabase/functions/_shared/stripe.ts`
- **index.ts** (19 connections) — `healthcareplatform/backend/supabase/functions/billing-modules/index.ts`
- **index.ts** (14 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **asString()** (14 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **handleSubscriptionEvent()** (12 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **handleCheckoutCompleted()** (10 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **index.ts** (9 connections) — `healthcareplatform/backend/supabase/functions/public-signup/index.ts`
- **asRecord()** (9 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **syncModuleProfilesFromSubscription()** (8 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **optionalEnv()** (8 connections) — `healthcareplatform/backend/supabase/functions/_shared/stripe.ts`
- **parseRoutePath()** (7 connections) — `healthcareplatform/backend/supabase/functions/patient-comms/index.ts`
- **validatePayload()** (7 connections) — `healthcareplatform/backend/supabase/functions/public-signup/index.ts`
- **resolveSubscriptionTierFromObject()** (6 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **index.ts** (5 connections) — `healthcareplatform/backend/supabase/functions/billing-portal/index.ts`
- **index.ts** (5 connections) — `healthcareplatform/backend/supabase/functions/checkout-session/index.ts`
- **asTrimmedString()** (5 connections) — `healthcareplatform/backend/supabase/functions/public-signup/index.ts`
- **listModuleBillingState()** (5 connections) — `healthcareplatform/backend/supabase/functions/billing-modules/index.ts`
- **resolveBillingIntervalFromObject()** (5 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **resolveTenantIdForStripeObject()** (5 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **syncTenantTierToAuthUsers()** (5 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **mapPriceIdToModule()** (5 connections) — `healthcareplatform/backend/supabase/functions/_shared/stripe.ts`
- **asNumber()** (4 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- **getModuleProfiles()** (4 connections) — `healthcareplatform/backend/supabase/functions/billing-modules/index.ts`
- **getTenantFacilityCount()** (4 connections) — `healthcareplatform/backend/supabase/functions/facilities/index.ts`
- **upsertBillingProfile()** (4 connections) — `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`
- *... and 39 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `healthcareplatform/backend/supabase/functions/_shared/stripe.test.ts`
- `healthcareplatform/backend/supabase/functions/_shared/stripe.ts`
- `healthcareplatform/backend/supabase/functions/billing-modules/index.ts`
- `healthcareplatform/backend/supabase/functions/billing-portal/index.ts`
- `healthcareplatform/backend/supabase/functions/checkout-session/index.ts`
- `healthcareplatform/backend/supabase/functions/facilities/index.ts`
- `healthcareplatform/backend/supabase/functions/patient-comms/index.ts`
- `healthcareplatform/backend/supabase/functions/public-signup/index.ts`
- `healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts`

## Audit Trail

- EXTRACTED: 260 (86%)
- INFERRED: 42 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*