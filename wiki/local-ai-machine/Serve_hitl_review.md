# Serve hitl review

> 10 nodes · cohesion 0.20

## Key Concepts

- **HITLHandler** (7 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **serve_hitl_review.py** (2 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **.do_POST()** (2 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **.do_GET()** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **.__init__()** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **.log_message()** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **main()** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **Handle POST /api/save-image-review — save one image's review state.** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **Serves the HITL HTML and proxies /images/ requests to local filesystem.** (1 connections) — `local-ai-machine/tools/serve_hitl_review.py`
- **SimpleHTTPRequestHandler** (1 connections)

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/tools/serve_hitl_review.py`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*