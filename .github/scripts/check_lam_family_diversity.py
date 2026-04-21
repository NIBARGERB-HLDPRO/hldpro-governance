import sys
from pathlib import Path
import yaml

cfg = yaml.safe_load(open(".lam-config.yml", "r", encoding="utf-8")) or {}
worker_family = ((cfg.get("worker") or {}).get("model_family") or "").strip()
shadow_critic = cfg.get("shadow_critic") or {}
shadow_family = (shadow_critic.get("model_family") or "").strip()
shadow_authority = (shadow_critic.get("authority") or "").strip()
large_candidates = ((cfg.get("worker") or {}).get("large_on_demand_candidates") or {})
micro_worker = cfg.get("worker_local_micro") or {}

if not worker_family or not shadow_family:
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] .lam-config.yml must define worker.model_family and shadow_critic.model_family")
    raise SystemExit(1)

if worker_family == shadow_family:
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] worker.model_family must differ from shadow_critic.model_family")
    raise SystemExit(1)

if shadow_authority != "ab_shadow_only":
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] shadow_critic.authority must remain ab_shadow_only unless a new promotion issue changes the charter")
    raise SystemExit(1)

if micro_worker.get("model_id") != "mlx-community/Qwen2.5-Coder-7B-Instruct-4bit":
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] worker_local_micro.model_id must remain the Qwen2.5-Coder micro-worker")
    raise SystemExit(1)

if micro_worker.get("authority") != "implementation_only":
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] worker_local_micro.authority must be implementation_only")
    raise SystemExit(1)

large = large_candidates.get("qwen3.6-35b-a3b-4bit") or {}
if large.get("model_id") != "mlx-community/Qwen3.6-35B-A3B-4bit":
    print("::error file=.lam-config.yml,line=1::[check-lam-family-diversity] qwen3.6-35b-a3b-4bit large worker candidate is required")
    raise SystemExit(1)

standards = Path("STANDARDS.md").read_text(encoding="utf-8")
if "Worker (substantial implementation)" not in standards or "`claude-sonnet-4-6`" not in standards:
    print("::error file=STANDARDS.md,line=1::[check-lam-family-diversity] SoM waterfall must keep claude-sonnet-4-6 as the substantial implementation Worker")
    raise SystemExit(1)

if "Windows-Ollama off-ladder" not in standards:
    print("::error file=STANDARDS.md,line=1::[check-lam-family-diversity] SoM waterfall must state Windows-Ollama is off-ladder")
    raise SystemExit(1)

for forbidden in [
    "| 2 | Worker (coder) | `gpt-5.3-codex-spark`",
    "Windows Ollama is an **ACTIVE SoM Tier-2 Worker fallback**",
]:
    if forbidden in standards:
        print(f"::error file=STANDARDS.md,line=1::[check-lam-family-diversity] stale SoM policy text remains: {forbidden}")
        raise SystemExit(1)

pr_template = Path(".github/pull_request_template.md").read_text(encoding="utf-8")
if "Spark only as logged fallback/specialist critique" not in pr_template:
    print("::error file=.github/pull_request_template.md,line=1::[check-lam-family-diversity] PR template must document Spark as fallback/specialist critique only")
    raise SystemExit(1)
