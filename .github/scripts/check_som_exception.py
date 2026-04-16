#!/usr/bin/env python3
"""Check if SOM-BOOTSTRAP-001 exception is active in docs/exception-register.md."""
import datetime
import re
import sys

path = "docs/exception-register.md"
try:
    text = open(path, "r", encoding="utf-8", errors="replace").read()
except FileNotFoundError:
    print("inactive")
    sys.exit(0)

pattern = re.compile(
    r"SOM-BOOTSTRAP-001[\s\S]*?expiry_date:\**\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", re.I
)
match = pattern.search(text)
if not match:
    print("inactive")
    sys.exit(0)

expiry = datetime.date.fromisoformat(match.group(1))
today = datetime.date.today()
print("active" if expiry > today else "inactive")
