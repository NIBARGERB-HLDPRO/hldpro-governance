#!/bin/bash
# check-errors.sh - local FAIL_FAST_LOG and ERROR_PATTERNS schema gate
# Usage: ./hooks/check-errors.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "${CLAUDE_CWD:-$PWD}" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/OVERLORD_BACKLOG.md" ]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  HLD Pro - Error Pattern Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 <<'PY'
import re
import sys
from pathlib import Path

FAIL_FAST_PATH = Path("docs/FAIL_FAST_LOG.md")
ERROR_PATTERNS_PATH = Path("docs/ERROR_PATTERNS.md")


def has_legacy_marker(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---\n", 4)
    if end == -1:
        return False
    frontmatter = text[4:end]
    return re.search(r"^legacy:\s*true\s*$", frontmatter, re.MULTILINE) is not None


def validate_fail_fast_log() -> bool:
    if not FAIL_FAST_PATH.exists():
        print(f"FAIL {FAIL_FAST_PATH}: file not found")
        return False
    if has_legacy_marker(FAIL_FAST_PATH):
        print(f"PASS {FAIL_FAST_PATH}: legacy marker present")
        return True
    text = FAIL_FAST_PATH.read_text(encoding="utf-8")
    header_re = re.compile(
        r"\|\s*Date\s*\|\s*Category\s*\|\s*Severity\s*\|\s*Error\s*\|\s*Root Cause\s*\|\s*Resolution\s*\|\s*Related Pattern\s*\|",
        re.IGNORECASE,
    )
    if not header_re.search(text):
        print(
            f"FAIL {FAIL_FAST_PATH}: canonical header "
            "'| Date | Category | Severity | Error | Root Cause | Resolution | Related Pattern |' not found"
        )
        return False
    print(f"PASS {FAIL_FAST_PATH}: canonical header present")
    return True


def validate_error_patterns() -> bool:
    if not ERROR_PATTERNS_PATH.exists():
        print(f"FAIL {ERROR_PATTERNS_PATH}: file not found")
        return False
    if has_legacy_marker(ERROR_PATTERNS_PATH):
        print(f"PASS {ERROR_PATTERNS_PATH}: legacy marker present")
        return True
    text = ERROR_PATTERNS_PATH.read_text(encoding="utf-8")
    pattern_ids = re.findall(
        r"^## Pattern: ([a-z0-9]+(?:-[a-z0-9]+)*)\s*$",
        text,
        re.MULTILINE,
    )
    if pattern_ids:
        print(f"PASS {ERROR_PATTERNS_PATH}: found {len(pattern_ids)} pattern heading(s)")
        return True
    if re.search(r"<!--\s*stub: no-patterns-yet\s*-->", text, re.IGNORECASE):
        print(f"PASS {ERROR_PATTERNS_PATH}: explicit stub marker present")
        return True
    print(
        f"FAIL {ERROR_PATTERNS_PATH}: no '## Pattern: <kebab-case-id>' heading "
        "and no '<!-- stub: no-patterns-yet -->' marker"
    )
    return False


ok = validate_fail_fast_log() and validate_error_patterns()
sys.exit(0 if ok else 1)
PY

echo ""
echo "Error pattern check PASS"
