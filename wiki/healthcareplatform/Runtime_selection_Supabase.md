# Runtime selection Supabase

> 27 nodes · cohesion 0.11

## Key Concepts

- **index.ts** (14 connections) — `healthcareplatform/backend/supabase/functions/visits/index.ts`
- **getChecklist()** (10 connections) — `healthcareplatform/backend/supabase/functions/visits/index.ts`
- **visit-pin-gate.ts** (9 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- **createVisit()** (9 connections) — `healthcareplatform/backend/supabase/functions/visits/index.ts`
- **index.ts** (8 connections) — `healthcareplatform/backend/supabase/functions/checklist-generate/index.ts`
- **runtime-selection.ts** (8 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- **computeEffectiveTemplateIds()** (5 connections) — `healthcareplatform/backend/supabase/functions/visits/index.ts`
- **checklist-assembly.ts** (4 connections) — `healthcareplatform/backend/supabase/functions/_shared/checklist-assembly.ts`
- **deterministicChecklistSnapshotHash()** (3 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- **evaluateVisitPinGate()** (3 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- **buildChecklistBindings()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/checklist-assembly.ts`
- **collectStandardIds()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/checklist-assembly.ts`
- **runtime-selection.test.ts** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.test.ts`
- **auditChecklistGenerate()** (2 connections) — `healthcareplatform/backend/supabase/functions/checklist-generate/index.ts`
- **buildPinnedBodyReleaseMap()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- **collectPinnedReleaseIds()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- **selectDeterministicCandidate()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- **selectPublishedReleaseIds()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- **buildDeterministicChecklistSnapshot()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- **normalizeString()** (2 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- **visit-pin-gate.test.ts** (1 connections) — `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.test.ts`
- **isInternalSecretRequest()** (1 connections) — `healthcareplatform/backend/supabase/functions/checklist-generate/index.ts`
- **isServiceRoleRequest()** (1 connections) — `healthcareplatform/backend/supabase/functions/checklist-generate/index.ts`
- **normalizeVisitsRoutePath()** (1 connections) — `healthcareplatform/backend/supabase/functions/visits/index.ts`
- **bodySortKey()** (1 connections) — `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- *... and 2 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `healthcareplatform/backend/supabase/functions/_shared/checklist-assembly.ts`
- `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.test.ts`
- `healthcareplatform/backend/supabase/functions/_shared/runtime-selection.ts`
- `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.test.ts`
- `healthcareplatform/backend/supabase/functions/_shared/visit-pin-gate.ts`
- `healthcareplatform/backend/supabase/functions/checklist-generate/index.ts`
- `healthcareplatform/backend/supabase/functions/visits/index.ts`

## Audit Trail

- EXTRACTED: 75 (75%)
- INFERRED: 25 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*