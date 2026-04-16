#!/usr/bin/env python3
"""Print space-separated list of labels on the current pull request."""
import json
import os

event = os.environ["GITHUB_EVENT_PATH"]
with open(event, "r", encoding="utf-8") as f:
    payload = json.load(f)
pull = payload.get("pull_request") or {}
labels = [l.get("name", "") for l in pull.get("labels", [])]
print(" ".join(filter(None, labels)))
