# Tradier provider Compute

> 51 nodes · cohesion 0.07

## Key Concepts

- **TradierProvider** (29 connections) — `stampede/scripts/tradier_provider.py`
- **compute_actuals.py** (9 connections) — `stampede/scripts/compute_actuals.py`
- **.fetch_minute_bars()** (8 connections) — `stampede/scripts/tradier_provider.py`
- **process_event()** (7 connections) — `stampede/scripts/compute_actuals.py`
- **run_cross_source_validation.py** (7 connections) — `stampede/scripts/run_cross_source_validation.py`
- **enrich()** (6 connections) — `stampede/scripts/enrich_paper_trade_outcomes.py`
- **run_validation()** (6 connections) — `stampede/scripts/run_cross_source_validation.py`
- **.fetch_daily_bars()** (6 connections) — `stampede/scripts/tradier_provider.py`
- **test_tradier_provider.py** (5 connections) — `stampede/scripts/test_tradier_provider.py`
- **TestFetchMinuteBars** (5 connections) — `stampede/scripts/test_tradier_provider.py`
- **.fetch_quote()** (5 connections) — `stampede/scripts/tradier_provider.py`
- **fetch_bars_cached()** (4 connections) — `stampede/scripts/compute_actuals.py`
- **get_tradier_daily_close()** (4 connections) — `stampede/scripts/run_cross_source_validation.py`
- **.test_returns_sorted_relative_bars()** (4 connections) — `stampede/scripts/test_tradier_provider.py`
- **TestTradierProviderInit** (4 connections) — `stampede/scripts/test_tradier_provider.py`
- **._headers()** (4 connections) — `stampede/scripts/tradier_provider.py`
- **compute_beta()** (3 connections) — `stampede/scripts/compute_actuals.py`
- **compute_label()** (3 connections) — `stampede/scripts/compute_actuals.py`
- **fetch_daily_cached()** (3 connections) — `stampede/scripts/compute_actuals.py`
- **main()** (3 connections) — `stampede/scripts/compute_actuals.py`
- **parse_t0()** (3 connections) — `stampede/scripts/compute_actuals.py`
- **_find_closest()** (3 connections) — `stampede/scripts/enrich_paper_trade_outcomes.py`
- **enrich_paper_trade_outcomes.py** (3 connections) — `stampede/scripts/enrich_paper_trade_outcomes.py`
- **TestFetchDailyBars** (3 connections) — `stampede/scripts/test_tradier_provider.py`
- **.test_returns_daily_list()** (3 connections) — `stampede/scripts/test_tradier_provider.py`
- *... and 26 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `stampede/scripts/compute_actuals.py`
- `stampede/scripts/enrich_paper_trade_outcomes.py`
- `stampede/scripts/run_cross_source_validation.py`
- `stampede/scripts/test_tradier_provider.py`
- `stampede/scripts/tradier_provider.py`

## Audit Trail

- EXTRACTED: 128 (68%)
- INFERRED: 61 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*