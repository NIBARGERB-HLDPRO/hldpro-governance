# Ops Generate ai draft report

> 26 nodes · cohesion 0.12

## Key Concepts

- **generate_ai_draft_report.py** (14 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **main()** (12 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **load_findings_from_state()** (7 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **_call_claude()** (6 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **generate_ai_narratives()** (6 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **generate_html()** (5 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **load_narratives_from_file()** (5 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **assemble_report()** (4 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **generate_docx()** (4 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **load_findings_from_api()** (4 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **generate_placeholder_narratives()** (3 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **load_dotenv()** (3 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **_strip_reasoning_leakage()** (3 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **_call_openai()** (2 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **parse_args()** (2 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Load findings from the survey API (stub — falls back to local data).** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Load pre-generated AI narratives from a JSON file.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Remove LLM reasoning preamble that leaks into generated output.      Catches pat** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Call Claude through the governed CLI supervisor and return the text response.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Call OpenAI API and return the text response.      STUB — not yet implemented. U** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Make 3 Claude API calls to generate report narratives.      Returns dict with ke** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Generate placeholder text for --no-ai mode.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Assemble all report data into a single dict.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Generate DOCX report matching Pinecroft Final Report format.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- **Load findings from state file. Falls back to Pinecroft data module.** (1 connections) — `local-ai-machine/scripts/ops/generate_ai_draft_report.py`
- *... and 1 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `local-ai-machine/scripts/ops/generate_ai_draft_report.py`

## Audit Trail

- EXTRACTED: 76 (84%)
- INFERRED: 15 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*