# Ghl sync contacts Supabase

> 43 nodes · cohesion 0.06

## Key Concepts

- **index.ts** (42 connections) — `knocktracker/supabase/functions/integration-webhook/index.ts`
- **GHLClient** (7 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **runSyncJob()** (7 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **.performRequest()** (5 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **.listContacts()** (3 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **.listContactsByUrl()** (3 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **json()** (3 connections) — `knocktracker/supabase/functions/import-osm-territory/index.ts`
- **buildNextPageUrl()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **delay()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **errorJson()** (2 connections) — `knocktracker/supabase/functions/import-osm-territory/index.ts`
- **exponentialBackoff()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **fetchAddressFromNominatim()** (2 connections) — `knocktracker/app/(tabs)/index.tsx`
- **fetchOverpass()** (2 connections) — `knocktracker/supabase/functions/import-osm-territory/index.ts`
- **getLastSuccessfulSync()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **getLocation()** (2 connections) — `knocktracker/app/(tabs)/index.tsx`
- **processContactsPage()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **updateSyncState()** (2 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **CrmSubmenuFloating.tsx** (1 connections) — `knocktracker/src/components/crm/CrmSubmenuFloating.tsx`
- **authenticateRequest()** (1 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **buildAddressLabel()** (1 connections) — `knocktracker/supabase/functions/osm-polygon-homes/index.ts`
- **buildOverpassPoly()** (1 connections) — `knocktracker/supabase/functions/import-osm-territory/index.ts`
- **elementsToRows()** (1 connections) — `knocktracker/supabase/functions/import-osm-territory/index.ts`
- **geocodeForward()** (1 connections) — `knocktracker/supabase/functions/cad-backfill-polygon/index.ts`
- **getActiveJobForUser()** (1 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- **getLastRunForUser()** (1 connections) — `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- *... and 18 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `knocktracker/app/(main)/crm/index.tsx`
- `knocktracker/app/(main)/index.tsx`
- `knocktracker/app/(tabs)/index.tsx`
- `knocktracker/app/index.tsx`
- `knocktracker/src/components/crm/CrmSubmenuFloating.tsx`
- `knocktracker/supabase/functions/cad-backfill-polygon/index.ts`
- `knocktracker/supabase/functions/generate-route/index.ts`
- `knocktracker/supabase/functions/ghl-sync-contacts/index.ts`
- `knocktracker/supabase/functions/import-osm-territory/index.ts`
- `knocktracker/supabase/functions/integration-webhook/index.ts`
- `knocktracker/supabase/functions/integration-worker/index.ts`
- `knocktracker/supabase/functions/osm-polygon-homes/index.ts`

## Audit Trail

- EXTRACTED: 90 (78%)
- INFERRED: 26 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*