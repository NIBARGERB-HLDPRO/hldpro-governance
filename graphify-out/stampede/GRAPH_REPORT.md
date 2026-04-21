# Graph Report - /Users/bennibarger/Developer/HLDPRO/Stampede  (2026-04-20)

## Corpus Check
- Corpus is ~35,085 words - fits in a single context window. You may not need a graph.

## Summary
- 363 nodes · 555 edges · 59 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 239 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `main()` - 11 edges
2. `SimulationEngine` - 10 edges
3. `PersonaLoader` - 9 edges
4. `MockProvider` - 9 edges
5. `StampedeAggregator` - 9 edges
6. `scan_massive_minute_file()` - 9 edges
7. `probe_massive_flatfiles()` - 9 edges
8. `yfinance No-Key Prototype Fallback Provider` - 9 edges
9. `FixtureProvider` - 8 edges
10. `fail()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `30-Min SPY-Adjusted Abnormal Return Prediction Task` --conceptually_related_to--> `SimulationEngine`  [INFERRED]
  prompts/baseline_llm_v0_1.txt → hldpro-sim/hldprosim/engine.py
- `Issue #29 - Phase 0 Freeze Evidence Matrix PDCAR` --references--> `Phase 0 Freeze Evidence Matrix Config`  [EXTRACTED]
  docs/plans/issue-29-freeze-evidence-matrix-pdcar.md → scripts/validate_phase0_freeze_matrix.py
- `yfinance Live Lookback Run 2026-04-20 15:52:39` --demonstrates--> `yfinance No-Key Prototype Fallback Provider`  [EXTRACTED]
  cache/lookback-runs/yfinance-live-20260420155239/live/summary.md → docs/DATA_SOURCES.md
- `yfinance Live Lookback Run 2026-04-20 15:44:32` --demonstrates--> `yfinance No-Key Prototype Fallback Provider`  [EXTRACTED]
  cache/lookback-runs/yfinance-live-20260420154432/live/summary.md → docs/DATA_SOURCES.md
- `MockProvider` --uses--> `RunManifest`  [INFERRED]
  /Users/bennibarger/Developer/HLDPRO/Stampede/hldpro-sim/tests/test_stampede_consumer_proof.py → /Users/bennibarger/Developer/HLDPRO/Stampede/hldpro-sim/hldprosim/artifacts.py

## Hyperedges (group relationships)
- **Simulation Pipeline** — hldprosim_PersonaLoader, hldprosim_SimulationEngine, hldprosim_BaseProvider, hldprosim_Runner [EXTRACTED 0.95]
- **Provider Implementation Hierarchy** — hldprosim_BaseProvider, hldprosim_CodexCliProvider, hldprosim_AnthropicApiProvider, hldprosim_ClaudeCliProvider [INFERRED 0.85]
- **End-to-End Test Stack** — hldprosim_PersonaLoader, hldprosim_SimulationEngine, hldprosim_Runner, stampede_NarrativeAggregator, hldprosim_ArtifactWriter [EXTRACTED 1.00]
- **Lookback Validation Pipeline** — validate_phase0_lookback_tests, validate_phase0_lookback, validate_phase0_lookback_features, compute_features [EXTRACTED 1.00]
- **Provider Probe Validation Pipeline** — run_provider_endpoint_probes, validate_endpoint_probes, validate_endpoint_probe_report [EXTRACTED 1.00]
- **Simulation Feature Extraction Workflow** — run_slice6_simulation, compute_features, lookback_features [INFERRED 0.85]
- **Production Spec Requirements** — production_spec_v0_1_1, phase0_pass_criteria, abnormal_return_30m_label, leakage_audit, scramble_test, discriminator_gate [EXTRACTED 1.00]
- **yfinance Fallback and Lookback Testing Path** — run_phase0_lookback, yfinance_provider, lookback_smoke_fixture_run, yfinance_live_run_20260420155239, yfinance_live_run_20260420154432, microstructure_degradation [EXTRACTED 1.00]
- **Phase 0 Freeze Evidence Validation Chain** — validate_phase0_freeze_matrix, validate_phase0_freeze, freeze_evidence_matrix [EXTRACTED 1.00]
- **Paid Provider Freeze Gate Requirements** — polygon_massive_provider, intrinio_provider, phase0_freeze_evidence_matrix_doc [EXTRACTED 1.00]
- **Data Source A/B Selection Process** — polygon_massive_provider, intrinio_provider, phase0_ab_plan [EXTRACTED 1.00]
- **Model A/B Selection Process** — claude_cli_model, codex_cli_model, phase0_ab_plan [EXTRACTED 1.00]
- **Phase 0 Freeze Evidence Gating** — issue_29_freeze_evidence_matrix, issue_4_phase0_freeze_prep, phase0_freeze, freeze_evidence_matrix [EXTRACTED 1.00]
- **Model Bakeoff Candidate Selection** — claude_cli_model, codex_cli_model, issue_14_cli_model_bakeoff, baseline_llm_v0_1 [EXTRACTED 1.00]

## Communities

### Community 0 - "Simulation Core Package"
Cohesion: 0.05
Nodes (32): ABC, BaseAggregator, ArtifactWriter, RunManifest, BaseAggregator, BaseModel, SimulationEngine, PersonaLoader (+24 more)

### Community 1 - "Provider Endpoint Probes"
Cohesion: 0.16
Nodes (27): Issue #21 - Massive and Alpaca Endpoint Probes PDCAR, alpaca_request(), base_provider_entry(), build_decision(), build_report(), classify_http_error(), classify_rclone_error(), iso_z() (+19 more)

### Community 2 - "Data Source Evaluation"
Cohesion: 0.13
Nodes (22): Alpaca Public/Internal Provider, Data-Source Bakeoff Report, Phase 0 Data Sources Decision Document, Discriminator Access Decision, build_manifest(), decision(), env_key(), load_json() (+14 more)

### Community 3 - "Lookback Comparison"
Cohesion: 0.17
Nodes (20): by_event(), load_json(), load_jsonl(), main(), Issue #35 - Phase 0 Lookback Testable Framework PDCAR, Microstructure Degradation for yfinance, dataframe_to_bars(), display_path() (+12 more)

### Community 4 - "Provider Adapter Layer"
Cohesion: 0.16
Nodes (14): CorporateActionEvidence, normalize_corporate_action_evidence(), normalize_intrinio_bar(), normalize_polygon_bar(), NormalizedBar, Provider fixture normalization helpers for Phase 0., fail(), load() (+6 more)

### Community 5 - "Probe Report Validation"
Cohesion: 0.27
Nodes (15): fail(), main(), reject_secret_leaks(), selected(), validate_corporate_action_endpoint(), validate_decision(), validate_minute_endpoint(), validate_provider() (+7 more)

### Community 6 - "Phase 0 Spec Requirements"
Cohesion: 0.26
Nodes (13): Abnormal Return 30m Label Definition, Discriminator Classification Gate, Leakage Audit Procedure, Phase 0 Pass Criteria, Production Spec v0.1.1, Scramble Test Negative Control, fail(), load_json() (+5 more)

### Community 7 - "Feature Extraction"
Cohesion: 0.29
Nodes (10): compute_features function, by_minute(), compute_features(), pct(), Feature helpers for Phase 0 lookback smoke runs., returns(), sign_changes(), validate_bar_window() (+2 more)

### Community 8 - "Probe Report Emission"
Cohesion: 0.35
Nodes (10): build_provider_entry(), build_report(), decision(), env_key(), family_evidence(), load_json(), main(), missing_required_keys() (+2 more)

### Community 9 - "Freeze Evidence Validation"
Cohesion: 0.42
Nodes (10): Phase 0 Freeze Evidence Matrix Config, Issue #29 - Phase 0 Freeze Evidence Matrix PDCAR, fail(), load_json(), main(), require_set(), validate_family_mapping(), validate_matrix() (+2 more)

### Community 10 - "Provider Test Suite"
Cohesion: 0.2
Nodes (0):

### Community 11 - "Lookback Validation"
Cohesion: 0.58
Nodes (8): fail(), load_features(), load_json(), main(), reject_raw_payloads(), validate_features(), validate_partial_features(), walk()

### Community 12 - "Model Bakeoff Planning"
Cohesion: 0.25
Nodes (9): Claude CLI Primary Model, Codex CLI OpenAI Model, Phase 0 Implementation Plan, Issue #14 - CLI-Primary Model Bakeoff PDCAR, CLI-Primary Model Bakeoff Plan, Phase 0 Freeze Evidence Matrix Doc, Phase 0 Lookback Smoke Framework, STAMPEDE Phase 0 Progress Tracking (+1 more)

### Community 13 - "LLM Provider and Prompt"
Cohesion: 0.22
Nodes (9): 30-Min SPY-Adjusted Abnormal Return Prediction Task, Baseline LLM Prompt v0.1, AnthropicApiProvider, BaseProvider Protocol, ClaudeCliProvider, CodexCliProvider, PersonaLoader, Runner (+1 more)

### Community 14 - "Lookback Negative Tests"
Cohesion: 0.57
Nodes (7): copy_run(), expect_validator_failure(), fail(), load(), main(), run(), write()

### Community 15 - "Provider Probe Report Validation"
Cohesion: 0.57
Nodes (6): fail(), has_corporate_action_endpoint_pass(), main(), provider_has_required_passes(), selected_providers(), validate_freeze_decision()

### Community 16 - "Data Source Bakeoff Script"
Cohesion: 0.52
Nodes (6): build_report(), env_key_present(), env_keys_all_present(), load_config(), main(), provider_status()

### Community 17 - "Event Set Validation"
Cohesion: 0.73
Nodes (5): fail(), main(), parse_dt(), validate(), validate_event()

### Community 18 - "Provider Probes Validation"
Cohesion: 0.73
Nodes (5): fail(), main(), require_doc(), require_report_rejected(), run_report()

### Community 19 - "Data Source Bakeoff Validation"
Cohesion: 0.9
Nodes (4): fail(), load_json(), main(), require_doc()

### Community 20 - "Live Provider Bakeoff Validation"
Cohesion: 1.0
Nodes (3): fail(), main(), require_doc()

### Community 21 - "Freeze Matrix Negative Tests"
Cohesion: 0.83
Nodes (3): fail(), main(), require_rejected()

### Community 22 - "Runner Tests"
Cohesion: 0.67
Nodes (0):

### Community 23 - "Model Bakeoff Smoke"
Cohesion: 1.0
Nodes (2): load_json(), main()

### Community 24 - "Artifact Manifest Emission"
Cohesion: 1.0
Nodes (2): main(), sha256_file()

### Community 25 - "Lookback Candidate Validation"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 26 - "Candidate Freshness Validation"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 27 - "Validation Script Cluster"
Cohesion: 0.67
Nodes (3): emit_provider_probe_report, validate_live_provider_bakeoff, validate_provider_probe_report

### Community 28 - "Tradier Microstructure Path"
Cohesion: 0.67
Nodes (3): Endpoint Probe Runbook, Issue #25 - Tradier Real-Time Microstructure Path PDCAR, Tradier Real-time Microstructure Provider

### Community 29 - "Engine Tests"
Cohesion: 1.0
Nodes (0):

### Community 30 - "Artifact Tests"
Cohesion: 1.0
Nodes (0):

### Community 31 - "Candidate Template Emission"
Cohesion: 1.0
Nodes (0):

### Community 32 - "Aggregator Hierarchy"
Cohesion: 1.0
Nodes (2): BaseAggregator, NarrativeAggregator

### Community 33 - "Artifact Writer System"
Cohesion: 1.0
Nodes (2): ArtifactWriter, RunManifest

### Community 34 - "yfinance Freeze Constraint"
Cohesion: 1.0
Nodes (2): Freeze Not Ready Constraint for Non-Paid Providers, Phase 0 yfinance Live Lookback Run Summary

### Community 35 - "Event Set Lock"
Cohesion: 1.0
Nodes (2): Event Set Lock Plan, Locked 30-Event Corpus

### Community 36 - "Phase 0 Freeze Decision"
Cohesion: 1.0
Nodes (2): Issue #4 - Phase 0 Recovery and Freeze-Prep PDCAR, Phase 0 Freeze Decision

### Community 37 - "Personas Rationale 24"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

### Community 38 - "Script Model Bakeoff"
Cohesion: 1.0
Nodes (1): model_bakeoff_smoke

### Community 39 - "Script Validate Event Set"
Cohesion: 1.0
Nodes (1): validate_event_set_v0_1

### Community 40 - "Changelog V0 1 To V0 1 1"
Cohesion: 1.0
Nodes (1): CHANGELOG v0.1 to v0.1.1

### Community 41 - "Live Provider Probe Contract"
Cohesion: 1.0
Nodes (1): Live Provider Probe Contract

### Community 42 - "Lookback Smoke Fixture Run"
Cohesion: 1.0
Nodes (1): Phase 0 Lookback Smoke Fixture Run

### Community 43 - "Provider Failure Modes"
Cohesion: 1.0
Nodes (1): Provider Failure Modes Doc

### Community 44 - "Exception Register"
Cohesion: 1.0
Nodes (1): STAMPEDE Phase 0 Exception Register

### Community 45 - "Run Record Schema"
Cohesion: 1.0
Nodes (1): Phase 0 Run Record Schema

### Community 46 - "Live Run Commands"
Cohesion: 1.0
Nodes (1): Live Run Commands

### Community 47 - "Phase0 Ab Plan"
Cohesion: 1.0
Nodes (1): Phase 0 A/B Plan

### Community 48 - "Solo Maintainer Merge Policy"
Cohesion: 1.0
Nodes (1): Solo Maintainer Merge Policy

### Community 49 - "Issue 27 Corporate Actions"
Cohesion: 1.0
Nodes (1): Issue #27 - Corporate-Action Evidence Contract PDCAR

### Community 50 - "Issue 39 Yfinance Missing Data"
Cohesion: 1.0
Nodes (1): Issue #39 - Live yfinance Missing-Data Evidence PDCAR

### Community 51 - "Issue 33 Solo Maintainer"
Cohesion: 1.0
Nodes (1): Issue #33 - Solo-Maintainer Auto-Merge Policy PDCAR

### Community 52 - "Issue 46 Yfinance Evidence Index"
Cohesion: 1.0
Nodes (1): Issue #46 - yfinance Evidence Index PDCAR

### Community 53 - "Issue 16 Public Data Path"
Cohesion: 1.0
Nodes (1): Issue #16 - Public/Internal Data Path PDCAR

### Community 54 - "Issue 41 Live Lookback Preflight"
Cohesion: 1.0
Nodes (1): Issue #41 - Live Lookback Runtime Preflight Checks PDCAR

### Community 55 - "Issue 23 Massive Event Window"
Cohesion: 1.0
Nodes (1): Issue #23 - Massive Event-Window Minute Bars PDCAR

### Community 56 - "Issue 18 Live Provider Probes"
Cohesion: 1.0
Nodes (1): Issue #18 - Live Provider Probe Scaffold PDCAR

### Community 57 - "Issue 37 Lookback Hardening"
Cohesion: 1.0
Nodes (1): Issue #37 - Phase 0 Lookback Hardening PDCAR

### Community 58 - "Issue 43 Yfinance Benchmark"
Cohesion: 1.0
Nodes (1): Issue #43 - yfinance SPY Benchmark PDCAR

## Knowledge Gaps
- **63 isolated node(s):** `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.`, `Cloud stub — not implemented until API keys are provisioned.`, `Feature helpers for Phase 0 lookback smoke runs.` (+58 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Engine Tests`** (2 nodes): `test_engine.py`, `test_engine_passes_template_results_to_provider()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Artifact Tests`** (2 nodes): `test_artifacts.py`, `test_artifact_writer_writes_manifest_and_outcomes()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Candidate Template Emission`** (2 nodes): `emit_yfinance_candidate_template.py`, `main()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Aggregator Hierarchy`** (2 nodes): `BaseAggregator`, `NarrativeAggregator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Artifact Writer System`** (2 nodes): `ArtifactWriter`, `RunManifest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `yfinance Freeze Constraint`** (2 nodes): `Freeze Not Ready Constraint for Non-Paid Providers`, `Phase 0 yfinance Live Lookback Run Summary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Event Set Lock`** (2 nodes): `Event Set Lock Plan`, `Locked 30-Event Corpus`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase 0 Freeze Decision`** (2 nodes): `Issue #4 - Phase 0 Recovery and Freeze-Prep PDCAR`, `Phase 0 Freeze Decision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Personas Rationale 24`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Script Model Bakeoff`** (1 nodes): `model_bakeoff_smoke`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Script Validate Event Set`** (1 nodes): `validate_event_set_v0_1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Changelog V0 1 To V0 1 1`** (1 nodes): `CHANGELOG v0.1 to v0.1.1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Live Provider Probe Contract`** (1 nodes): `Live Provider Probe Contract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Lookback Smoke Fixture Run`** (1 nodes): `Phase 0 Lookback Smoke Fixture Run`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Failure Modes`** (1 nodes): `Provider Failure Modes Doc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Exception Register`** (1 nodes): `STAMPEDE Phase 0 Exception Register`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Run Record Schema`** (1 nodes): `Phase 0 Run Record Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Live Run Commands`** (1 nodes): `Live Run Commands`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase0 Ab Plan`** (1 nodes): `Phase 0 A/B Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Solo Maintainer Merge Policy`** (1 nodes): `Solo Maintainer Merge Policy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 27 Corporate Actions`** (1 nodes): `Issue #27 - Corporate-Action Evidence Contract PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 39 Yfinance Missing Data`** (1 nodes): `Issue #39 - Live yfinance Missing-Data Evidence PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 33 Solo Maintainer`** (1 nodes): `Issue #33 - Solo-Maintainer Auto-Merge Policy PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 46 Yfinance Evidence Index`** (1 nodes): `Issue #46 - yfinance Evidence Index PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 16 Public Data Path`** (1 nodes): `Issue #16 - Public/Internal Data Path PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 41 Live Lookback Preflight`** (1 nodes): `Issue #41 - Live Lookback Runtime Preflight Checks PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 23 Massive Event Window`** (1 nodes): `Issue #23 - Massive Event-Window Minute Bars PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 18 Live Provider Probes`** (1 nodes): `Issue #18 - Live Provider Probe Scaffold PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 37 Lookback Hardening`** (1 nodes): `Issue #37 - Phase 0 Lookback Hardening PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Issue 43 Yfinance Benchmark`** (1 nodes): `Issue #43 - yfinance SPY Benchmark PDCAR`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `yfinance No-Key Prototype Fallback Provider` connect `Data Source Evaluation` to `Lookback Comparison`, `Model Bakeoff Planning`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `main()` (e.g. with `load_json()` and `load_live_yfinance_events()`) actually correct?**
  _`main()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SimulationEngine` (e.g. with `Runner` and `PersonaLoader`) actually correct?**
  _`SimulationEngine` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PersonaLoader` (e.g. with `SimulationEngine` and `MockProvider`) actually correct?**
  _`PersonaLoader` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `MockProvider` (e.g. with `test_stampede_e2e()` and `ArtifactWriter`) actually correct?**
  _`MockProvider` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `StampedeAggregator` (e.g. with `run_simulation()` and `BaseAggregator`) actually correct?**
  _`StampedeAggregator` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Load persona JSON files. Resolves local-first, shared fallback.`, `Convenience: load shared dir from bundled package personas/.`, `Subprocess-backed provider using codex exec --ephemeral.` to the rest of the system?**
  _63 weakly-connected nodes found - possible documentation gaps or missing edges._