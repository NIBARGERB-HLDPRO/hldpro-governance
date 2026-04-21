#!/usr/bin/env python3
"""Inventory Cloudflare Pages Direct Upload projects for governed consumers."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_PROJECTS = [
    "seek-and-ponder",
    "hldpro-dashboard",
    "hldpro-marketing",
    "hldpro-pwa",
    "hldpro-reseller",
]

PROJECT_OWNERS = {
    "seek-and-ponder": "NIBARGERB-HLDPRO/seek-and-ponder",
    "hldpro-dashboard": "NIBARGERB-HLDPRO/HealthcarePlatform",
    "hldpro-marketing": "NIBARGERB-HLDPRO/ai-integration-services",
    "hldpro-pwa": "NIBARGERB-HLDPRO/ai-integration-services",
    "hldpro-reseller": "NIBARGERB-HLDPRO/ai-integration-services",
}

PROJECT_DEPLOY_PATHS = {
    "seek-and-ponder": "scripts/deploy-pages.sh -> apps/web build -> wrangler pages deploy",
    "hldpro-dashboard": "HealthcarePlatform dashboard frontend -> frontend/dist -> wrangler pages deploy",
    "hldpro-marketing": "ai-integration-services apps/marketing -> apps/marketing/dist -> wrangler pages deploy",
    "hldpro-pwa": "ai-integration-services apps/pwa -> apps/pwa/dist -> wrangler pages deploy",
    "hldpro-reseller": "ai-integration-services apps/reseller -> apps/reseller/dist -> wrangler pages deploy",
}

PROJECT_FOLLOW_UPS = {
    "seek-and-ponder": "https://github.com/NIBARGERB-HLDPRO/seek-and-ponder/issues/163",
    "hldpro-dashboard": "https://github.com/NIBARGERB-HLDPRO/HealthcarePlatform/issues/1478",
    "hldpro-marketing": "https://github.com/NIBARGERB-HLDPRO/ai-integration-services/issues/1217",
    "hldpro-pwa": "https://github.com/NIBARGERB-HLDPRO/ai-integration-services/issues/1217",
    "hldpro-reseller": "https://github.com/NIBARGERB-HLDPRO/ai-integration-services/issues/1217",
}

GATE_ADOPTED = {
    "seek-and-ponder": True,
    "hldpro-dashboard": False,
    "hldpro-marketing": False,
    "hldpro-pwa": False,
    "hldpro-reseller": False,
}


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _api_get_projects(account_id: str, token: str) -> list[dict[str, Any]]:
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "hldpro-pages-inventory/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Cloudflare Pages API request failed with HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cloudflare Pages API request failed: {exc.reason}") from exc

    if not isinstance(payload, dict) or not payload.get("success"):
        raise RuntimeError("Cloudflare Pages API response did not report success")
    result = payload.get("result")
    if not isinstance(result, list):
        raise RuntimeError("Cloudflare Pages API response missing result[]")
    return [item for item in result if isinstance(item, dict)]


def _project_name(project: dict[str, Any]) -> str:
    return str(project.get("name") or project.get("project_name") or "")


def _source_type(project: dict[str, Any]) -> str | None:
    source = project.get("source")
    if isinstance(source, dict):
        raw = source.get("type")
        return str(raw) if raw else None
    raw = project.get("source_type")
    return str(raw) if raw else None


def _git_provider_status(project: dict[str, Any]) -> str:
    source_type = _source_type(project)
    if source_type in {None, "", "direct_upload"}:
        return "no_git_provider_direct_upload"
    return "git_provider_configured"


def _domains(project: dict[str, Any]) -> list[str]:
    domains = project.get("domains")
    if isinstance(domains, list):
        return [str(domain) for domain in domains if domain]
    subdomain = project.get("subdomain")
    return [str(subdomain)] if subdomain else []


def _latest_deployment(project: dict[str, Any]) -> dict[str, Any]:
    latest = project.get("latest_deployment")
    if isinstance(latest, dict):
        return latest
    deployments = project.get("deployments")
    if isinstance(deployments, list) and deployments and isinstance(deployments[0], dict):
        return deployments[0]
    return {}


def _deployment_metadata(deployment: dict[str, Any]) -> dict[str, Any]:
    metadata = deployment.get("deployment_trigger", {}).get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def inventory(projects: list[dict[str, Any]], expected_names: list[str]) -> dict[str, Any]:
    by_name = {_project_name(project): project for project in projects}
    rows = []
    for name in expected_names:
        project = by_name.get(name, {"name": name})
        latest = _latest_deployment(project)
        trigger = latest.get("deployment_trigger") if isinstance(latest.get("deployment_trigger"), dict) else {}
        metadata = _deployment_metadata(latest)
        git_provider_status = _git_provider_status(project)
        gate_adopted = GATE_ADOPTED.get(name, False)
        if name not in by_name:
            disposition = "unknown-needs-follow-up"
        elif gate_adopted:
            disposition = "covered"
        elif git_provider_status == "no_git_provider_direct_upload":
            disposition = "needs-consumer-adoption"
        else:
            disposition = "exempt"
        rows.append(
            {
                "cf_project_name": name,
                "domains": _domains(project),
                "git_provider_status": git_provider_status,
                "source_type": _source_type(project),
                "owning_repo": PROJECT_OWNERS.get(name, "unknown"),
                "current_deploy_path": PROJECT_DEPLOY_PATHS.get(name, "unknown"),
                "governance_gate_exists": gate_adopted,
                "disposition": disposition,
                "follow_up_issue": PROJECT_FOLLOW_UPS.get(name),
                "latest_deployment": {
                    "id": latest.get("id"),
                    "created_on": latest.get("created_on"),
                    "trigger_type": trigger.get("type") if isinstance(trigger, dict) else None,
                    "branch": metadata.get("branch"),
                    "commit_hash": metadata.get("commit_hash"),
                    "commit_message": metadata.get("commit_message"),
                    "commit_dirty": metadata.get("commit_dirty"),
                },
            }
        )
    return {
        "schema_version": "v1",
        "generated_for_issue": 472,
        "parent_epic": 467,
        "source_of_truth": [
            "Cloudflare Pages API /accounts/{account_id}/pages/projects",
            "governance-owned project owner map in this script",
            "repo-local Pages config/workflow evidence",
        ],
        "projects": rows,
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# Cloudflare Pages Direct Upload Inventory",
        "",
        "Issue: #472",
        "Parent epic: #467",
        "",
        "| Project | Domains | Git Provider | Owning Repo | Deploy Path | Gate | Disposition | Follow-up |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in payload["projects"]:
        domains = ", ".join(row["domains"]) if row["domains"] else "unknown"
        gate = "yes" if row["governance_gate_exists"] else "no"
        follow_up = row.get("follow_up_issue") or "n/a"
        lines.append(
            "| {project} | {domains} | {git_provider} | {owner} | {deploy_path} | {gate} | {disposition} | {follow_up} |".format(
                project=row["cf_project_name"],
                domains=domains,
                git_provider=row["git_provider_status"],
                owner=row["owning_repo"],
                deploy_path=row["current_deploy_path"],
                gate=gate,
                disposition=row["disposition"],
                follow_up=follow_up,
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inventory Cloudflare Pages Direct Upload projects")
    parser.add_argument("--account-id", default=os.environ.get("CLOUDFLARE_ACCOUNT_ID"))
    parser.add_argument("--api-token-env", default="CLOUDFLARE_PAGES_TOKEN")
    parser.add_argument("--offline-json", type=Path, help="Read a saved Cloudflare Pages projects JSON payload instead of live API")
    parser.add_argument("--project", action="append", dest="projects", default=[], help="Expected Pages project name")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-markdown", type=Path)
    args = parser.parse_args(argv)

    expected = args.projects or list(DEFAULT_PROJECTS)
    if args.offline_json:
        raw = _load_json(args.offline_json)
        projects = raw.get("result", raw) if isinstance(raw, dict) else raw
        if not isinstance(projects, list):
            raise SystemExit("--offline-json must contain a list or an object with result[]")
    else:
        token = os.environ.get(args.api_token_env)
        if not args.account_id:
            raise SystemExit("CLOUDFLARE_ACCOUNT_ID is required")
        if not token:
            raise SystemExit(f"{args.api_token_env} is required")
        projects = _api_get_projects(args.account_id, token)

    payload = inventory(projects, expected)
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output_json:
        args.output_json.write_text(rendered + "\n", encoding="utf-8")
    if args.output_markdown:
        write_markdown(payload, args.output_markdown)
    if not args.output_json and not args.output_markdown:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
