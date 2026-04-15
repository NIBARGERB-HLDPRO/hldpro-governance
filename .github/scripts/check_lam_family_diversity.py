import sys
import yaml

cfg = yaml.safe_load(open(".lam-config.yml", "r", encoding="utf-8")) or {}
worker_family = ((cfg.get("worker") or {}).get("model_family") or "").strip()
reviewer_family = ((cfg.get("reviewer") or {}).get("model_family") or "").strip()

if not worker_family or not reviewer_family:
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] .lam-config.yml must define worker.model_family and reviewer.model_family")
    raise SystemExit(1)

if worker_family == reviewer_family:
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] worker.model_family must differ from reviewer.model_family")
    raise SystemExit(1)
