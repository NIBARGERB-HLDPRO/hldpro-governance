# Graph Report - /Users/bennibarger/Developer/HLDPRO/_worktrees/kt-graphify-phase6  (2026-04-09)

## Corpus Check
- Large corpus: 246 files · ~318,385 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 456 nodes · 660 edges · 38 communities detected
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 125 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `CRMService` - 14 edges
2. `GHLService` - 13 edges
3. `DealService` - 9 edges
4. `saveActivity()` - 8 edges
5. `GHLClient` - 7 edges
6. `runSyncJob()` - 7 edges
7. `ContactService` - 7 edges
8. `logEvent()` - 6 edges
9. `CompanyService` - 6 edges
10. `isObject()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `pointInPolygon()` --calls--> `normalizePolygon()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/kt-graphify-phase6/lib/routing/geo.ts → /Users/bennibarger/Developer/HLDPRO/_worktrees/kt-graphify-phase6/utils/routing/geo.ts

## Communities

### Community 0 - "Map Handle"
Cohesion: 0.05
Nodes (16): buildPolygonRouteViaServer(), buildRoutePlan(), buildRoutePlanFromServerRoute(), buildTerritoryGeoJson(), fetchOsmCandidates(), handleClearSearch(), handleFinishDrawing(), handlePolygonComplete() (+8 more)

### Community 1 - "Ghl sync contacts Supabase"
Cohesion: 0.06
Nodes (13): buildNextPageUrl(), delay(), errorJson(), exponentialBackoff(), fetchAddressFromNominatim(), fetchOverpass(), getLastSuccessfulSync(), getLocation() (+5 more)

### Community 2 - "Routing Geo Draw"
Cohesion: 0.08
Nodes (16): applyHouseCountConstraint(), applyTimeConstraint(), computeDistanceMeters(), computeMinutes(), computeRouteStats(), distancePointToSegmentMeters(), haversineDistanceMeters(), normalizePolygon() (+8 more)

### Community 3 - "Integrations Connectors Enqueue"
Cohesion: 0.1
Nodes (4): loadFailedJobs(), retryJob(), enqueueForEnabledProviders(), getEnabledProviders()

### Community 4 - "Tabs Ghl sync Auth"
Cohesion: 0.06
Nodes (0): 

### Community 5 - "Crm Companies Contacts"
Cohesion: 0.09
Nodes (0): 

### Community 6 - "Contracts Manager contracts Input"
Cohesion: 0.1
Nodes (9): applyWebDate(), endOfDay(), onDateChange(), startOfDay(), isFiniteNumber(), isIsoDateString(), pushCsvRow(), serializeManagerWeeklySummaryPacketToCsv() (+1 more)

### Community 7 - "Routing Weighted route Nearest"
Cohesion: 0.13
Nodes (14): buildRouteFromPolygon(), polygonCentroid(), buildNearestNeighborRoute(), haversineMeters(), nearestNeighbor(), haversineMeters(), routeDistance(), twoOpt() (+6 more)

### Community 8 - "Track Header"
Cohesion: 0.15
Nodes (14): appendNotes(), buildContactUpdate(), chooseContactAction(), detectNearbyRouteStop(), fetchAddressFromNominatim(), findExistingContact(), getFinalStatus(), getLocation() (+6 more)

### Community 9 - "Contact Company"
Cohesion: 0.1
Nodes (3): ActivityService, CompanyService, ContactService

### Community 10 - "Routing Engine Heuristics"
Cohesion: 0.22
Nodes (12): buildFromPin(), buildFromPolygon(), buildLineString(), capCandidates(), computeRouteMeters(), orderCandidates(), toLatLng(), routeDistance() (+4 more)

### Community 11 - "Crm Export"
Cohesion: 0.24
Nodes (1): CRMService

### Community 12 - "Ghl Contact"
Cohesion: 0.32
Nodes (1): GHLService

### Community 13 - "Route optimizer Routes"
Cohesion: 0.21
Nodes (4): calculateDistance(), calculateTotalDistance(), nearestNeighborTSP(), optimizeRoute()

### Community 14 - "Navigation Mobile"
Cohesion: 0.24
Nodes (4): handleNavigation(), toggleGroup(), handleNavigation(), toggleGroup()

### Community 15 - "Deal Deals"
Cohesion: 0.28
Nodes (1): DealService

### Community 16 - "Track Route stop logic"
Cohesion: 0.36
Nodes (4): buildRouteStopOptions(), haversineMeters(), selectNearbyRouteStop(), toCandidates()

### Community 17 - "Backfill cad coordinates Ors"
Cohesion: 0.39
Nodes (6): buildGeocodeQuery(), run(), sleep(), extractFirstGeocode(), geocodeForward(), getOrsConfig()

### Community 18 - "Contracts Contracts Generate"
Cohesion: 0.48
Nodes (5): isGenerateRouteSuccess(), isImportOsmTerritorySuccess(), isObject(), parseGenerateRouteRequest(), parseImportOsmTerritoryRequest()

### Community 19 - "Homeowner lookup Format"
Cohesion: 0.5
Nodes (0): 

### Community 20 - "Map Leaflet map Web"
Cohesion: 0.67
Nodes (0): 

### Community 21 - "Shims React native maps"
Cohesion: 0.67
Nodes (0): 

### Community 22 - "Settings Security Open"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Debug sentinel"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Crm Header Handle"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Map Leaflet map Native"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Ghl connection"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Document picker Web"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Map Use draw polygon"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Metro"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Eslint"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Types Shims"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Not found"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Integration types Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Crm Tag pill"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Import tarrant cad"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Extract tarrant cad"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Document picker Native"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Settings Security Open`** (2 nodes): `security.tsx`, `openSupabaseDashboard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Debug sentinel`** (2 nodes): `DebugSentinel.tsx`, `DebugSentinel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crm Header Handle`** (2 nodes): `PageHeader.tsx`, `handleSearchChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Map Leaflet map Native`** (2 nodes): `LeafletMap.native.tsx`, `LeafletMap()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ghl connection`** (2 nodes): `test-ghl-connection.js`, `testConnection()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Document picker Web`** (2 nodes): `documentPicker.web.ts`, `getDocumentAsync()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Map Use draw polygon`** (2 nodes): `useDrawPolygon.ts`, `useDrawPolygon()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Metro`** (1 nodes): `metro.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Eslint`** (1 nodes): `eslint.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Types Shims`** (1 nodes): `shims.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Not found`** (1 nodes): `+not-found.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Integration types Supabase`** (1 nodes): `integration-types.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crm Tag pill`** (1 nodes): `TagPill.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Import tarrant cad`** (1 nodes): `import-tarrant-cad.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Extract tarrant cad`** (1 nodes): `extract-tarrant-cad.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Document picker Native`** (1 nodes): `documentPicker.native.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRMService` connect `Crm Export` to `Integrations Connectors Enqueue`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `DealService` connect `Deal Deals` to `Integrations Connectors Enqueue`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `ContactService` connect `Contact Company` to `Integrations Connectors Enqueue`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `saveActivity()` (e.g. with `getFinalStatus()` and `getPipelineUpdateForStatus()`) actually correct?**
  _`saveActivity()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Map Handle` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Ghl sync contacts Supabase` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Routing Geo Draw` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._