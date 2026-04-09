# Graph Report - /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform  (2026-04-09)

## Corpus Check
- Large corpus: 998 files · ~2,658,107 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1706 nodes · 2609 edges · 200 communities detected
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 723 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `SurveyOfflineStore` - 35 edges
2. `handleVisitSurveyRoute()` - 16 edges
3. `main()` - 15 edges
4. `main()` - 15 edges
5. `resolveSeededRouteParams()` - 11 edges
6. `fail()` - 11 edges
7. `requireDeterministicId()` - 10 edges
8. `requireAdminLike()` - 10 edges
9. `apply_create_table()` - 9 edges
10. `fail()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `setupTestUser()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/scripts/smoke/smoke-test.js → /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/smoke-test.js
- `handleVisitSurveyRoute()` --calls--> `getReport()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/survey/index.ts → /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/reports/index.ts
- `upsertResponse()` --calls--> `validateUpsertPayload()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/responses/index.ts → /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/acquisition-assessments/index.ts
- `upsertResponse()` --calls--> `computeEffectiveTemplateIds()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/responses/index.ts → /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/checklist-generate/index.ts
- `getChecklist()` --calls--> `computeEffectiveTemplateIds()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/visits/index.ts → /Users/bennibarger/Developer/HLDPRO/HealthcarePlatform/backend/supabase/functions/checklist-generate/index.ts

## Communities

### Community 0 - "Training Supabase"
Cohesion: 0.01
Nodes (121): addDocument(), addFinding(), addTracer(), addTracerStep(), applyGradeCap(), approveQuiz(), approveRecommendation(), auditAiDraft() (+113 more)

### Community 1 - "Corrective actions Visits"
Cohesion: 0.02
Nodes (26): buildViewerContext(), mapRole(), mapTier(), asActionStatus(), asEvidenceLinks(), asRecord(), asVisit(), getCorrectiveAction() (+18 more)

### Community 2 - "Seeded Auth"
Cohesion: 0.03
Nodes (58): assertAppReady(), assertDeniedRoute(), assertNotFoundRoute(), routeHeadingCandidates(), routePathFromInput(), assertAuthenticatedLanding(), assertVisibleNavMarker(), credentialKeys() (+50 more)

### Community 3 - "Survey sync Finding"
Cohesion: 0.03
Nodes (21): detectConditionLevel(), detectPatterns(), findParentCfc(), groupFindingsByStandard(), SafeLogger, getPosition(), handleChange(), addFinding() (+13 more)

### Community 4 - "Integrations Survey"
Cohesion: 0.04
Nodes (34): getProjectRef(), invokeFunction(), isRecord(), normalizeErrorEnvelope(), readAccessTokenFromStorage(), resolveAccessToken(), toSafeMessage(), asCommitEvidenceResponse() (+26 more)

### Community 5 - "Training Assignments"
Cohesion: 0.05
Nodes (8): ensureArray(), generateRecommendationDraft(), getTranscript(), listApprovedQuizzes(), listQuizReviewQueue(), listRecommendationDrafts(), listTrainingAssignments(), listTrainingModules()

### Community 6 - "Daily assessment Acquisition"
Cohesion: 0.06
Nodes (12): calculateCategorySummary(), getItemsByCategory(), escapeCsv(), exportRowsToCsv(), getDailyPlan(), getOperatingDayNumberFrom(), formatMMDD(), getFloatingHolidays() (+4 more)

### Community 7 - "Supabase Admin"
Cohesion: 0.09
Nodes (23): buildAuditPayload(), corsPreflightResponse(), createAuthValue(), createQueryClient(), createUserClient(), denyTenantMismatch(), deterministicSha256Hex(), errorResponse() (+15 more)

### Community 8 - "Reports Reviewer"
Cohesion: 0.08
Nodes (19): asFindingStatus(), asRecord(), getFinding(), reviewFinding(), toFinding(), asRecord(), buildReportExportFilename(), generateDraftReport() (+11 more)

### Community 9 - "Survey store Offline"
Cohesion: 0.11
Nodes (1): SurveyOfflineStore

### Community 10 - "Shell Notifications"
Cohesion: 0.08
Nodes (4): buildBreadcrumbs(), isDynamicPathToken(), copySupportBundleToClipboard(), generateSupportBundle()

### Community 11 - "Store Offline"
Cohesion: 0.08
Nodes (5): buildDraftId(), isSafeKeyPart(), parseDraftId(), OfflineStore, SyncEngine

### Community 12 - "Visit Extract From"
Cohesion: 0.15
Nodes (20): assignVisitToSurveyor(), buildSlugs(), callFunction(), decodeJwtPayload(), extractFacilityRowsFromBody(), extractVisitIdFromBody(), extractVisitRowsFromBody(), getEnv() (+12 more)

### Community 13 - "Admin Facility"
Cohesion: 0.12
Nodes (13): asRecord(), asRole(), canManageAdminWorkspace(), createAdminUser(), getAdminUser(), isRoleElevationBlocked(), replaceAdminUserFacilities(), toAssignments() (+5 more)

### Community 14 - "Chart audit Batch"
Cohesion: 0.09
Nodes (4): asRecord(), createBatch(), getBatch(), toBatch()

### Community 15 - "State regulatory Import"
Cohesion: 0.13
Nodes (8): ApiRequestError, getCrosswalkCompleteness(), getStateCoverageComparison(), getStateGapAnalysis(), getStateRegulatoryBodies(), importStateRegulatory(), stageStateImport(), toApiRequestError()

### Community 16 - "Ci Validate subagent evidence"
Cohesion: 0.29
Nodes (17): buildDecisionHelpers(), computeRequiredAgents(), detectTriggers(), ensureTriggerKeysDefined(), fail(), findRepoRoot(), getBackendRoot(), main() (+9 more)

### Community 17 - "Schema Generate effective schema"
Cohesion: 0.26
Nodes (15): apply_alter_table(), apply_create_table(), clean_sql(), ensure_table(), extract_alter_table_statements(), extract_block(), extract_create_table_statements(), extract_execute_alter_sql() (+7 more)

### Community 18 - "Issue3 signed url"
Cohesion: 0.35
Nodes (15): authHeaders(), authToken(), consumeSignedUrl(), evidenceFunctionUrl(), extractVisitRows(), issueDownloadUrl(), isUploadEligibleVisit(), listVisits() (+7 more)

### Community 19 - "Coverage Sorter"
Cohesion: 0.27
Nodes (11): addSortIndicators(), enableUI(), getNthColumn(), getTable(), getTableBody(), getTableHeader(), loadColumns(), loadData() (+3 more)

### Community 20 - "Chart audit Rule engine Supabase"
Cohesion: 0.4
Nodes (12): evaluateAllRules(), evaluatePresenceRule(), evaluateREC02(), evaluateREC04(), evaluateREC05(), evaluateREC06(), evaluateREC08(), evaluateREC10() (+4 more)

### Community 21 - "Coverage Prettify"
Cohesion: 0.35
Nodes (8): a(), B(), D(), g(), i(), k(), Q(), y()

### Community 22 - "Demo requests Superadmin"
Cohesion: 0.18
Nodes (0): 

### Community 23 - "Issue131 evidence deny audit"
Cohesion: 0.45
Nodes (9): buildAuditUrl(), callCrossTenantEvidenceList(), createTenantAVisitIfNeeded(), fetchRecentListFailedAudits(), hasMatchingDenyAudit(), main(), normalizeBaseUrl(), parseJsonSafe() (+1 more)

### Community 24 - "Ci Validate agents rules"
Cohesion: 0.44
Nodes (10): ensureRangeReferencesResolve(), ensureRequiredPrefixes(), ensureRuleIndexParity(), extractRules(), fail(), main(), parseRuleId(), readFileUtf8() (+2 more)

### Community 25 - "Simple Visit"
Cohesion: 0.24
Nodes (3): login(), main(), runTest()

### Community 26 - "Ci Check search path hardening"
Cohesion: 0.44
Nodes (9): fail(), findCreateFunctionBlocks(), getChangedMigrationFiles(), main(), normalizeArgs(), normalizeFunctionRef(), parseAlterSearchPathSignatures(), parseArgs() (+1 more)

### Community 27 - "Ci Check lane enforcement regression"
Cohesion: 0.44
Nodes (9): deleteBranch(), fail(), main(), psArgs(), removeWorktree(), resolvePsCommand(), resolveRepoRoot(), resolveRootCheckCwd() (+1 more)

### Community 28 - "Chart audit Ccd parser Supabase"
Cohesion: 0.39
Nodes (7): buildSlot(), classifySectionKey(), findElements(), getAttributeValue(), getElementText(), parseCcdDocument(), parseXmlSimple()

### Community 29 - "Twenty crm client"
Cohesion: 0.54
Nodes (7): createActivity(), createPerson(), crmFetch(), findPersonByEmail(), getConfig(), isCrmConfigured(), syncDemoRequestToCrm()

### Community 30 - "Chart audit Fhir parser Supabase"
Cohesion: 0.46
Nodes (6): buildSlot(), classifySectionKey(), extractYear(), getResourceText(), parseFhirBundle(), stripHtml()

### Community 31 - "Ci Check supabase lint security"
Cohesion: 0.54
Nodes (7): fail(), listDetails(), main(), parseArgs(), parseLintPayload(), readInputOrRunLint(), summarize()

### Community 32 - "Ci Validate issue execution governance"
Cohesion: 0.61
Nodes (7): fail(), getCurrentBranch(), getIssueNumberFromBranch(), main(), readJson(), readUtf8(), requirePatterns()

### Community 33 - "Scoring Scoring logic Supabase"
Cohesion: 0.33
Nodes (2): applyGradeCap(), gradeRank()

### Community 34 - "Asc evaluator Call"
Cohesion: 0.57
Nodes (5): callFunction(), main(), normalizeBaseUrl(), parseJsonSafe(), signInWithPassword()

### Community 35 - "Bolt Url"
Cohesion: 0.43
Nodes (5): isFunctionsGatewayRoot(), joinFunctionUrl(), main(), normalizeEnvValue(), readEnv()

### Community 36 - "Ci Check asc evaluator import"
Cohesion: 0.67
Nodes (6): assertImportFnInvariants(), fail(), includesAll(), main(), readJson(), readUtf8()

### Community 37 - "Ci Validate cms cfc sample pack"
Cohesion: 0.62
Nodes (6): fail(), isPositiveInteger(), isSortedBy(), main(), readJsonl(), requireAppendixLinkage()

### Community 38 - "Ci Check progress github alignment"
Cohesion: 0.62
Nodes (6): collectSectionLines(), fail(), hasIssueRef(), main(), parseMarkdownRow(), readUtf8()

### Community 39 - "Walkthrough Click"
Cohesion: 0.33
Nodes (0): 

### Community 40 - "Admin Policy Supabase"
Cohesion: 0.33
Nodes (0): 

### Community 41 - "Runtime selection Supabase"
Cohesion: 0.33
Nodes (0): 

### Community 42 - "Report traceability Supabase"
Cohesion: 0.6
Nodes (4): buildReportCitationTraceability(), normalizeAppendix(), normalizeMappedStandard(), normalizeString()

### Community 43 - "Visit pin gate"
Cohesion: 0.47
Nodes (4): buildDeterministicChecklistSnapshot(), deterministicChecklistSnapshotHash(), evaluateVisitPinGate(), normalizeString()

### Community 44 - "Chart audit Phi scrubber Supabase"
Cohesion: 0.33
Nodes (1): TokenMapper

### Community 45 - "Ci Check no stale mirror gate language"
Cohesion: 0.47
Nodes (4): fail(), isExcluded(), main(), normalizeSlash()

### Community 46 - "Ci Check auth Fail"
Cohesion: 0.67
Nodes (5): fail(), hasAuthMarkers(), main(), parseFunctionVerifyJwt(), readUtf8()

### Community 47 - "Ci Validate state regulatory pack"
Cohesion: 0.6
Nodes (5): fail(), hasLikelyPhi(), isSortedBy(), main(), validatePack()

### Community 48 - "Ci Validate state asc sample pack"
Cohesion: 0.67
Nodes (5): fail(), isSortedBy(), main(), parseArgs(), readJsonl()

### Community 49 - "Gui review slice"
Cohesion: 0.5
Nodes (2): firstEnv(), login()

### Community 50 - "Link content phi gate"
Cohesion: 0.4
Nodes (0): 

### Community 51 - "Coverage Block navigation"
Cohesion: 0.7
Nodes (4): goToNext(), goToPrevious(), makeCurrent(), toggleClass()

### Community 52 - "Corrective actions Capa logic Supabase"
Cohesion: 0.4
Nodes (0): 

### Community 53 - "State import adapter"
Cohesion: 0.7
Nodes (4): buildStateStageSummary(), hasLikelyPhi(), normalizeStatePayload(), validateStatePayload()

### Community 54 - "Cms import adapter"
Cohesion: 0.6
Nodes (3): buildCmsStageSummary(), normalizeCmsImportPayload(), stableJson()

### Community 55 - "Cms import adapter"
Cohesion: 0.5
Nodes (2): assertEquals(), canonicalize()

### Community 56 - "Seed local fixtures"
Cohesion: 0.5
Nodes (2): Ensure-AuthUser(), Query-Scalar()

### Community 57 - "Ci Check mode a route scope"
Cohesion: 0.7
Nodes (4): extractActiveRoutes(), fail(), main(), normalizePath()

### Community 58 - "Ci Check hosted auth matrix classification"
Cohesion: 0.8
Nodes (4): fail(), getInputPath(), main(), readJson()

### Community 59 - "Ci Check claude codex governance alignment"
Cohesion: 0.8
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 60 - "Ci Check no raw error logging"
Cohesion: 0.7
Nodes (4): fail(), lineFromIndex(), main(), walk()

### Community 61 - "Ci Check asc evaluator import behavior"
Cohesion: 0.8
Nodes (4): assertBehavior(), fail(), main(), readUtf8()

### Community 62 - "Ci Check no canonical mirror"
Cohesion: 0.7
Nodes (4): fail(), isIssueLane(), main(), run()

### Community 63 - "Ci Validate supabase gh governance"
Cohesion: 1.0
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 64 - "Ci Validate structured agent cycle plan schema"
Cohesion: 0.9
Nodes (4): fail(), main(), readJson(), requireKey()

### Community 65 - "Schema Validate ingestion schema headers"
Cohesion: 0.83
Nodes (3): extract_header_value(), fail(), main()

### Community 66 - "Tenant isolation validation"
Cohesion: 0.5
Nodes (0): 

### Community 67 - "Role policy validation"
Cohesion: 0.5
Nodes (0): 

### Community 68 - "Export Supabase"
Cohesion: 0.83
Nodes (3): buildCentralizedExportPayload(), isRawIdentifierKey(), sanitizeForExport()

### Community 69 - "Accreditor import adapter"
Cohesion: 0.83
Nodes (3): isAccreditorBody(), isBlank(), validateAccreditorAdapterContract()

### Community 70 - "Audit emission validation"
Cohesion: 0.5
Nodes (0): 

### Community 71 - "Log redaction Supabase"
Cohesion: 0.83
Nodes (3): isSensitiveKey(), redactLogValue(), redactString()

### Community 72 - "Audit Supabase"
Cohesion: 0.83
Nodes (3): hashIdentifier(), normalizeActorRole(), writeEvidenceAuditEvent()

### Community 73 - "Chart audit Scoring Supabase"
Cohesion: 0.67
Nodes (2): classifyBatchScope(), computeBatchResults()

### Community 74 - "Chart audit Rule engine Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 75 - "Survey cfc import"
Cohesion: 1.0
Nodes (3): main(), normalizeUrl(), signIn()

### Community 76 - "Ci Check active workflows"
Cohesion: 0.67
Nodes (2): fail(), main()

### Community 77 - "Ci Check asc evaluator import"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 78 - "Ci Validate pre survey upload"
Cohesion: 1.0
Nodes (3): ensureStringArray(), fail(), main()

### Community 79 - "Ci Check asc evaluator import compat"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 80 - "Issues Capture subagent evidence"
Cohesion: 0.83
Nodes (3): fail(), main(), parseArgs()

### Community 81 - "Photo upload Create"
Cohesion: 0.67
Nodes (0): 

### Community 82 - "Photo upload probe4"
Cohesion: 0.67
Nodes (0): 

### Community 83 - "Mocks Offline"
Cohesion: 0.67
Nodes (0): 

### Community 84 - "Demo requests Demo requests Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 85 - "Accreditor import adapter"
Cohesion: 0.67
Nodes (0): 

### Community 86 - "Pre survey upload"
Cohesion: 0.67
Nodes (0): 

### Community 87 - "Phase8 8 8 b archival validation"
Cohesion: 0.67
Nodes (0): 

### Community 88 - "Standards source governance"
Cohesion: 1.0
Nodes (2): isBlank(), validateSourceGovernance()

### Community 89 - "Publish workflow Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 90 - "Phase8 8 3 c audit validation"
Cohesion: 0.67
Nodes (0): 

### Community 91 - "Signed url policy"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Storage rls validation"
Cohesion: 0.67
Nodes (0): 

### Community 93 - "N8n trigger Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 94 - "Audit export retention validation"
Cohesion: 0.67
Nodes (0): 

### Community 95 - "Checklist assembly Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 96 - "Phase8 8 3 b hardening validation"
Cohesion: 0.67
Nodes (0): 

### Community 97 - "Chart audit Types Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 98 - "Gpt assist Gpt assist phi"
Cohesion: 0.67
Nodes (0): 

### Community 99 - "State regulatory update check"
Cohesion: 1.0
Nodes (2): computeUrlHash(), main()

### Community 100 - "Lane Start lane Ps1"
Cohesion: 0.67
Nodes (0): 

### Community 101 - "Ci Check survey compat"
Cohesion: 0.67
Nodes (0): 

### Community 102 - "Ci Check supabase migration order"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 103 - "Ci Validate state asc wave1 sample packs"
Cohesion: 1.0
Nodes (2): main(), runPack()

### Community 104 - "Testing Run v1 1 local db simulation"
Cohesion: 0.67
Nodes (0): 

### Community 105 - "Testing Preflight v1 1 local"
Cohesion: 1.0
Nodes (2): Ensure-Command(), Fail()

### Community 106 - "Testing Backup local state pre v1 1"
Cohesion: 0.67
Nodes (0): 

### Community 107 - "Issues Sync mirror lane"
Cohesion: 0.67
Nodes (0): 

### Community 108 - "Playwright gate Resolve"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Playwright Resolve"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Photo interaction Create"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Survey Image annotator"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Admin Policy Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Phase8 8 2 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 114 - "Log redaction Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 115 - "Standards source governance"
Cohesion: 1.0
Nodes (0): 

### Community 116 - "Publish workflow Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 117 - "Phase8 8 6 state integrity validation"
Cohesion: 1.0
Nodes (0): 

### Community 118 - "Phase8 8 8 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 119 - "Issue502 full role crawl matrix validation"
Cohesion: 1.0
Nodes (0): 

### Community 120 - "Scoring presentation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 121 - "Issue292 ai quiz draft gate validation"
Cohesion: 1.0
Nodes (0): 

### Community 122 - "Phase8 8 4 b inputs hash validation"
Cohesion: 1.0
Nodes (0): 

### Community 123 - "Phase8 8 8 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 124 - "Runtime selection Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 125 - "Tenant isolation validation"
Cohesion: 1.0
Nodes (0): 

### Community 126 - "Phase8 8 2 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 127 - "Phase8 8 9 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 128 - "Phase8 8 9 b regeneration validation"
Cohesion: 1.0
Nodes (0): 

### Community 129 - "Role policy validation"
Cohesion: 1.0
Nodes (0): 

### Community 130 - "Phase8 8 3 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 131 - "Phase8 8 5 b version resolution validation"
Cohesion: 1.0
Nodes (0): 

### Community 132 - "Cms 2567 formatter"
Cohesion: 1.0
Nodes (0): 

### Community 133 - "Phase8 8 6 validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 134 - "Phase8 8 3 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 135 - "Issue501 report citation traceability validation"
Cohesion: 1.0
Nodes (0): 

### Community 136 - "Phase8 8 9 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 137 - "Issue301 recommendation draft gate validation"
Cohesion: 1.0
Nodes (0): 

### Community 138 - "Issue300 video analytics validation"
Cohesion: 1.0
Nodes (0): 

### Community 139 - "Issue500 survey scoring finding capa validation"
Cohesion: 1.0
Nodes (0): 

### Community 140 - "Issue294 completion immutability validation"
Cohesion: 1.0
Nodes (0): 

### Community 141 - "Issue293 training assignments validation"
Cohesion: 1.0
Nodes (0): 

### Community 142 - "Phase8 8 5 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 143 - "Issue295 export validation"
Cohesion: 1.0
Nodes (0): 

### Community 144 - "Phase8 8 5 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 145 - "Export Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 146 - "Phase8 8 3 c validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 147 - "Phase8 8 9 a version binding validation"
Cohesion: 1.0
Nodes (0): 

### Community 148 - "Phase8 8 4 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 149 - "Audit emission validation"
Cohesion: 1.0
Nodes (0): 

### Community 150 - "Phase8 8 4 a methodology validation"
Cohesion: 1.0
Nodes (0): 

### Community 151 - "Phase8 8 5 a immutability validation"
Cohesion: 1.0
Nodes (0): 

### Community 152 - "Phase8 8 10 validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 153 - "Signed url policy"
Cohesion: 1.0
Nodes (0): 

### Community 154 - "Phase8 8 4 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 155 - "Phase8 8 10 compliance mode validation"
Cohesion: 1.0
Nodes (0): 

### Community 156 - "Chart audit Scoring Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 157 - "Chart audit Route coverage Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 158 - "Chart audit Pilot don review"
Cohesion: 1.0
Nodes (0): 

### Community 159 - "Prepare local supabase"
Cohesion: 1.0
Nodes (0): 

### Community 160 - "Lane Preflight Ps1"
Cohesion: 1.0
Nodes (0): 

### Community 161 - "Ci Check survey"
Cohesion: 1.0
Nodes (0): 

### Community 162 - "Ci Check regulatory seed compat"
Cohesion: 1.0
Nodes (0): 

### Community 163 - "Tailwind"
Cohesion: 1.0
Nodes (0): 

### Community 164 - "Playwright"
Cohesion: 1.0
Nodes (0): 

### Community 165 - "Playwright"
Cohesion: 1.0
Nodes (0): 

### Community 166 - "Playwright comprehensive"
Cohesion: 1.0
Nodes (0): 

### Community 167 - "Playwright seeded"
Cohesion: 1.0
Nodes (0): 

### Community 168 - "Playwright interaction"
Cohesion: 1.0
Nodes (0): 

### Community 169 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 170 - "Vitest"
Cohesion: 1.0
Nodes (0): 

### Community 171 - "Postcss"
Cohesion: 1.0
Nodes (0): 

### Community 172 - "Debug photo upload"
Cohesion: 1.0
Nodes (0): 

### Community 173 - "Community 173"
Cohesion: 1.0
Nodes (0): 

### Community 174 - "Seeded Public auth"
Cohesion: 1.0
Nodes (0): 

### Community 175 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 176 - "Setup"
Cohesion: 1.0
Nodes (0): 

### Community 177 - "Permissions"
Cohesion: 1.0
Nodes (0): 

### Community 178 - "Scoring presentation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 179 - "Visit pin gate"
Cohesion: 1.0
Nodes (0): 

### Community 180 - "Pre survey upload"
Cohesion: 1.0
Nodes (0): 

### Community 181 - "Report traceability Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 182 - "Chart audit Portfolio route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 183 - "Chart audit Phi validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 184 - "Chart audit Ccd parser Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 185 - "Chart audit Trends route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 186 - "Chart audit Ingest structured route"
Cohesion: 1.0
Nodes (0): 

### Community 187 - "Chart audit Qapi feed Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 188 - "Chart audit Phi scrubber Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 189 - "Chart audit Benchmark route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 190 - "Chart audit Qapi pip route"
Cohesion: 1.0
Nodes (0): 

### Community 191 - "Chart audit Fhir parser Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 192 - "Chart audit Schedule route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 193 - "Ci Check standards provenance schema"
Cohesion: 1.0
Nodes (0): 

### Community 194 - "Testing Init v1 1 scale run"
Cohesion: 1.0
Nodes (0): 

### Community 195 - "Testing Recover hosted jwt gateway"
Cohesion: 1.0
Nodes (0): 

### Community 196 - "Testing Seed option3 full local"
Cohesion: 1.0
Nodes (0): 

### Community 197 - "Testing Seed option3 clinical richness"
Cohesion: 1.0
Nodes (0): 

### Community 198 - "Session Gemini watch Ps1"
Cohesion: 1.0
Nodes (0): 

### Community 199 - "Session Bootstrap Ps1"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Playwright gate Resolve`** (2 nodes): `playwright.gate.config.ts`, `resolveEnvOrDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright Resolve`** (2 nodes): `playwright.config.ts`, `resolveEnvOrDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Photo interaction Create`** (2 nodes): `photo-interaction.spec.ts`, `createTestImage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Survey Image annotator`** (2 nodes): `ImageAnnotator.tsx`, `ImageAnnotator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Admin Policy Supabase`** (2 nodes): `policy.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 2 b validation Supabase`** (2 nodes): `phase8-8-2-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Log redaction Supabase`** (2 nodes): `log-redaction.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Standards source governance`** (2 nodes): `standards-source-governance.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Publish workflow Supabase`** (2 nodes): `publish-workflow.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 6 state integrity validation`** (2 nodes): `phase8-8-6-state-integrity-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 8 b validation Supabase`** (2 nodes): `phase8-8-8-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue502 full role crawl matrix validation`** (2 nodes): `issue502-full-role-crawl-matrix-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scoring presentation Supabase`** (2 nodes): `scoring-presentation.ts`, `mapScoreToCmsOutcome()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue292 ai quiz draft gate validation`** (2 nodes): `issue292-ai-quiz-draft-gate-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 4 b inputs hash validation`** (2 nodes): `phase8-8-4-b-inputs-hash-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 8 a validation Supabase`** (2 nodes): `phase8-8-8-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Runtime selection Supabase`** (2 nodes): `runtime-selection.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tenant isolation validation`** (2 nodes): `tenant-isolation-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 2 a validation Supabase`** (2 nodes): `phase8-8-2-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 9 b validation Supabase`** (2 nodes): `phase8-8-9-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 9 b regeneration validation`** (2 nodes): `phase8-8-9-b-regeneration-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Role policy validation`** (2 nodes): `role-policy-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 3 b validation Supabase`** (2 nodes): `phase8-8-3-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 5 b version resolution validation`** (2 nodes): `phase8-8-5-b-version-resolution-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Cms 2567 formatter`** (2 nodes): `cms-2567-formatter.ts`, `formatCms2567()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 6 validation Supabase`** (2 nodes): `phase8-8-6-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 3 a validation Supabase`** (2 nodes): `phase8-8-3-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue501 report citation traceability validation`** (2 nodes): `issue501-report-citation-traceability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 9 a validation Supabase`** (2 nodes): `phase8-8-9-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue301 recommendation draft gate validation`** (2 nodes): `issue301-recommendation-draft-gate-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue300 video analytics validation`** (2 nodes): `issue300-video-analytics-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue500 survey scoring finding capa validation`** (2 nodes): `issue500-survey-scoring-finding-capa-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue294 completion immutability validation`** (2 nodes): `issue294-completion-immutability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue293 training assignments validation`** (2 nodes): `issue293-training-assignments-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 5 a validation Supabase`** (2 nodes): `phase8-8-5-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue295 export validation`** (2 nodes): `issue295-export-service-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 5 b validation Supabase`** (2 nodes): `phase8-8-5-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Export Supabase`** (2 nodes): `export-service.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 3 c validation Supabase`** (2 nodes): `phase8-8-3-c-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 9 a version binding validation`** (2 nodes): `phase8-8-9-a-version-binding-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 4 a validation Supabase`** (2 nodes): `phase8-8-4-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Audit emission validation`** (2 nodes): `audit-emission-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 4 a methodology validation`** (2 nodes): `phase8-8-4-a-methodology-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 5 a immutability validation`** (2 nodes): `phase8-8-5-a-immutability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 10 validation Supabase`** (2 nodes): `phase8-8-10-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Signed url policy`** (2 nodes): `signed-url-policy.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 4 b validation Supabase`** (2 nodes): `phase8-8-4-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase8 8 10 compliance mode validation`** (2 nodes): `phase8-8-10-compliance-mode-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Scoring Supabase`** (2 nodes): `scoring.test.ts`, `makeFinding()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Route coverage Supabase`** (2 nodes): `route-coverage.test.ts`, `readSource()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Pilot don review`** (2 nodes): `pilot-don-review.test.ts`, `slot()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Prepare local supabase`** (2 nodes): `prepare-local-supabase-env.ps1`, `Get-ValueFromStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lane Preflight Ps1`** (2 nodes): `preflight.ps1`, `Fail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ci Check survey`** (2 nodes): `check-survey-edge-function-contract.js`, `check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ci Check regulatory seed compat`** (2 nodes): `check-regulatory-seed-compat.js`, `check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tailwind`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright`** (1 nodes): `playwright.staging.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright`** (1 nodes): `playwright.production-readonly.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright comprehensive`** (1 nodes): `playwright.comprehensive.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright seeded`** (1 nodes): `playwright.seeded-staging.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Playwright interaction`** (1 nodes): `playwright.interaction.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vitest`** (1 nodes): `vitest.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Postcss`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Debug photo upload`** (1 nodes): `debug-photo-upload.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `staging-e2e.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seeded Public auth`** (1 nodes): `staging-public-auth.contract.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Setup`** (1 nodes): `setup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissions`** (1 nodes): `permissions.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scoring presentation Supabase`** (1 nodes): `scoring-presentation.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Visit pin gate`** (1 nodes): `visit-pin-gate.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pre survey upload`** (1 nodes): `pre-survey-upload-contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Report traceability Supabase`** (1 nodes): `report-traceability.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Portfolio route Supabase`** (1 nodes): `portfolio-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Phi validation Supabase`** (1 nodes): `phi-validation.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Ccd parser Supabase`** (1 nodes): `ccd-parser.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Trends route Supabase`** (1 nodes): `trends-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Ingest structured route`** (1 nodes): `ingest-structured-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Qapi feed Supabase`** (1 nodes): `qapi-feed.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Phi scrubber Supabase`** (1 nodes): `phi-scrubber.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Benchmark route Supabase`** (1 nodes): `benchmark-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Qapi pip route`** (1 nodes): `qapi-pip-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Fhir parser Supabase`** (1 nodes): `fhir-parser.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Chart audit Schedule route Supabase`** (1 nodes): `schedule-route.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ci Check standards provenance schema`** (1 nodes): `check-standards-provenance-schema.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Testing Init v1 1 scale run`** (1 nodes): `init-v1_1-scale-run.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Testing Recover hosted jwt gateway`** (1 nodes): `recover-hosted-jwt-gateway.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Testing Seed option3 full local`** (1 nodes): `seed-option3-full-local.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Testing Seed option3 clinical richness`** (1 nodes): `seed-option3-clinical-richness.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Session Gemini watch Ps1`** (1 nodes): `gemini_watch.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Session Bootstrap Ps1`** (1 nodes): `bootstrap.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SurveyOfflineStore` connect `Survey store Offline` to `Survey sync Finding`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `handleVisitSurveyRoute()` (e.g. with `getReport()` and `saveReport()`) actually correct?**
  _`handleVisitSurveyRoute()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `setupTestUser()` and `runTest()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `parseArgs()` and `fail()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `resolveSeededRouteParams()` (e.g. with `requireSeededVisitId()` and `defaultVisitIdForTier()`) actually correct?**
  _`resolveSeededRouteParams()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Training Supabase` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Corrective actions Visits` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._