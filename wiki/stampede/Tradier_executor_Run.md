# Tradier executor Run

> 26 nodes · cohesion 0.12

## Key Concepts

- **run_paper_trade()** (9 connections) — `stampede/scripts/run_paper_trade.py`
- **run_live_inference()** (8 connections) — `stampede/scripts/run_inference_live.py`
- **run_inference_live.py** (7 connections) — `stampede/scripts/run_inference_live.py`
- **TradierExecutor** (7 connections) — `stampede/scripts/tradier_executor.py`
- **.place_order()** (7 connections) — `stampede/scripts/tradier_executor.py`
- **KillSwitch** (6 connections) — `stampede/scripts/tradier_executor.py`
- **run_paper_trade.py** (4 connections) — `stampede/scripts/run_paper_trade.py`
- **build_packet()** (4 connections) — `stampede/scripts/run_inference_live.py`
- **_fetch_bars()** (4 connections) — `stampede/scripts/run_inference_live.py`
- **main()** (3 connections) — `stampede/scripts/run_inference_live.py`
- **main()** (3 connections) — `stampede/scripts/run_paper_trade.py`
- **_print_status()** (3 connections) — `stampede/scripts/run_paper_trade.py`
- **tradier_executor.py** (2 connections) — `stampede/scripts/tradier_executor.py`
- **aggregate()** (2 connections) — `stampede/scripts/run_inference_live.py`
- **call_llm()** (2 connections) — `stampede/scripts/run_inference_live.py`
- **_compute_5m_signals()** (2 connections) — `stampede/scripts/run_inference_live.py`
- **_count_logged_entries()** (2 connections) — `stampede/scripts/run_paper_trade.py`
- **.close_position()** (2 connections) — `stampede/scripts/tradier_executor.py`
- **._ensure_orders_dir()** (2 connections) — `stampede/scripts/tradier_executor.py`
- **._skip()** (2 connections) — `stampede/scripts/tradier_executor.py`
- **.check_consecutive()** (1 connections) — `stampede/scripts/tradier_executor.py`
- **.check_daily()** (1 connections) — `stampede/scripts/tradier_executor.py`
- **.check_per_event()** (1 connections) — `stampede/scripts/tradier_executor.py`
- **Simple risk limits used to decide when to pause execution.** (1 connections) — `stampede/scripts/tradier_executor.py`
- **signal: event_id, ticker, signal_direction, signal_magnitude_bps, last_price (op** (1 connections) — `stampede/scripts/tradier_executor.py`
- *... and 1 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `stampede/scripts/run_inference_live.py`
- `stampede/scripts/run_paper_trade.py`
- `stampede/scripts/tradier_executor.py`

## Audit Trail

- EXTRACTED: 72 (83%)
- INFERRED: 15 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*