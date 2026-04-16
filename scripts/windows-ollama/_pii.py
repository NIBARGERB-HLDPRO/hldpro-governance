#!/usr/bin/env python3
"""
Shared PII utilities for Windows-Ollama scripts.

Used by both decide.sh (via an embedded Python call) and submit.py so
pattern matching behavior is consistent across routing and submission paths.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency optional in tooling image
    raise ImportError(
        "PyYAML is required for PII pattern loading. Install with `pip install pyyaml`."
    ) from exc


_BUILTIN_PATTERNS = {
    "ssn": r"(?:\d{3}-\d{2}-\d{4}|\d{9})",
    "phone": r"(?:\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "dob": r"(?:0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](19|20)\d{2}",
    "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "field_marker": r"(?:ssn|social|phone|dob|date.?of.?birth|credit|password|api.?key)\s*[:=]",
}


def load_pii_patterns(patterns_file: str) -> Dict[str, Dict[str, Any]]:
    """Load and validate pii patterns from pii_patterns.yml."""
    patterns_path = Path(patterns_file)
    if not patterns_path.exists():
        raise FileNotFoundError(f"pii_patterns.yml not found at {patterns_path}")

    with open(patterns_path) as f:
        try:
            data = yaml.safe_load(f)
        except Exception as exc:
            raise ValueError(f"Failed to parse pii_patterns.yml: {exc}") from exc

    patterns = data.get("patterns") if isinstance(data, dict) else None
    if not isinstance(patterns, dict):
        raise ValueError("Invalid pii_patterns.yml structure: missing top-level `patterns` mapping")

    normalized: Dict[str, Dict[str, Any]] = {}
    for pattern_name, cfg in patterns.items():
        if not isinstance(pattern_name, str) or not isinstance(cfg, dict):
            continue
        regex = cfg.get("regex")
        if isinstance(regex, str) and regex.strip():
            normalized[pattern_name] = cfg

    if not normalized:
        raise ValueError("No valid regex patterns found in pii_patterns.yml")

    return normalized


def _iter_patterns(patterns: Dict[str, Dict[str, Any]]):
    for pattern_name, cfg in patterns.items():
        regex = cfg.get("regex")
        if not isinstance(regex, str) or not regex.strip():
            continue
        flags = cfg.get("flags", "")
        re_flags = re.IGNORECASE if (isinstance(flags, str) and "i" in flags.lower()) else 0
        yield pattern_name, regex, re_flags


def detect_pii(text: str, patterns: Dict[str, Dict[str, Any]]) -> Optional[str]:
    """
    Scan text for PII patterns from YAML patterns.

    Falls back to the previous built-in patterns if a loaded pattern is malformed.
    """
    if not text:
        return None

    for pattern_name, regex, flags in _iter_patterns(patterns):
        try:
            if re.search(regex, text, flags):
                return pattern_name
        except re.error:
            continue

    # Backward-compatible fallback for environments that omit flags/metadata.
    for pattern_name, regex in _BUILTIN_PATTERNS.items():
        try:
            if re.search(regex, text, re.IGNORECASE):
                return pattern_name
        except re.error:
            continue

    return None

