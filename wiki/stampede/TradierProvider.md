# TradierProvider

> God node · 29 connections · `stampede/scripts/tradier_provider.py`

## Connections by Relation

### calls
- [[run_paper_trade()]] `INFERRED`
- [[enrich()]] `INFERRED`
- [[.test_returns_sorted_relative_bars()]] `INFERRED`
- [[get_tradier_daily_close()]] `INFERRED`
- [[_fetch_bars()]] `INFERRED`
- [[.test_single_bar_dict_response()]] `INFERRED`
- [[.test_returns_daily_list()]] `INFERRED`
- [[.test_returns_quote()]] `INFERRED`
- [[main()]] `INFERRED`
- [[.test_init_ok()]] `INFERRED`
- [[.test_init_missing_token()]] `INFERRED`

### contains
- [[tradier_provider.py]] `EXTRACTED`

### method
- [[.fetch_minute_bars()]] `EXTRACTED`
- [[.fetch_daily_bars()]] `EXTRACTED`
- [[.fetch_quote()]] `EXTRACTED`
- [[._headers()]] `EXTRACTED`
- [[.__init__()]] `EXTRACTED`

### rationale_for
- [[Fetches 1-min bars and daily bars from Tradier production API.]] `EXTRACTED`

### uses
- [[TestFetchMinuteBars]] `INFERRED`
- [[TestTradierProviderInit]] `INFERRED`
- [[TestFetchDailyBars]] `INFERRED`
- [[TestFetchQuote]] `INFERRED`
- [[Unit tests for TradierProvider using recorded fixture responses.]] `INFERRED`
- [[Daily bar cross-source validation: Tradier (primary) vs yfinance (tertiary).  Pe]] `INFERRED`
- [[Return the close price of the bar whose relative_minute is closest to target.]] `INFERRED`
- [[compute_actuals.py  Computes real abnormal_return_30m_bps for each event in the]] `INFERRED`
- [[Parse ISO 8601 event_timestamp → aware datetime in ET.]] `INFERRED`
- [[Rolling OLS beta: cov(r_ticker, r_spy) / var(r_spy). Returns (beta, n_obs).]] `INFERRED`
- [[Compute abnormal_return_30m_bps from bar lists.     Returns (value_bps, None) or]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*