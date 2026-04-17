# Windows ollama Audit

> 21 nodes · cohesion 0.13

## Key Concepts

- **audit.py** (7 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **.write_entry()** (7 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._write_manifest()** (7 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._get_prev_hash()** (6 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._get_today_path()** (5 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._read_last_entry()** (5 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **canonical_json()** (5 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._get_next_seq()** (4 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **compute_entry_hmac()** (4 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **compute_sha256()** (4 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **._get_today_manifest_path()** (3 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Write an audit entry. Returns True if successful, False otherwise.          Args** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Return canonical JSON for HMAC computation.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Write or update today's manifest.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Compute SHA256 hash of bytes.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Compute HMAC-SHA256 over canonical JSON of entry (without entry_hmac field).** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Return path to today's audit log.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Return path to today's manifest.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Read the last entry from today's log, or None if file doesn't exist.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Get next sequence number for today.** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`
- **Get previous entry's hash (or zero for seq=0).** (1 connections) — `hldpro-governance/scripts/windows-ollama/audit.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `hldpro-governance/scripts/windows-ollama/audit.py`

## Audit Trail

- EXTRACTED: 37 (55%)
- INFERRED: 30 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*