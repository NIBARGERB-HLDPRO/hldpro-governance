# Graph Report - healthcareplatform  (2026-04-09)

## Corpus Check
- Large corpus: 1039 files · ~2,702,839 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1924 nodes · 3033 edges · 207 communities detected
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 903 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `SurveyOfflineStore` - 35 edges
2. `handleVisitSurveyRoute()` - 16 edges
3. `main()` - 15 edges
4. `main()` - 15 edges
5. `asString()` - 12 edges
6. `resolveSeededRouteParams()` - 11 edges
7. `mapAvailityCoverageResponse()` - 11 edges
8. `fail()` - 11 edges
9. `fail()` - 10 edges
10. `readSeedValidationArtifact()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `setupTestUser()`  [INFERRED]
  healthcareplatform/backend/scripts/smoke/smoke-test.js → healthcareplatform/backend/smoke-test.js
- `resolveExistingModuleItem()` --calls--> `asString()`  [INFERRED]
  healthcareplatform/backend/supabase/functions/billing-modules/index.ts → healthcareplatform/backend/supabase/functions/billing-portal/index.ts
- `handleVisitSurveyRoute()` --calls--> `getReport()`  [INFERRED]
  healthcareplatform/backend/supabase/functions/survey/index.ts → healthcareplatform/backend/supabase/functions/reports/index.ts
- `syncTenantTierToAuthUsers()` --calls--> `asRecord()`  [INFERRED]
  healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts → healthcareplatform/backend/supabase/functions/billing-modules/index.ts
- `syncModuleProfilesFromSubscription()` --calls--> `asRecord()`  [INFERRED]
  healthcareplatform/backend/supabase/functions/stripe-webhook/index.ts → healthcareplatform/backend/supabase/functions/billing-modules/index.ts

## Communities

### Community 0 - "Training Supabase"
Cohesion: 0.01
Nodes (171): addDays(), addDocument(), addFinding(), addTracer(), addTracerStep(), appendAuthTimeline(), applyGradeCap(), approveQuiz() (+163 more)

### Community 1 - "Admin State"
Cohesion: 0.02
Nodes (47): asRecord(), asRole(), canManageAdminWorkspace(), createAdminUser(), getAdminUser(), isRoleElevationBlocked(), replaceAdminUserFacilities(), toAssignments() (+39 more)

### Community 2 - "Seeded Auth"
Cohesion: 0.03
Nodes (59): assertAppReady(), assertDeniedRoute(), assertNotFoundRoute(), routeHeadingCandidates(), routePathFromInput(), acceptedLandingPathsFor(), assertAuthenticatedLanding(), assertVisibleNavMarker() (+51 more)

### Community 3 - "Survey sync Finding"
Cohesion: 0.03
Nodes (21): detectConditionLevel(), detectPatterns(), findParentCfc(), groupFindingsByStandard(), SafeLogger, getPosition(), handleChange(), addFinding() (+13 more)

### Community 4 - "Chart audit Insurance"
Cohesion: 0.03
Nodes (42): getProjectRef(), invokeFunction(), invokePublicFunction(), isRecord(), normalizeErrorEnvelope(), readAccessTokenFromStorage(), resolveAccessToken(), toSafeMessage() (+34 more)

### Community 5 - "Supabase Audit"
Cohesion: 0.05
Nodes (25): landingPathForRole(), resolveSafeFromPath(), buildAuditPayload(), corsPreflightResponse(), createAuthValue(), createQueryClient(), createUserClient(), denyTenantMismatch() (+17 more)

### Community 6 - "Training Assignments"
Cohesion: 0.05
Nodes (8): ensureArray(), generateRecommendationDraft(), getTranscript(), listApprovedQuizzes(), listQuizReviewQueue(), listRecommendationDrafts(), listTrainingAssignments(), listTrainingModules()

### Community 7 - "Daily assessment Acquisition"
Cohesion: 0.06
Nodes (12): calculateCategorySummary(), getItemsByCategory(), escapeCsv(), exportRowsToCsv(), getDailyPlan(), getOperatingDayNumberFrom(), formatMMDD(), getFloatingHolidays() (+4 more)

### Community 8 - "Billing Notifications"
Cohesion: 0.07
Nodes (14): createBillingPortalSession(), createCheckoutSession(), createPublicSignup(), getBillingPortalSummary(), getModuleBillingState(), isRecord(), mutateModuleBilling(), parseModuleBillingState() (+6 more)

### Community 9 - "Reports Reviewer"
Cohesion: 0.08
Nodes (19): asFindingStatus(), asRecord(), getFinding(), reviewFinding(), toFinding(), asRecord(), buildReportExportFilename(), generateDraftReport() (+11 more)

### Community 10 - "Survey store Offline"
Cohesion: 0.11
Nodes (1): SurveyOfflineStore

### Community 11 - "Visit Extract From"
Cohesion: 0.15
Nodes (20): assignVisitToSurveyor(), buildSlugs(), callFunction(), decodeJwtPayload(), extractFacilityRowsFromBody(), extractVisitIdFromBody(), extractVisitRowsFromBody(), getEnv() (+12 more)

### Community 12 - "Insurance verification Supabase"
Cohesion: 0.18
Nodes (25): amountToCents(), asRecord(), asRecordArray(), buildAvailityCoverageRequest(), buildExternalFailure(), buildManualVerification(), buildProviderUnconfiguredVerification(), encodeForm() (+17 more)

### Community 13 - "Store Offline"
Cohesion: 0.1
Nodes (5): buildDraftId(), isSafeKeyPart(), parseDraftId(), OfflineStore, SyncEngine

### Community 14 - "Stripe Supabase"
Cohesion: 0.14
Nodes (15): computeSignature(), fallbackMonthlyPriceEnvName(), mapPriceIdToModule(), mapPriceIdToTier(), moduleEnvSuffix(), optionalEnv(), requireEnv(), resolveBillingPortalReturnUrl() (+7 more)

### Community 15 - "Policies Policy"
Cohesion: 0.16
Nodes (11): acknowledgePolicy(), asRecord(), buildQuery(), createPolicy(), getPolicies(), getPolicy(), getPolicyAcknowledgmentSummary(), parsePolicy() (+3 more)

### Community 16 - "Ci Validate subagent evidence"
Cohesion: 0.29
Nodes (17): buildDecisionHelpers(), computeRequiredAgents(), detectTriggers(), ensureTriggerKeysDefined(), fail(), findRepoRoot(), getBackendRoot(), main() (+9 more)

### Community 17 - "Schema Generate effective schema"
Cohesion: 0.26
Nodes (15): apply_alter_table(), apply_create_table(), clean_sql(), ensure_table(), extract_alter_table_statements(), extract_block(), extract_create_table_statements(), extract_execute_alter_sql() (+7 more)

### Community 18 - "Standards releases"
Cohesion: 0.17
Nodes (8): approvePublish(), asRecord(), getReleaseDiffPreview(), getStandardsRelease(), publishRelease(), publishWithSupersession(), requestReleaseReview(), toSummary()

### Community 19 - "Issue3 signed url"
Cohesion: 0.35
Nodes (15): authHeaders(), authToken(), consumeSignedUrl(), evidenceFunctionUrl(), extractVisitRows(), issueDownloadUrl(), isUploadEligibleVisit(), listVisits() (+7 more)

### Community 20 - "Coverage Sorter"
Cohesion: 0.27
Nodes (11): addSortIndicators(), enableUI(), getNthColumn(), getTable(), getTableBody(), getTableHeader(), loadColumns(), loadData() (+3 more)

### Community 21 - "Chart audit Rule engine Supabase"
Cohesion: 0.4
Nodes (12): evaluateAllRules(), evaluatePresenceRule(), evaluateREC02(), evaluateREC04(), evaluateREC05(), evaluateREC06(), evaluateREC08(), evaluateREC10() (+4 more)

### Community 22 - "Demo requests Superadmin"
Cohesion: 0.17
Nodes (0): 

### Community 23 - "Coverage Prettify"
Cohesion: 0.35
Nodes (8): a(), B(), D(), g(), i(), k(), Q(), y()

### Community 24 - "Insurance ai Supabase"
Cohesion: 0.42
Nodes (10): asNumber(), buildInsuranceAiPayload(), clampConfidence(), generateInsuranceAiAssessment(), heuristicAssessment(), maybeModelAssessment(), parseModelOutput(), readAiFeatureEnabled() (+2 more)

### Community 25 - "Issue131 evidence deny audit"
Cohesion: 0.45
Nodes (9): buildAuditUrl(), callCrossTenantEvidenceList(), createTenantAVisitIfNeeded(), fetchRecentListFailedAudits(), hasMatchingDenyAudit(), main(), normalizeBaseUrl(), parseJsonSafe() (+1 more)

### Community 26 - "Ci Validate agents rules"
Cohesion: 0.44
Nodes (10): ensureRangeReferencesResolve(), ensureRequiredPrefixes(), ensureRuleIndexParity(), extractRules(), fail(), main(), parseRuleId(), readFileUtf8() (+2 more)

### Community 27 - "Simple Visit"
Cohesion: 0.24
Nodes (3): login(), main(), runTest()

### Community 28 - "Ci Check search path hardening"
Cohesion: 0.44
Nodes (9): fail(), findCreateFunctionBlocks(), getChangedMigrationFiles(), main(), normalizeArgs(), normalizeFunctionRef(), parseAlterSearchPathSignatures(), parseArgs() (+1 more)

### Community 29 - "Ci Check lane enforcement regression"
Cohesion: 0.44
Nodes (9): deleteBranch(), fail(), main(), psArgs(), removeWorktree(), resolvePsCommand(), resolveRepoRoot(), resolveRootCheckCwd() (+1 more)

### Community 30 - "Chart audit Ccd parser Supabase"
Cohesion: 0.39
Nodes (7): buildSlot(), classifySectionKey(), findElements(), getAttributeValue(), getElementText(), parseCcdDocument(), parseXmlSimple()

### Community 31 - "Twenty crm client"
Cohesion: 0.54
Nodes (7): createActivity(), createPerson(), crmFetch(), findPersonByEmail(), getConfig(), isCrmConfigured(), syncDemoRequestToCrm()

### Community 32 - "Chart audit Fhir parser Supabase"
Cohesion: 0.46
Nodes (6): buildSlot(), classifySectionKey(), extractYear(), getResourceText(), parseFhirBundle(), stripHtml()

### Community 33 - "Ci Check supabase lint security"
Cohesion: 0.54
Nodes (7): fail(), listDetails(), main(), parseArgs(), parseLintPayload(), readInputOrRunLint(), summarize()

### Community 34 - "Ci Validate issue execution governance"
Cohesion: 0.61
Nodes (7): fail(), getCurrentBranch(), getIssueNumberFromBranch(), main(), readJson(), readUtf8(), requirePatterns()

### Community 35 - "Scoring Scoring logic Supabase"
Cohesion: 0.33
Nodes (2): applyGradeCap(), gradeRank()

### Community 36 - "Asc evaluator Call"
Cohesion: 0.57
Nodes (5): callFunction(), main(), normalizeBaseUrl(), parseJsonSafe(), signInWithPassword()

### Community 37 - "Bolt Url"
Cohesion: 0.43
Nodes (5): isFunctionsGatewayRoot(), joinFunctionUrl(), main(), normalizeEnvValue(), readEnv()

### Community 38 - "Ci Check asc evaluator import"
Cohesion: 0.67
Nodes (6): assertImportFnInvariants(), fail(), includesAll(), main(), readJson(), readUtf8()

### Community 39 - "Ci Validate cms cfc sample pack"
Cohesion: 0.62
Nodes (6): fail(), isPositiveInteger(), isSortedBy(), main(), readJsonl(), requireAppendixLinkage()

### Community 40 - "Ci Check progress github alignment"
Cohesion: 0.62
Nodes (6): collectSectionLines(), fail(), hasIssueRef(), main(), parseMarkdownRow(), readUtf8()

### Community 41 - "Walkthrough Click"
Cohesion: 0.33
Nodes (0): 

### Community 42 - "Admin Policy Supabase"
Cohesion: 0.33
Nodes (0): 

### Community 43 - "Runtime selection Supabase"
Cohesion: 0.33
Nodes (0): 

### Community 44 - "Report traceability Supabase"
Cohesion: 0.6
Nodes (4): buildReportCitationTraceability(), normalizeAppendix(), normalizeMappedStandard(), normalizeString()

### Community 45 - "Visit pin gate"
Cohesion: 0.47
Nodes (4): buildDeterministicChecklistSnapshot(), deterministicChecklistSnapshotHash(), evaluateVisitPinGate(), normalizeString()

### Community 46 - "Chart audit Phi scrubber Supabase"
Cohesion: 0.33
Nodes (1): TokenMapper

### Community 47 - "Ci Check no stale mirror gate language"
Cohesion: 0.47
Nodes (4): fail(), isExcluded(), main(), normalizeSlash()

### Community 48 - "Ci Check auth Fail"
Cohesion: 0.67
Nodes (5): fail(), hasAuthMarkers(), main(), parseFunctionVerifyJwt(), readUtf8()

### Community 49 - "Ci Validate state regulatory pack"
Cohesion: 0.6
Nodes (5): fail(), hasLikelyPhi(), isSortedBy(), main(), validatePack()

### Community 50 - "Ci Validate state asc sample pack"
Cohesion: 0.67
Nodes (5): fail(), isSortedBy(), main(), parseArgs(), readJsonl()

### Community 51 - "Gui review slice"
Cohesion: 0.5
Nodes (2): firstEnv(), login()

### Community 52 - "Link content phi gate"
Cohesion: 0.4
Nodes (0): 

### Community 53 - "Coverage Block navigation"
Cohesion: 0.7
Nodes (4): goToNext(), goToPrevious(), makeCurrent(), toggleClass()

### Community 54 - "Demo requests Demo requests Supabase"
Cohesion: 0.5
Nodes (2): inferServiceType(), normalizeServiceType()

### Community 55 - "Corrective actions Capa logic Supabase"
Cohesion: 0.4
Nodes (0): 

### Community 56 - "State import adapter"
Cohesion: 0.7
Nodes (4): buildStateStageSummary(), hasLikelyPhi(), normalizeStatePayload(), validateStatePayload()

### Community 57 - "Cms import adapter"
Cohesion: 0.6
Nodes (3): buildCmsStageSummary(), normalizeCmsImportPayload(), stableJson()

### Community 58 - "Cms import adapter"
Cohesion: 0.5
Nodes (2): assertEquals(), canonicalize()

### Community 59 - "Seed local fixtures"
Cohesion: 0.5
Nodes (2): Ensure-AuthUser(), Query-Scalar()

### Community 60 - "Ci Check mode a route scope"
Cohesion: 0.7
Nodes (4): extractActiveRoutes(), fail(), main(), normalizePath()

### Community 61 - "Ci Check hosted auth matrix classification"
Cohesion: 0.8
Nodes (4): fail(), getInputPath(), main(), readJson()

### Community 62 - "Ci Check claude codex governance alignment"
Cohesion: 0.8
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 63 - "Ci Check no raw error logging"
Cohesion: 0.7
Nodes (4): fail(), lineFromIndex(), main(), walk()

### Community 64 - "Ci Check asc evaluator import behavior"
Cohesion: 0.8
Nodes (4): assertBehavior(), fail(), main(), readUtf8()

### Community 65 - "Ci Check no canonical mirror"
Cohesion: 0.7
Nodes (4): fail(), isIssueLane(), main(), run()

### Community 66 - "Ci Validate supabase gh governance"
Cohesion: 1.0
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 67 - "Ci Validate structured agent cycle plan schema"
Cohesion: 0.9
Nodes (4): fail(), main(), readJson(), requireKey()

### Community 68 - "Schema Validate ingestion schema headers"
Cohesion: 0.83
Nodes (3): extract_header_value(), fail(), main()

### Community 69 - "Tenant isolation validation"
Cohesion: 0.5
Nodes (0): 

### Community 70 - "Role policy validation"
Cohesion: 0.5
Nodes (0): 

### Community 71 - "Export Supabase"
Cohesion: 0.83
Nodes (3): buildCentralizedExportPayload(), isRawIdentifierKey(), sanitizeForExport()

### Community 72 - "Accreditor import adapter"
Cohesion: 0.83
Nodes (3): isAccreditorBody(), isBlank(), validateAccreditorAdapterContract()

### Community 73 - "Audit emission validation"
Cohesion: 0.5
Nodes (0): 

### Community 74 - "Log redaction Supabase"
Cohesion: 0.83
Nodes (3): isSensitiveKey(), redactLogValue(), redactString()

### Community 75 - "Audit Supabase"
Cohesion: 0.83
Nodes (3): hashIdentifier(), normalizeActorRole(), writeEvidenceAuditEvent()

### Community 76 - "Chart audit Scoring Supabase"
Cohesion: 0.67
Nodes (2): classifyBatchScope(), computeBatchResults()

### Community 77 - "Chart audit Rule engine Supabase"
Cohesion: 0.5
Nodes (0): 

### Community 78 - "Survey cfc import"
Cohesion: 1.0
Nodes (3): main(), normalizeUrl(), signIn()

### Community 79 - "Ci Check active workflows"
Cohesion: 0.67
Nodes (2): fail(), main()

### Community 80 - "Ci Check asc evaluator import"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 81 - "Ci Validate pre survey upload"
Cohesion: 1.0
Nodes (3): ensureStringArray(), fail(), main()

### Community 82 - "Ci Check asc evaluator import compat"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 83 - "Issues Capture subagent evidence"
Cohesion: 0.83
Nodes (3): fail(), main(), parseArgs()

### Community 84 - "Photo upload Create"
Cohesion: 0.67
Nodes (0): 

### Community 85 - "Photo upload probe4"
Cohesion: 0.67
Nodes (0): 

### Community 86 - "Mocks Offline"
Cohesion: 0.67
Nodes (0): 

### Community 87 - "Accreditor import adapter"
Cohesion: 0.67
Nodes (0): 

### Community 88 - "Pre survey upload"
Cohesion: 0.67
Nodes (0): 

### Community 89 - "Phase8 8 8 b archival validation"
Cohesion: 0.67
Nodes (0): 

### Community 90 - "Standards source governance"
Cohesion: 1.0
Nodes (2): isBlank(), validateSourceGovernance()

### Community 91 - "Publish workflow Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Phase8 8 3 c audit validation"
Cohesion: 0.67
Nodes (0): 

### Community 93 - "Signed url policy"
Cohesion: 0.67
Nodes (0): 

### Community 94 - "Storage rls validation"
Cohesion: 0.67
Nodes (0): 

### Community 95 - "N8n trigger Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 96 - "Audit export retention validation"
Cohesion: 0.67
Nodes (0): 

### Community 97 - "Checklist assembly Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 98 - "Phase8 8 3 b hardening validation"
Cohesion: 0.67
Nodes (0): 

### Community 99 - "Chart audit Types Supabase"
Cohesion: 0.67
Nodes (0): 

### Community 100 - "Gpt assist Gpt assist phi"
Cohesion: 0.67
Nodes (0): 

### Community 101 - "State regulatory update check"
Cohesion: 1.0
Nodes (2): computeUrlHash(), main()

### Community 102 - "Lane Start lane Ps1"
Cohesion: 0.67
Nodes (0): 

### Community 103 - "Ci Check survey compat"
Cohesion: 0.67
Nodes (0): 

### Community 104 - "Ci Check supabase migration order"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 105 - "Ci Validate state asc wave1 sample packs"
Cohesion: 1.0
Nodes (2): main(), runPack()

### Community 106 - "Testing Run v1 1 local db simulation"
Cohesion: 0.67
Nodes (0): 

### Community 107 - "Testing Preflight v1 1 local"
Cohesion: 1.0
Nodes (2): Ensure-Command(), Fail()

### Community 108 - "Testing Backup local state pre v1 1"
Cohesion: 0.67
Nodes (0): 

### Community 109 - "Issues Sync mirror lane"
Cohesion: 0.67
Nodes (0): 

### Community 110 - "Playwright gate Resolve"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Playwright Resolve"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Photo interaction Create"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Survey Image annotator"
Cohesion: 1.0
Nodes (0): 

### Community 114 - "Policies Policies Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 115 - "Admin Policy Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 116 - "Phase8 8 2 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 117 - "Log redaction Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 118 - "Standards source governance"
Cohesion: 1.0
Nodes (0): 

### Community 119 - "Publish workflow Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 120 - "Phase8 8 6 state integrity validation"
Cohesion: 1.0
Nodes (0): 

### Community 121 - "Phase8 8 8 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 122 - "Issue502 full role crawl matrix validation"
Cohesion: 1.0
Nodes (0): 

### Community 123 - "Scoring presentation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 124 - "Issue292 ai quiz draft gate validation"
Cohesion: 1.0
Nodes (0): 

### Community 125 - "Phase8 8 4 b inputs hash validation"
Cohesion: 1.0
Nodes (0): 

### Community 126 - "Phase8 8 8 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 127 - "Runtime selection Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 128 - "Tenant isolation validation"
Cohesion: 1.0
Nodes (0): 

### Community 129 - "Phase8 8 2 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 130 - "Phase8 8 9 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 131 - "Phase8 8 9 b regeneration validation"
Cohesion: 1.0
Nodes (0): 

### Community 132 - "Role policy validation"
Cohesion: 1.0
Nodes (0): 

### Community 133 - "Phase8 8 3 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 134 - "Phase8 8 5 b version resolution validation"
Cohesion: 1.0
Nodes (0): 

### Community 135 - "Cms 2567 formatter"
Cohesion: 1.0
Nodes (0): 

### Community 136 - "Phase8 8 6 validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 137 - "Phase8 8 3 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 138 - "Issue501 report citation traceability validation"
Cohesion: 1.0
Nodes (0): 

### Community 139 - "Phase8 8 9 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 140 - "Issue301 recommendation draft gate validation"
Cohesion: 1.0
Nodes (0): 

### Community 141 - "Issue300 video analytics validation"
Cohesion: 1.0
Nodes (0): 

### Community 142 - "Issue500 survey scoring finding capa validation"
Cohesion: 1.0
Nodes (0): 

### Community 143 - "Issue294 completion immutability validation"
Cohesion: 1.0
Nodes (0): 

### Community 144 - "Issue293 training assignments validation"
Cohesion: 1.0
Nodes (0): 

### Community 145 - "Phase8 8 5 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 146 - "Issue295 export validation"
Cohesion: 1.0
Nodes (0): 

### Community 147 - "Phase8 8 5 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 148 - "Export Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 149 - "Phase8 8 3 c validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 150 - "Phase8 8 9 a version binding validation"
Cohesion: 1.0
Nodes (0): 

### Community 151 - "Phase8 8 4 a validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 152 - "Audit emission validation"
Cohesion: 1.0
Nodes (0): 

### Community 153 - "Insurance verification Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 154 - "Phase8 8 4 a methodology validation"
Cohesion: 1.0
Nodes (0): 

### Community 155 - "Phase8 8 5 a immutability validation"
Cohesion: 1.0
Nodes (0): 

### Community 156 - "Phase8 8 10 validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 157 - "Signed url policy"
Cohesion: 1.0
Nodes (0): 

### Community 158 - "Phase8 8 4 b validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 159 - "Phase8 8 10 compliance mode validation"
Cohesion: 1.0
Nodes (0): 

### Community 160 - "Chart audit Scoring Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 161 - "Chart audit Route coverage Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 162 - "Chart audit Pilot don review"
Cohesion: 1.0
Nodes (0): 

### Community 163 - "Prepare local supabase"
Cohesion: 1.0
Nodes (0): 

### Community 164 - "Lane Preflight Ps1"
Cohesion: 1.0
Nodes (0): 

### Community 165 - "Ci Check survey"
Cohesion: 1.0
Nodes (0): 

### Community 166 - "Ci Check regulatory seed compat"
Cohesion: 1.0
Nodes (0): 

### Community 167 - "Tailwind"
Cohesion: 1.0
Nodes (0): 

### Community 168 - "Playwright"
Cohesion: 1.0
Nodes (0): 

### Community 169 - "Playwright"
Cohesion: 1.0
Nodes (0): 

### Community 170 - "Playwright comprehensive"
Cohesion: 1.0
Nodes (0): 

### Community 171 - "Playwright seeded"
Cohesion: 1.0
Nodes (0): 

### Community 172 - "Playwright interaction"
Cohesion: 1.0
Nodes (0): 

### Community 173 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 174 - "Vitest"
Cohesion: 1.0
Nodes (0): 

### Community 175 - "Postcss"
Cohesion: 1.0
Nodes (0): 

### Community 176 - "Debug photo upload"
Cohesion: 1.0
Nodes (0): 

### Community 177 - "Community 177"
Cohesion: 1.0
Nodes (0): 

### Community 178 - "Seeded Public auth"
Cohesion: 1.0
Nodes (0): 

### Community 179 - "Vite"
Cohesion: 1.0
Nodes (0): 

### Community 180 - "Setup"
Cohesion: 1.0
Nodes (0): 

### Community 181 - "Permissions"
Cohesion: 1.0
Nodes (0): 

### Community 182 - "Insurance ai Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 183 - "Stripe Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 184 - "Scoring presentation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 185 - "Visit pin gate"
Cohesion: 1.0
Nodes (0): 

### Community 186 - "Pre survey upload"
Cohesion: 1.0
Nodes (0): 

### Community 187 - "Insurance route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 188 - "Report traceability Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 189 - "Chart audit Portfolio route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 190 - "Chart audit Phi validation Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 191 - "Chart audit Ccd parser Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 192 - "Chart audit Trends route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 193 - "Chart audit Ingest structured route"
Cohesion: 1.0
Nodes (0): 

### Community 194 - "Chart audit Qapi feed Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 195 - "Chart audit Phi scrubber Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 196 - "Chart audit Benchmark route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 197 - "Chart audit Qapi pip route"
Cohesion: 1.0
Nodes (0): 

### Community 198 - "Chart audit Fhir parser Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 199 - "Chart audit Schedule route Supabase"
Cohesion: 1.0
Nodes (0): 

### Community 200 - "Ci Check standards provenance schema"
Cohesion: 1.0
Nodes (0): 

### Community 201 - "Testing Init v1 1 scale run"
Cohesion: 1.0
Nodes (0): 

### Community 202 - "Testing Recover hosted jwt gateway"
Cohesion: 1.0
Nodes (0): 

### Community 203 - "Testing Seed option3 full local"
Cohesion: 1.0
Nodes (0): 

### Community 204 - "Testing Seed option3 clinical richness"
Cohesion: 1.0
Nodes (0): 

### Community 205 - "Session Gemini watch Ps1"
Cohesion: 1.0
Nodes (0): 

### Community 206 - "Session Bootstrap Ps1"
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
- **Thin community `Policies Policies Supabase`** (2 nodes): `policies.test.ts`, `hasPhiLikeContent()`
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
- **Thin community `Insurance verification Supabase`** (2 nodes): `insurance-verification.test.ts`, `resetInsuranceEnv()`
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
- **Thin community `Community 177`** (1 nodes): `staging-e2e.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seeded Public auth`** (1 nodes): `staging-public-auth.contract.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Setup`** (1 nodes): `setup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Permissions`** (1 nodes): `permissions.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Insurance ai Supabase`** (1 nodes): `insurance-ai.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stripe Supabase`** (1 nodes): `stripe.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scoring presentation Supabase`** (1 nodes): `scoring-presentation.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Visit pin gate`** (1 nodes): `visit-pin-gate.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pre survey upload`** (1 nodes): `pre-survey-upload-contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Insurance route Supabase`** (1 nodes): `insurance-route-contract.test.ts`
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
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `handleVisitSurveyRoute()` (e.g. with `getReport()` and `saveReport()`) actually correct?**
  _`handleVisitSurveyRoute()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `setupTestUser()` and `runTest()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `parseArgs()` and `fail()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `asString()` (e.g. with `syncTenantTierToAuthUsers()` and `syncModuleProfilesFromSubscription()`) actually correct?**
  _`asString()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `Training Supabase` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Admin State` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._