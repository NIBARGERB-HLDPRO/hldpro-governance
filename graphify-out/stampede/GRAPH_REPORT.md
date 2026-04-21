# Graph Report - stampede  (2026-04-21)

## Corpus Check
- 115 files · ~51,929 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 466 nodes · 913 edges · 34 communities detected
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 178 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Hldpro sim Hldprosim Providers|Hldpro sim Hldprosim Providers]]
- [[_COMMUNITY_Tradier provider Compute|Tradier provider Compute]]
- [[_COMMUNITY_Hldpro sim Hldprosim Stampede|Hldpro sim Hldprosim Stampede]]
- [[_COMMUNITY_Run provider endpoint probes|Run provider endpoint probes]]
- [[_COMMUNITY_Validate endpoint probes Provider|Validate endpoint probes Provider]]
- [[_COMMUNITY_Tradier executor Run|Tradier executor Run]]
- [[_COMMUNITY_Event corpus Gdelt|Event corpus Gdelt]]
- [[_COMMUNITY_Provider adapters Validate|Provider adapters Validate]]
- [[_COMMUNITY_Run forward validation|Run forward validation]]
- [[_COMMUNITY_Event trigger Parse|Event trigger Parse]]
- [[_COMMUNITY_Run phase0 lookback|Run phase0 lookback]]
- [[_COMMUNITY_Run seed stability|Run seed stability]]
- [[_COMMUNITY_Emit source manifest|Emit source manifest]]
- [[_COMMUNITY_Validate endpoint report|Validate endpoint report]]
- [[_COMMUNITY_Emit provider report|Emit provider report]]
- [[_COMMUNITY_Lookback features Validate|Lookback features Validate]]
- [[_COMMUNITY_Validate phase0 lookback|Validate phase0 lookback]]
- [[_COMMUNITY_Validate phase0 freeze matrix|Validate phase0 freeze matrix]]
- [[_COMMUNITY_Validate phase0 lookback|Validate phase0 lookback]]
- [[_COMMUNITY_Append yfinance candidates|Append yfinance candidates]]
- [[_COMMUNITY_Validate phase0 freeze|Validate phase0 freeze]]
- [[_COMMUNITY_Phase0 source bakeoff|Phase0 source bakeoff]]
- [[_COMMUNITY_Validate provider report|Validate provider report]]
- [[_COMMUNITY_Validate event set v0 1|Validate event set v0 1]]
- [[_COMMUNITY_Run backtest Packet|Run backtest Packet]]
- [[_COMMUNITY_Validate paper trade run|Validate paper trade run]]
- [[_COMMUNITY_Validate phase0 lookback candidate freshness|Validate phase0 lookback candidate freshness]]
- [[_COMMUNITY_Emit lookback artifact manifest|Emit lookback artifact manifest]]
- [[_COMMUNITY_Validate phase0 lookback candidate|Validate phase0 lookback candidate]]
- [[_COMMUNITY_Validate event trigger|Validate event trigger]]
- [[_COMMUNITY_Validate phase1 Number|Validate phase1 Number]]
- [[_COMMUNITY_Emit yfinance candidate template|Emit yfinance candidate template]]
- [[_COMMUNITY_Tradier executor|Tradier executor]]
- [[_COMMUNITY_Hldpro sim Hldprosim Personas|Hldpro sim Hldprosim Personas]]

## God Nodes (most connected - your core abstractions)
1. `TradierProvider` - 29 edges
2. `PersonaLoader` - 18 edges
3. `SimulationEngine` - 16 edges
4. `cmd_predict()` - 15 edges
5. `main()` - 13 edges
6. `AnthropicApiProvider` - 13 edges
7. `main()` - 12 edges
8. `CodexCliProvider` - 12 edges
9. `StampedeAggregator` - 11 edges
10. `test_stampede_e2e()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `test_stampede_e2e()` --calls--> `aggregate()`  [INFERRED]
  stampede/hldpro-sim/tests/test_stampede_consumer_proof.py → stampede/hldpro-sim/hldprosim/aggregator.py
- `build_v4_packet()` --calls--> `compute_features()`  [INFERRED]
  stampede/scripts/run_forward_validation.py → stampede/scripts/lookback_features.py
- `cmd_predict()` --calls--> `AnthropicApiProvider`  [INFERRED]
  stampede/scripts/run_forward_validation.py → stampede/hldpro-sim/hldprosim/providers.py
- `cmd_predict()` --calls--> `PersonaLoader`  [INFERRED]
  stampede/scripts/run_forward_validation.py → stampede/hldpro-sim/hldprosim/personas.py
- `cmd_predict()` --calls--> `SimulationEngine`  [INFERRED]
  stampede/scripts/run_forward_validation.py → stampede/hldpro-sim/hldprosim/engine.py

## Communities

### Community 0 - "Hldpro sim Hldprosim Providers"
Cohesion: 0.06
Nodes (45): ABC, aggregate(), BaseAggregator, BaseAggregator, SimulationEngine, load_json(), main(), PersonaLoader (+37 more)

### Community 1 - "Tradier provider Compute"
Cohesion: 0.07
Nodes (34): cache_key(), compute_beta(), compute_label(), fetch_bars_cached(), fetch_daily_cached(), main(), parse_t0(), process_event() (+26 more)

### Community 2 - "Hldpro sim Hldprosim Stampede"
Cohesion: 0.11
Nodes (15): ArtifactWriter, RunManifest, BaseModel, load_json(), main(), Runner, load_json(), main() (+7 more)

### Community 3 - "Run provider endpoint probes"
Cohesion: 0.17
Nodes (26): alpaca_request(), base_provider_entry(), build_decision(), build_report(), classify_http_error(), classify_rclone_error(), iso_z(), load_json() (+18 more)

### Community 4 - "Validate endpoint probes Provider"
Cohesion: 0.15
Nodes (20): fail(), load_json(), main(), require_doc(), fail(), main(), require_report_rejected(), require_runner_rejected() (+12 more)

### Community 5 - "Tradier executor Run"
Cohesion: 0.12
Nodes (15): aggregate(), build_packet(), call_llm(), _compute_5m_signals(), _fetch_bars(), main(), run_live_inference(), _count_logged_entries() (+7 more)

### Community 6 - "Event corpus Gdelt"
Cohesion: 0.2
Nodes (22): assign_bucket(), av_get(), build_corpus(), cache_get(), cache_put(), classify(), edgar_get(), fetch_edgar_earnings() (+14 more)

### Community 7 - "Provider adapters Validate"
Cohesion: 0.24
Nodes (15): classify_error(), CorporateActionEvidence, has_corporate_action_reference(), has_quote_or_trade_capability(), normalize_corporate_action_evidence(), normalize_intrinio_bar(), normalize_polygon_bar(), NormalizedBar (+7 more)

### Community 8 - "Run forward validation"
Cohesion: 0.28
Nodes (14): build_v4_packet(), cmd_actuals(), cmd_predict(), cmd_summary(), _extract_bars(), fetch_live_event_data(), load_events(), load_results() (+6 more)

### Community 9 - "Event trigger Parse"
Cohesion: 0.26
Nodes (13): fetch_route(), find_child_text(), is_market_open(), iter_items(), load_watchlist(), main(), make_event_id(), parse_datetime() (+5 more)

### Community 10 - "Run phase0 lookback"
Cohesion: 0.28
Nodes (14): dataframe_to_bars(), display_path(), fail_live_preflight(), git_commit(), iso_z(), load_json(), load_live_yfinance_events(), main() (+6 more)

### Community 11 - "Run seed stability"
Cohesion: 0.24
Nodes (12): compute_overall_metrics(), compute_per_event_metrics(), load_cache_bakeoff(), load_results_file(), main(), print_report(), Return synthetic multi-seed records by jittering base predictions., Group records by (event_id, persona_id) and compute stability stats. (+4 more)

### Community 12 - "Emit source manifest"
Cohesion: 0.26
Nodes (11): by_event(), load_json(), load_jsonl(), main(), build_manifest(), decision(), env_key(), load_json() (+3 more)

### Community 13 - "Validate endpoint report"
Cohesion: 0.45
Nodes (10): fail(), main(), reject_secret_leaks(), selected(), validate_corporate_action_endpoint(), validate_decision(), validate_minute_endpoint(), validate_provider() (+2 more)

### Community 14 - "Emit provider report"
Cohesion: 0.35
Nodes (10): build_provider_entry(), build_report(), decision(), env_key(), family_evidence(), load_json(), main(), missing_required_keys() (+2 more)

### Community 15 - "Lookback features Validate"
Cohesion: 0.33
Nodes (9): by_minute(), compute_features(), pct(), Feature helpers for Phase 0 lookback smoke runs., returns(), sign_changes(), validate_bar_window(), fail() (+1 more)

### Community 16 - "Validate phase0 lookback"
Cohesion: 0.58
Nodes (8): fail(), load_features(), load_json(), main(), reject_raw_payloads(), validate_features(), validate_partial_features(), walk()

### Community 17 - "Validate phase0 freeze matrix"
Cohesion: 0.58
Nodes (8): fail(), load_json(), main(), require_set(), validate_family_mapping(), validate_matrix(), validate_negative_controls(), validate_reports()

### Community 18 - "Validate phase0 lookback"
Cohesion: 0.57
Nodes (7): copy_run(), expect_validator_failure(), fail(), load(), main(), run(), write()

### Community 19 - "Append yfinance candidates"
Cohesion: 0.43
Nodes (7): _bump_version(), fail(), main(), _max_candidate_number(), Return the highest NNN from any yf_candidate_NNN event_id, or 0 if none., Increment the minor version number in a 'vMAJOR.MINOR' string., validate_new_event()

### Community 20 - "Validate phase0 freeze"
Cohesion: 0.64
Nodes (7): fail(), load_json(), load_yaml(), main(), require_doc(), require_families(), require_locked_v01()

### Community 21 - "Phase0 source bakeoff"
Cohesion: 0.52
Nodes (6): build_report(), env_key_present(), env_keys_all_present(), load_config(), main(), provider_status()

### Community 22 - "Validate provider report"
Cohesion: 0.57
Nodes (6): fail(), has_corporate_action_endpoint_pass(), main(), provider_has_required_passes(), selected_providers(), validate_freeze_decision()

### Community 23 - "Validate event set v0 1"
Cohesion: 0.73
Nodes (5): fail(), main(), parse_dt(), validate(), validate_event()

### Community 24 - "Run backtest Packet"
Cohesion: 0.47
Nodes (5): build_packet(), call_llm(), main(), run_backtest.py  Runs LLM predictions against 27 real historical events with rea, Build event packet for the prompt from real data.

### Community 25 - "Validate paper trade run"
Cohesion: 0.83
Nodes (3): _actual_direction(), _load_entries(), main()

### Community 26 - "Validate phase0 lookback candidate freshness"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 27 - "Emit lookback artifact manifest"
Cohesion: 1.0
Nodes (2): main(), sha256_file()

### Community 28 - "Validate phase0 lookback candidate"
Cohesion: 1.0
Nodes (2): fail(), main()

### Community 29 - "Validate event trigger"
Cohesion: 1.0
Nodes (2): main(), validate()

### Community 30 - "Validate phase1 Number"
Cohesion: 1.0
Nodes (2): is_number(), main()

### Community 31 - "Emit yfinance candidate template"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Tradier executor"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Hldpro sim Hldprosim Personas"
Cohesion: 1.0
Nodes (1): Convenience: load shared dir from bundled package personas/.

## Knowledge Gaps
- **26 isolated node(s):** `build_event_corpus.py  (v4 — EDGAR + GDELT primary)  Discovery pipeline:   EDGAR`, `8-K Item 2.02 filings → {(ticker, t0_date): event_dict}`, `Fetch genuine Tesla corporate events from GDELT (IR/official sources).`, `Use GDELT to fill bucket gaps after EDGAR.`, `Load JSONL or JSON multi-seed results from path.` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Emit yfinance candidate template`** (2 nodes): `main()`, `emit_yfinance_candidate_template.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tradier executor`** (1 nodes): `test_tradier_executor.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hldpro sim Hldprosim Personas`** (1 nodes): `Convenience: load shared dir from bundled package personas/.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_stampede_e2e()` connect `Hldpro sim Hldprosim Stampede` to `Hldpro sim Hldprosim Providers`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `TradierProvider` connect `Tradier provider Compute` to `Tradier executor Run`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `PersonaLoader` connect `Hldpro sim Hldprosim Providers` to `Run forward validation`, `Hldpro sim Hldprosim Stampede`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `TradierProvider` (e.g. with `TestTradierProviderInit` and `TestFetchMinuteBars`) actually correct?**
  _`TradierProvider` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `PersonaLoader` (e.g. with `SimpleAggregator` and `Live forward validation runner for Stampede Phase 0, issue #78.`) actually correct?**
  _`PersonaLoader` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `SimulationEngine` (e.g. with `SimpleAggregator` and `Live forward validation runner for Stampede Phase 0, issue #78.`) actually correct?**
  _`SimulationEngine` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `cmd_predict()` (e.g. with `AnthropicApiProvider` and `PersonaLoader`) actually correct?**
  _`cmd_predict()` has 4 INFERRED edges - model-reasoned connections that need verification._