#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES_PATH = REPO_ROOT / "docs" / "delegation" / "delegation_rules.json"
BLOCK_THRESHOLD = 0.90
WARN_THRESHOLD = 0.70
IMPLEMENTATION_SCOPED_EXPLORE = re.compile(
    r"\b(review|audit|validate|write|implement|fix|test|diagram|document|migration|schema|edge function)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OwnerRule:
    task_type: str
    agent: str
    keywords: tuple[str, ...]
    implementation_verbs: tuple[str, ...]


@dataclass(frozen=True)
class GateDecision:
    decision: str
    owner: str
    confidence: float
    reason: str
    source: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "owner": self.owner,
            "confidence": round(self.confidence, 3),
            "reason": self.reason,
            "source": self.source,
        }


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_term(text: str, term: str) -> bool:
    normalized_term = _normalize(term)
    if " " in normalized_term or "-" in normalized_term:
        return normalized_term in text
    return re.search(rf"\b{re.escape(normalized_term)}\b", text) is not None


def load_rules(path: Path = DEFAULT_RULES_PATH) -> tuple[dict[str, Any], list[OwnerRule]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: rules must be a JSON object")
    owners = payload.get("owners")
    if not isinstance(owners, list) or not owners:
        raise ValueError(f"{path}: owners must be a non-empty list")

    parsed: list[OwnerRule] = []
    for index, item in enumerate(owners, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{path}: owners[{index}] must be an object")
        task_type = str(item.get("task_type", "")).strip()
        agent = str(item.get("agent", "")).strip()
        keywords = item.get("keywords")
        verbs = item.get("implementation_verbs")
        if not task_type or not agent:
            raise ValueError(f"{path}: owners[{index}] missing task_type or agent")
        if not isinstance(keywords, list) or not all(isinstance(value, str) and value.strip() for value in keywords):
            raise ValueError(f"{path}: owners[{index}].keywords must be a non-empty string list")
        if not isinstance(verbs, list) or not all(isinstance(value, str) and value.strip() for value in verbs):
            raise ValueError(f"{path}: owners[{index}].implementation_verbs must be a non-empty string list")
        parsed.append(
            OwnerRule(
                task_type=task_type,
                agent=agent,
                keywords=tuple(keywords),
                implementation_verbs=tuple(verbs),
            )
        )
    return payload, parsed


def deterministic_match(task_description: str, rules: list[OwnerRule]) -> GateDecision | None:
    text = _normalize(task_description)
    if not text:
        return None

    best: tuple[float, OwnerRule, list[str], list[str]] | None = None
    for rule in rules:
        matched_keywords = [term for term in rule.keywords if _contains_term(text, term)]
        if not matched_keywords:
            continue
        matched_verbs = [verb for verb in rule.implementation_verbs if _contains_term(text, verb)]
        confidence = 0.95 if matched_verbs else 0.75
        if best is None or confidence > best[0] or (confidence == best[0] and len(matched_keywords) > len(best[2])):
            best = (confidence, rule, matched_keywords, matched_verbs)

    if best is None:
        return None

    confidence, rule, matched_keywords, matched_verbs = best
    reason = f"matched {rule.task_type} owner terms: {', '.join(matched_keywords)}"
    if matched_verbs:
        reason += f"; implementation verb(s): {', '.join(matched_verbs)}"
    return GateDecision("UNSET", rule.agent, confidence, reason, "deterministic")


def classifier_match(classifier_payload: dict[str, Any] | None) -> GateDecision | None:
    if not classifier_payload:
        return None
    owner = str(classifier_payload.get("owner", "")).strip()
    if not owner or owner == "NONE":
        return None
    try:
        confidence = float(classifier_payload.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    reason = str(classifier_payload.get("reason", "classifier fallback")).strip() or "classifier fallback"
    return GateDecision("UNSET", owner, confidence, reason, "classifier")


def apply_policy(
    candidate: GateDecision | None,
    *,
    tool_name: str,
    task_description: str,
    bypass: bool = False,
) -> GateDecision:
    tool = tool_name.strip()
    if bypass:
        return GateDecision("ALLOW", "", 0.0, "explicit bypass flag present", "bypass")
    if tool == "Read":
        return GateDecision("ALLOW", "", 0.0, "Read is never delegated-gated", "policy")
    if tool == "Explore" and not IMPLEMENTATION_SCOPED_EXPLORE.search(task_description):
        return GateDecision("ALLOW", "", 0.0, "Explore text is not implementation-scoped", "policy")
    if candidate is None:
        return GateDecision("ALLOW", "", 0.0, "no delegation owner matched", "policy")

    if candidate.confidence >= BLOCK_THRESHOLD:
        decision = "WARN" if tool == "Explore" else "BLOCK"
    elif candidate.confidence >= WARN_THRESHOLD:
        decision = "WARN"
    else:
        decision = "ALLOW"

    return GateDecision(decision, candidate.owner, candidate.confidence, candidate.reason, candidate.source)


def decide(
    *,
    tool_name: str,
    task_description: str,
    rules_path: Path = DEFAULT_RULES_PATH,
    classifier_payload: dict[str, Any] | None = None,
    bypass: bool = False,
) -> GateDecision:
    _, rules = load_rules(rules_path)
    candidate = deterministic_match(task_description, rules)
    if candidate is None:
        candidate = classifier_match(classifier_payload)
    return apply_policy(candidate, tool_name=tool_name, task_description=task_description, bypass=bypass)


def _load_classifier(raw: str) -> dict[str, Any] | None:
    if not raw.strip():
        return None
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("classifier payload must be a JSON object")
    return payload


def _run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate §DA delegation gate decisions.")
    parser.add_argument("--tool-name", required=True)
    parser.add_argument("--task-description", required=True)
    parser.add_argument("--rules-path", type=Path, default=DEFAULT_RULES_PATH)
    parser.add_argument("--classifier-json", default="")
    parser.add_argument("--bypass", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        decision = decide(
            tool_name=args.tool_name,
            task_description=args.task_description,
            rules_path=args.rules_path,
            classifier_payload=_load_classifier(args.classifier_json),
            bypass=args.bypass,
        )
    except Exception as exc:
        payload = {"decision": "ALLOW", "owner": "", "confidence": 0.0, "reason": f"fail-open: {exc}", "source": "error"}
        print(json.dumps(payload, sort_keys=True) if args.json else payload["reason"])
        return 0

    payload = decision.as_dict()
    print(json.dumps(payload, sort_keys=True) if args.json else payload["decision"])
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_cli())
