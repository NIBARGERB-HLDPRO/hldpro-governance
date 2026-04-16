import json
import os
with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
    payload = json.load(f)
pull = payload.get("pull_request", {	})
print(" ".join(l.get("name", "") for l in pull.get("labels", [])))
