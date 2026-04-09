# Graph Report - /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4  (2026-04-09)

## Corpus Check
- Large corpus: 867 files · ~2,624,240 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 1549 nodes · 2396 edges · 176 communities detected
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 651 edges (avg confidence: 0.5)
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
  /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/scripts/smoke/smoke-test.js → /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/smoke-test.js
- `handleVisitSurveyRoute()` --calls--> `getReport()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/survey/index.ts → /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/reports/index.ts
- `upsertResponse()` --calls--> `validateUpsertPayload()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/responses/index.ts → /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/acquisition-assessments/index.ts
- `upsertResponse()` --calls--> `computeEffectiveTemplateIds()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/responses/index.ts → /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/checklist-generate/index.ts
- `getChecklist()` --calls--> `computeEffectiveTemplateIds()`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/visits/index.ts → /Users/bennibarger/Developer/HLDPRO/_worktrees/hp-graphify-phase4/backend/supabase/functions/checklist-generate/index.ts

## Communities

### Community 0 - "Community 0"
Cohesion: 0.01
Nodes (116): addDocument(), addFinding(), addTracer(), addTracerStep(), applyGradeCap(), approveQuiz(), approveRecommendation(), auditAiDraft() (+108 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (24): buildViewerContext(), mapRole(), mapTier(), asActionStatus(), asEvidenceLinks(), asRecord(), asVisit(), getCorrectiveAction() (+16 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (50): assertAppReady(), assertDeniedRoute(), assertNotFoundRoute(), routeHeadingCandidates(), routePathFromInput(), assertAuthenticatedLanding(), assertVisibleNavMarker(), credentialKeys() (+42 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (21): detectConditionLevel(), detectPatterns(), findParentCfc(), groupFindingsByStandard(), SafeLogger, getPosition(), handleChange(), addFinding() (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (46): getProjectRef(), invokeFunction(), isRecord(), normalizeErrorEnvelope(), readAccessTokenFromStorage(), resolveAccessToken(), toSafeMessage(), asCommitEvidenceResponse() (+38 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (8): ensureArray(), generateRecommendationDraft(), getTranscript(), listApprovedQuizzes(), listQuizReviewQueue(), listRecommendationDrafts(), listTrainingAssignments(), listTrainingModules()

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (12): calculateCategorySummary(), getItemsByCategory(), escapeCsv(), exportRowsToCsv(), getDailyPlan(), getOperatingDayNumberFrom(), formatMMDD(), getFloatingHolidays() (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (23): buildAuditPayload(), corsPreflightResponse(), createAuthValue(), createQueryClient(), createUserClient(), denyTenantMismatch(), deterministicSha256Hex(), errorResponse() (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (1): SurveyOfflineStore

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (4): buildBreadcrumbs(), isDynamicPathToken(), copySupportBundleToClipboard(), generateSupportBundle()

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (5): buildDraftId(), isSafeKeyPart(), parseDraftId(), OfflineStore, SyncEngine

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (20): assignVisitToSurveyor(), buildSlugs(), callFunction(), decodeJwtPayload(), extractFacilityRowsFromBody(), extractVisitIdFromBody(), extractVisitRowsFromBody(), getEnv() (+12 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (13): asRecord(), asRole(), canManageAdminWorkspace(), createAdminUser(), getAdminUser(), isRoleElevationBlocked(), replaceAdminUserFacilities(), toAssignments() (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (8): ApiRequestError, getCrosswalkCompleteness(), getStateCoverageComparison(), getStateGapAnalysis(), getStateRegulatoryBodies(), importStateRegulatory(), stageStateImport(), toApiRequestError()

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (17): buildDecisionHelpers(), computeRequiredAgents(), detectTriggers(), ensureTriggerKeysDefined(), fail(), findRepoRoot(), getBackendRoot(), main() (+9 more)

### Community 15 - "Community 15"
Cohesion: 0.26
Nodes (15): apply_alter_table(), apply_create_table(), clean_sql(), ensure_table(), extract_alter_table_statements(), extract_block(), extract_create_table_statements(), extract_execute_alter_sql() (+7 more)

### Community 16 - "Community 16"
Cohesion: 0.35
Nodes (15): authHeaders(), authToken(), consumeSignedUrl(), evidenceFunctionUrl(), extractVisitRows(), issueDownloadUrl(), isUploadEligibleVisit(), listVisits() (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.17
Nodes (7): asRecord(), getIntegrationReferenceData(), getIntegrationRuns(), getIntegrationStatus(), toReferenceItems(), toRuns(), toStatus()

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 0.45
Nodes (9): buildAuditUrl(), callCrossTenantEvidenceList(), createTenantAVisitIfNeeded(), fetchRecentListFailedAudits(), hasMatchingDenyAudit(), main(), normalizeBaseUrl(), parseJsonSafe() (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.44
Nodes (10): ensureRangeReferencesResolve(), ensureRequiredPrefixes(), ensureRuleIndexParity(), extractRules(), fail(), main(), parseRuleId(), readFileUtf8() (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.24
Nodes (3): login(), main(), runTest()

### Community 22 - "Community 22"
Cohesion: 0.44
Nodes (9): fail(), findCreateFunctionBlocks(), getChangedMigrationFiles(), main(), normalizeArgs(), normalizeFunctionRef(), parseAlterSearchPathSignatures(), parseArgs() (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.44
Nodes (9): deleteBranch(), fail(), main(), psArgs(), removeWorktree(), resolvePsCommand(), resolveRepoRoot(), resolveRootCheckCwd() (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.54
Nodes (7): createActivity(), createPerson(), crmFetch(), findPersonByEmail(), getConfig(), isCrmConfigured(), syncDemoRequestToCrm()

### Community 25 - "Community 25"
Cohesion: 0.54
Nodes (7): fail(), listDetails(), main(), parseArgs(), parseLintPayload(), readInputOrRunLint(), summarize()

### Community 26 - "Community 26"
Cohesion: 0.61
Nodes (7): fail(), getCurrentBranch(), getIssueNumberFromBranch(), main(), readJson(), readUtf8(), requirePatterns()

### Community 27 - "Community 27"
Cohesion: 0.48
Nodes (5): getEnvOrThrow(), getServiceClient(), verifyEvidenceExists(), verifyPrestudyDocument(), verifyStorageFileExists()

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (2): applyGradeCap(), gradeRank()

### Community 29 - "Community 29"
Cohesion: 0.57
Nodes (5): callFunction(), main(), normalizeBaseUrl(), parseJsonSafe(), signInWithPassword()

### Community 30 - "Community 30"
Cohesion: 0.43
Nodes (5): isFunctionsGatewayRoot(), joinFunctionUrl(), main(), normalizeEnvValue(), readEnv()

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (6): assertImportFnInvariants(), fail(), includesAll(), main(), readJson(), readUtf8()

### Community 32 - "Community 32"
Cohesion: 0.62
Nodes (6): fail(), isPositiveInteger(), isSortedBy(), main(), readJsonl(), requireAppendixLinkage()

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 0.6
Nodes (4): buildReportCitationTraceability(), normalizeAppendix(), normalizeMappedStandard(), normalizeString()

### Community 37 - "Community 37"
Cohesion: 0.47
Nodes (4): buildDeterministicChecklistSnapshot(), deterministicChecklistSnapshotHash(), evaluateVisitPinGate(), normalizeString()

### Community 38 - "Community 38"
Cohesion: 0.47
Nodes (4): fail(), isExcluded(), main(), normalizeSlash()

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (5): fail(), hasAuthMarkers(), main(), parseFunctionVerifyJwt(), readUtf8()

### Community 40 - "Community 40"
Cohesion: 0.6
Nodes (5): fail(), hasLikelyPhi(), isSortedBy(), main(), validatePack()

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (5): fail(), isSortedBy(), main(), parseArgs(), readJsonl()

### Community 42 - "Community 42"
Cohesion: 0.5
Nodes (2): firstEnv(), login()

### Community 43 - "Community 43"
Cohesion: 0.4
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 0.4
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 0.7
Nodes (4): buildStateStageSummary(), hasLikelyPhi(), normalizeStatePayload(), validateStatePayload()

### Community 46 - "Community 46"
Cohesion: 0.6
Nodes (3): buildCmsStageSummary(), normalizeCmsImportPayload(), stableJson()

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (2): assertEquals(), canonicalize()

### Community 48 - "Community 48"
Cohesion: 0.5
Nodes (2): Ensure-AuthUser(), Query-Scalar()

### Community 49 - "Community 49"
Cohesion: 0.7
Nodes (4): extractActiveRoutes(), fail(), main(), normalizePath()

### Community 50 - "Community 50"
Cohesion: 0.8
Nodes (4): fail(), getInputPath(), main(), readJson()

### Community 51 - "Community 51"
Cohesion: 0.8
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 52 - "Community 52"
Cohesion: 0.7
Nodes (4): fail(), lineFromIndex(), main(), walk()

### Community 53 - "Community 53"
Cohesion: 0.8
Nodes (4): assertBehavior(), fail(), main(), readUtf8()

### Community 54 - "Community 54"
Cohesion: 0.7
Nodes (4): fail(), isIssueLane(), main(), run()

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (4): fail(), main(), readUtf8(), requirePatterns()

### Community 56 - "Community 56"
Cohesion: 0.9
Nodes (4): fail(), main(), readJson(), requireKey()

### Community 57 - "Community 57"
Cohesion: 0.83
Nodes (3): extract_header_value(), fail(), main()

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (2): collectRoutablePaths(), joinRoutePath()

### Community 59 - "Community 59"
Cohesion: 0.5
Nodes (0): 

### Community 60 - "Community 60"
Cohesion: 0.5
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 0.83
Nodes (3): buildCentralizedExportPayload(), isRawIdentifierKey(), sanitizeForExport()

### Community 62 - "Community 62"
Cohesion: 0.83
Nodes (3): isAccreditorBody(), isBlank(), validateAccreditorAdapterContract()

### Community 63 - "Community 63"
Cohesion: 0.5
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 0.83
Nodes (3): isSensitiveKey(), redactLogValue(), redactString()

### Community 65 - "Community 65"
Cohesion: 0.83
Nodes (3): hashIdentifier(), normalizeActorRole(), writeEvidenceAuditEvent()

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (3): main(), normalizeUrl(), signIn()

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (2): fail(), main()

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (3): ensureStringArray(), fail(), main()

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (3): fail(), main(), readUtf8()

### Community 71 - "Community 71"
Cohesion: 0.83
Nodes (3): fail(), main(), parseArgs()

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (0): 

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (0): 

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (0): 

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (2): isBlank(), validateSourceGovernance()

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (0): 

### Community 82 - "Community 82"
Cohesion: 0.67
Nodes (0): 

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 0.67
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 0.67
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 0.67
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 0.67
Nodes (0): 

### Community 88 - "Community 88"
Cohesion: 0.67
Nodes (0): 

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (2): computeUrlHash(), main()

### Community 90 - "Community 90"
Cohesion: 0.67
Nodes (0): 

### Community 91 - "Community 91"
Cohesion: 0.67
Nodes (0): 

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (2): main(), runPack()

### Community 94 - "Community 94"
Cohesion: 0.67
Nodes (0): 

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (2): Ensure-Command(), Fail()

### Community 96 - "Community 96"
Cohesion: 0.67
Nodes (0): 

### Community 97 - "Community 97"
Cohesion: 0.67
Nodes (0): 

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (0): 

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (0): 

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (0): 

### Community 101 - "Community 101"
Cohesion: 1.0
Nodes (0): 

### Community 102 - "Community 102"
Cohesion: 1.0
Nodes (0): 

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (0): 

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (0): 

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (0): 

### Community 106 - "Community 106"
Cohesion: 1.0
Nodes (0): 

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (0): 

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (0): 

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (0): 

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (0): 

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (0): 

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (0): 

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (0): 

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (0): 

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (0): 

### Community 116 - "Community 116"
Cohesion: 1.0
Nodes (0): 

### Community 117 - "Community 117"
Cohesion: 1.0
Nodes (0): 

### Community 118 - "Community 118"
Cohesion: 1.0
Nodes (0): 

### Community 119 - "Community 119"
Cohesion: 1.0
Nodes (0): 

### Community 120 - "Community 120"
Cohesion: 1.0
Nodes (0): 

### Community 121 - "Community 121"
Cohesion: 1.0
Nodes (0): 

### Community 122 - "Community 122"
Cohesion: 1.0
Nodes (0): 

### Community 123 - "Community 123"
Cohesion: 1.0
Nodes (0): 

### Community 124 - "Community 124"
Cohesion: 1.0
Nodes (0): 

### Community 125 - "Community 125"
Cohesion: 1.0
Nodes (0): 

### Community 126 - "Community 126"
Cohesion: 1.0
Nodes (0): 

### Community 127 - "Community 127"
Cohesion: 1.0
Nodes (0): 

### Community 128 - "Community 128"
Cohesion: 1.0
Nodes (0): 

### Community 129 - "Community 129"
Cohesion: 1.0
Nodes (0): 

### Community 130 - "Community 130"
Cohesion: 1.0
Nodes (0): 

### Community 131 - "Community 131"
Cohesion: 1.0
Nodes (0): 

### Community 132 - "Community 132"
Cohesion: 1.0
Nodes (0): 

### Community 133 - "Community 133"
Cohesion: 1.0
Nodes (0): 

### Community 134 - "Community 134"
Cohesion: 1.0
Nodes (0): 

### Community 135 - "Community 135"
Cohesion: 1.0
Nodes (0): 

### Community 136 - "Community 136"
Cohesion: 1.0
Nodes (0): 

### Community 137 - "Community 137"
Cohesion: 1.0
Nodes (0): 

### Community 138 - "Community 138"
Cohesion: 1.0
Nodes (0): 

### Community 139 - "Community 139"
Cohesion: 1.0
Nodes (0): 

### Community 140 - "Community 140"
Cohesion: 1.0
Nodes (0): 

### Community 141 - "Community 141"
Cohesion: 1.0
Nodes (0): 

### Community 142 - "Community 142"
Cohesion: 1.0
Nodes (0): 

### Community 143 - "Community 143"
Cohesion: 1.0
Nodes (0): 

### Community 144 - "Community 144"
Cohesion: 1.0
Nodes (0): 

### Community 145 - "Community 145"
Cohesion: 1.0
Nodes (0): 

### Community 146 - "Community 146"
Cohesion: 1.0
Nodes (0): 

### Community 147 - "Community 147"
Cohesion: 1.0
Nodes (0): 

### Community 148 - "Community 148"
Cohesion: 1.0
Nodes (0): 

### Community 149 - "Community 149"
Cohesion: 1.0
Nodes (0): 

### Community 150 - "Community 150"
Cohesion: 1.0
Nodes (0): 

### Community 151 - "Community 151"
Cohesion: 1.0
Nodes (0): 

### Community 152 - "Community 152"
Cohesion: 1.0
Nodes (0): 

### Community 153 - "Community 153"
Cohesion: 1.0
Nodes (0): 

### Community 154 - "Community 154"
Cohesion: 1.0
Nodes (0): 

### Community 155 - "Community 155"
Cohesion: 1.0
Nodes (0): 

### Community 156 - "Community 156"
Cohesion: 1.0
Nodes (0): 

### Community 157 - "Community 157"
Cohesion: 1.0
Nodes (0): 

### Community 158 - "Community 158"
Cohesion: 1.0
Nodes (0): 

### Community 159 - "Community 159"
Cohesion: 1.0
Nodes (0): 

### Community 160 - "Community 160"
Cohesion: 1.0
Nodes (0): 

### Community 161 - "Community 161"
Cohesion: 1.0
Nodes (0): 

### Community 162 - "Community 162"
Cohesion: 1.0
Nodes (0): 

### Community 163 - "Community 163"
Cohesion: 1.0
Nodes (0): 

### Community 164 - "Community 164"
Cohesion: 1.0
Nodes (0): 

### Community 165 - "Community 165"
Cohesion: 1.0
Nodes (0): 

### Community 166 - "Community 166"
Cohesion: 1.0
Nodes (0): 

### Community 167 - "Community 167"
Cohesion: 1.0
Nodes (0): 

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (0): 

### Community 169 - "Community 169"
Cohesion: 1.0
Nodes (0): 

### Community 170 - "Community 170"
Cohesion: 1.0
Nodes (0): 

### Community 171 - "Community 171"
Cohesion: 1.0
Nodes (0): 

### Community 172 - "Community 172"
Cohesion: 1.0
Nodes (0): 

### Community 173 - "Community 173"
Cohesion: 1.0
Nodes (0): 

### Community 174 - "Community 174"
Cohesion: 1.0
Nodes (0): 

### Community 175 - "Community 175"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **Thin community `Community 98`** (2 nodes): `playwright.gate.config.ts`, `resolveEnvOrDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (2 nodes): `playwright.config.ts`, `resolveEnvOrDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (2 nodes): `photo-interaction.spec.ts`, `createTestImage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (2 nodes): `ImageAnnotator.tsx`, `ImageAnnotator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 102`** (2 nodes): `policy.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (2 nodes): `phase8-8-2-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (2 nodes): `log-redaction.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (2 nodes): `standards-source-governance.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (2 nodes): `publish-workflow.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (2 nodes): `phase8-8-6-state-integrity-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (2 nodes): `phase8-8-8-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (2 nodes): `issue502-full-role-crawl-matrix-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (2 nodes): `scoring-presentation.ts`, `mapScoreToCmsOutcome()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (2 nodes): `issue292-ai-quiz-draft-gate-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (2 nodes): `phase8-8-4-b-inputs-hash-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (2 nodes): `phase8-8-8-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 114`** (2 nodes): `runtime-selection.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (2 nodes): `tenant-isolation-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (2 nodes): `phase8-8-2-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (2 nodes): `phase8-8-9-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 118`** (2 nodes): `phase8-8-9-b-regeneration-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 119`** (2 nodes): `role-policy-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 120`** (2 nodes): `phase8-8-3-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 121`** (2 nodes): `phase8-8-5-b-version-resolution-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 122`** (2 nodes): `cms-2567-formatter.ts`, `formatCms2567()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 123`** (2 nodes): `phase8-8-6-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 124`** (2 nodes): `phase8-8-3-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 125`** (2 nodes): `issue501-report-citation-traceability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 126`** (2 nodes): `phase8-8-9-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 127`** (2 nodes): `issue301-recommendation-draft-gate-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 128`** (2 nodes): `issue300-video-analytics-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 129`** (2 nodes): `issue500-survey-scoring-finding-capa-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 130`** (2 nodes): `issue294-completion-immutability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 131`** (2 nodes): `issue293-training-assignments-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 132`** (2 nodes): `phase8-8-5-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 133`** (2 nodes): `issue295-export-service-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 134`** (2 nodes): `phase8-8-5-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 135`** (2 nodes): `export-service.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 136`** (2 nodes): `phase8-8-3-c-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 137`** (2 nodes): `phase8-8-9-a-version-binding-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 138`** (2 nodes): `phase8-8-4-a-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 139`** (2 nodes): `audit-emission-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 140`** (2 nodes): `phase8-8-4-a-methodology-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 141`** (2 nodes): `phase8-8-5-a-immutability-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 142`** (2 nodes): `phase8-8-10-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 143`** (2 nodes): `signed-url-policy.test.ts`, `assertEquals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 144`** (2 nodes): `phase8-8-4-b-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 145`** (2 nodes): `phase8-8-10-compliance-mode-validation.test.ts`, `assert()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (2 nodes): `prepare-local-supabase-env.ps1`, `Get-ValueFromStatus()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 147`** (2 nodes): `preflight.ps1`, `Fail()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 148`** (2 nodes): `check-survey-edge-function-contract.js`, `check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 149`** (2 nodes): `check-regulatory-seed-compat.js`, `check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 150`** (1 nodes): `tailwind.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 151`** (1 nodes): `playwright.staging.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 152`** (1 nodes): `playwright.production-readonly.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 153`** (1 nodes): `playwright.comprehensive.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 154`** (1 nodes): `playwright.seeded-staging.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 155`** (1 nodes): `playwright.interaction.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 156`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 157`** (1 nodes): `vitest.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 158`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 159`** (1 nodes): `debug-photo-upload.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 160`** (1 nodes): `staging-e2e.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 161`** (1 nodes): `staging-public-auth.contract.spec.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 162`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 163`** (1 nodes): `setup.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 164`** (1 nodes): `permissions.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 165`** (1 nodes): `scoring-presentation.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 166`** (1 nodes): `visit-pin-gate.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 167`** (1 nodes): `pre-survey-upload-contract.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `report-traceability.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 169`** (1 nodes): `check-standards-provenance-schema.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 170`** (1 nodes): `init-v1_1-scale-run.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 171`** (1 nodes): `recover-hosted-jwt-gateway.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 172`** (1 nodes): `seed-option3-full-local.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `seed-option3-clinical-richness.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 174`** (1 nodes): `gemini_watch.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 175`** (1 nodes): `bootstrap.ps1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SurveyOfflineStore` connect `Community 8` to `Community 3`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `handleVisitSurveyRoute()` (e.g. with `getReport()` and `saveReport()`) actually correct?**
  _`handleVisitSurveyRoute()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `setupTestUser()` and `runTest()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `main()` (e.g. with `parseArgs()` and `fail()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `resolveSeededRouteParams()` (e.g. with `requireSeededVisitId()` and `defaultVisitIdForTier()`) actually correct?**
  _`resolveSeededRouteParams()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.01 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._