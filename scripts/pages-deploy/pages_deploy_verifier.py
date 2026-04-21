#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TextIO


DEPLOYMENT_PATH = "/cdn-cgi/pages/deployment"
DEFAULT_BRANCH = "main"
MAX_ATTEMPTS = 3
MAX_TOTAL_SECONDS = 30.0
MAX_REDIRECTS = 10
SENSITIVE_QUERY_KEYS = {
    "access_token",
    "auth",
    "authorization",
    "cf_access_client_secret",
    "code",
    "key",
    "secret",
    "sig",
    "signature",
    "signed",
    "token",
}
SHA_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")


class PagesDeployVerifierError(RuntimeError):
    pass


@dataclass(frozen=True)
class HttpResponse:
    status: int
    url: str
    headers: dict[str, str]
    body: bytes = b""


HttpGet = Callable[[str, dict[str, str]], HttpResponse]


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def _headers_dict(raw_headers: Any) -> dict[str, str]:
    return {str(key): str(value) for key, value in raw_headers.items()}


def _header(headers: dict[str, str], name: str) -> str:
    expected = name.lower()
    for key, value in headers.items():
        if key.lower() == expected:
            return value
    return ""


def _sanitize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    sanitized_pairs = [
        (key, "REDACTED" if key.lower() in SENSITIVE_QUERY_KEYS else value)
        for key, value in query_pairs
    ]
    sanitized_query = urllib.parse.urlencode(sanitized_pairs)
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, sanitized_query, parsed.fragment)
    )


def _sanitize_text(value: str) -> str:
    sanitized = value
    for key in SENSITIVE_QUERY_KEYS:
        sanitized = re.sub(
            rf"({re.escape(key)}=)[^&\s]+",
            rf"\1REDACTED",
            sanitized,
            flags=re.IGNORECASE,
        )
    sanitized = re.sub(
        r"(Authorization:\s*)(Bearer\s+)?[A-Za-z0-9._~+/=-]+",
        r"\1REDACTED",
        sanitized,
        flags=re.IGNORECASE,
    )
    return sanitized


def _load_config(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PagesDeployVerifierError(f"could not read config {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PagesDeployVerifierError(f"could not parse config {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PagesDeployVerifierError("config must be a JSON object")
    return payload


def _branch(config: dict[str, Any]) -> str:
    branch = config.get("branch", DEFAULT_BRANCH)
    if not isinstance(branch, str) or not branch.strip():
        raise PagesDeployVerifierError("config branch must be a non-empty string")
    return branch.strip()


def _domains(config: dict[str, Any]) -> list[str]:
    domains: list[str] = []
    pages_alias = config.get("pages_alias")
    if isinstance(pages_alias, str) and pages_alias.strip():
        domains.append(pages_alias.strip())
    elif isinstance(pages_alias, list):
        domains.extend(str(item).strip() for item in pages_alias if str(item).strip())

    custom_domains = config.get("custom_domains", [])
    if custom_domains is None:
        custom_domains = []
    if not isinstance(custom_domains, list):
        raise PagesDeployVerifierError("config custom_domains must be a list")
    domains.extend(str(item).strip() for item in custom_domains if str(item).strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for domain in domains:
        normalized = _domain_label(domain)
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(domain)
    if not deduped:
        raise PagesDeployVerifierError("config must include pages_alias or custom_domains")
    return deduped


def _domain_label(domain: str) -> str:
    parsed = urllib.parse.urlsplit(domain if "://" in domain else f"https://{domain}")
    return parsed.netloc or parsed.path


def _deployment_url(domain: str, nocache: str) -> str:
    parsed = urllib.parse.urlsplit(domain if "://" in domain else f"https://{domain}")
    netloc = parsed.netloc or parsed.path
    if not netloc:
        raise PagesDeployVerifierError(f"invalid domain value: {domain}")
    return urllib.parse.urlunsplit(("https", netloc, DEPLOYMENT_PATH, f"nocache={nocache}", ""))


def _query_value(url: str, key: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    for query_key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True):
        if query_key == key:
            return value
    return ""


def _with_query_value(url: str, key: str, value: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    pairs = [
        (query_key, query_value)
        for query_key, query_value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        if query_key != key
    ]
    pairs.append((key, value))
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(pairs), parsed.fragment)
    )


def _urllib_get(url: str, headers: dict[str, str]) -> HttpResponse:
    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(_NoRedirectHandler)
    try:
        with opener.open(request, timeout=10) as response:
            return HttpResponse(
                status=int(response.getcode()),
                url=str(response.geturl()),
                headers=_headers_dict(response.headers),
                body=response.read(65536),
            )
    except urllib.error.HTTPError as exc:
        return HttpResponse(
            status=int(exc.code),
            url=str(exc.geturl()),
            headers=_headers_dict(exc.headers),
            body=exc.read(65536),
        )


def _fetch_with_redirects(url: str, headers: dict[str, str], http_get: HttpGet) -> tuple[HttpResponse, list[dict[str, Any]]]:
    nocache = _query_value(url, "nocache")
    current_url = _with_query_value(url, "nocache", nocache) if nocache else url
    redirect_chain: list[dict[str, Any]] = []
    for _ in range(MAX_REDIRECTS + 1):
        response = http_get(current_url, headers)
        response_url = response.url or current_url
        redirect_chain.append({"url": _sanitize_url(response_url), "status": response.status})
        location = _header(response.headers, "location")
        if response.status in {301, 302, 303, 307, 308} and location:
            current_url = urllib.parse.urljoin(response_url, location)
            if nocache:
                current_url = _with_query_value(current_url, "nocache", nocache)
            continue
        return response, redirect_chain
    raise PagesDeployVerifierError(f"too many redirects while probing {_sanitize_url(url)}")


def _extract_deployment_id(response: HttpResponse) -> tuple[str | None, str]:
    header_value = _header(response.headers, "cf-deployment-id").strip()
    if header_value:
        return header_value, "cf-deployment-id header"

    content_type = _header(response.headers, "content-type").lower()
    if "html" in content_type:
        return None, "none"

    text = response.body.decode("utf-8", errors="replace").strip()
    if not text:
        return None, "none"

    if content_type.startswith("application/json") or text.startswith("{"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            for key in ("deployment_id", "deploymentId", "id", "source_sha", "sha"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip(), f"{DEPLOYMENT_PATH} endpoint"

    if SHA_RE.match(text):
        return text, f"{DEPLOYMENT_PATH} endpoint"
    return None, "none"


def _cname_note(response: HttpResponse) -> str:
    values = [
        _header(response.headers, "cf-pages-error"),
        _header(response.headers, "cf-cname-status"),
        _header(response.headers, "x-cname-status"),
        _header(response.headers, "x-pages-domain-status"),
    ]
    joined = " ".join(value for value in values if value).lower()
    if "cname" in joined:
        return "CNAME mismatch reported; operator concern, not blocking verifier."
    return ""


def _domain_result(
    domain: str,
    expected_sha: str,
    response: HttpResponse,
    redirect_chain: list[dict[str, Any]],
    attempts: int,
) -> dict[str, Any]:
    deployment_id, source = _extract_deployment_id(response)
    domain_active = response.status == 200
    deployment_id_match = bool(domain_active and deployment_id == expected_sha)

    if not domain_active:
        note = _cname_note(response) or "Domain returned non-200; operator concern, not blocking verifier."
    elif deployment_id:
        note = f"Deployment id observed via {source}; HTML body was not inspected."
    else:
        note = "Deployment id unavailable from stable endpoint/header; HTML body was not inspected."

    return {
        "domain": _domain_label(domain),
        "domain_active": domain_active,
        "deployment_id_match": deployment_id_match,
        "deployment_id": deployment_id,
        "http_status": response.status,
        "final_url": _sanitize_url(response.url),
        "redirect_chain": redirect_chain,
        "asset_hash_note": note,
        "attempts": attempts,
    }


def _error_domain_result(domain: str, message: str, attempts: int) -> dict[str, Any]:
    return {
        "domain": _domain_label(domain),
        "domain_active": False,
        "deployment_id_match": False,
        "deployment_id": None,
        "http_status": 0,
        "final_url": "",
        "redirect_chain": [],
        "asset_hash_note": f"Request failed after {attempts} attempts: {_sanitize_text(message)}",
        "attempts": attempts,
    }


def _should_retry_response(response: HttpResponse) -> bool:
    if _cname_note(response):
        return False
    return response.status == 429 or response.status >= 500


def _sleep_for_retry(
    attempt: int,
    start_time: float,
    clock: Callable[[], float],
    sleep: Callable[[float], None],
) -> None:
    delay = float(2 ** (attempt - 1))
    remaining = MAX_TOTAL_SECONDS - (clock() - start_time)
    if remaining <= 0:
        return
    sleep(max(0.0, min(delay, remaining)))


def probe_domain(
    domain: str,
    expected_sha: str,
    *,
    http_get: HttpGet | None = None,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], float] = time.time,
) -> dict[str, Any]:
    if http_get is None:
        http_get = _urllib_get
    start_time = clock()
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "hldpro-pages-deploy-verifier/1.0",
    }
    last_error = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):
        nocache = f"{int(now() * 1000)}-{attempt}"
        url = _deployment_url(domain, nocache)
        try:
            response, redirect_chain = _fetch_with_redirects(url, headers, http_get)
        except Exception as exc:  # noqa: BLE001 - surfaced as redacted verifier evidence.
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < MAX_ATTEMPTS and clock() - start_time < MAX_TOTAL_SECONDS:
                _sleep_for_retry(attempt, start_time, clock, sleep)
                continue
            return _error_domain_result(domain, last_error, attempt)

        if _should_retry_response(response) and attempt < MAX_ATTEMPTS and clock() - start_time < MAX_TOTAL_SECONDS:
            _sleep_for_retry(attempt, start_time, clock, sleep)
            continue
        return _domain_result(domain, expected_sha, response, redirect_chain, attempt)

    return _error_domain_result(domain, last_error or "request did not complete", MAX_ATTEMPTS)


def stale_checkout_guard(repo_root: Path, branch: str) -> None:
    fetch = subprocess.run(
        ["git", "fetch", "origin", branch],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        detail = _sanitize_text((fetch.stderr or fetch.stdout).strip())
        raise PagesDeployVerifierError(f"stale-checkout guard fetch failed for origin/{branch}: {detail}")

    log = subprocess.run(
        ["git", "log", f"origin/{branch}..HEAD", "--oneline"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if log.returncode != 0:
        detail = _sanitize_text((log.stderr or log.stdout).strip())
        raise PagesDeployVerifierError(f"stale-checkout guard log failed for origin/{branch}: {detail}")
    if log.stdout.strip():
        raise PagesDeployVerifierError(
            f"stale checkout refused: local HEAD has commits not in origin/{branch}: "
            f"{_sanitize_text(log.stdout.strip())}"
        )


def build_report(
    config: dict[str, Any],
    expected_sha: str,
    *,
    http_get: HttpGet | None = None,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], float] = time.time,
) -> dict[str, Any]:
    domains = [
        probe_domain(domain, expected_sha, http_get=http_get, sleep=sleep, clock=clock, now=now)
        for domain in _domains(config)
    ]

    failures: list[str] = []
    warnings: list[str] = []
    active_domains = [domain for domain in domains if domain["domain_active"]]
    observed_active_ids = {
        domain["deployment_id"]
        for domain in active_domains
        if isinstance(domain.get("deployment_id"), str) and domain["deployment_id"]
    }

    for domain in domains:
        if not domain["domain_active"]:
            warnings.append(f"{domain['domain']} inactive or non-200: {domain['asset_hash_note']}")
            continue
        if not domain.get("deployment_id"):
            failures.append(f"{domain['domain']} active but deployment id unavailable")
        elif not domain["deployment_id_match"]:
            failures.append(
                f"{domain['domain']} deployment id {domain['deployment_id']} did not match expected {expected_sha}"
            )

    if len(observed_active_ids) > 1:
        failures.append(f"active domains reported different deployment ids: {sorted(observed_active_ids)}")

    return {
        "status": "failed" if failures else "passed",
        "expected_sha": expected_sha,
        "branch": _branch(config),
        "freshness_threshold": config.get("freshness_threshold"),
        "parity_rule": config.get("parity_rule", "active_domains_match_expected_sha"),
        "domains": domains,
        "failures": failures,
        "warnings": warnings,
    }


def run_verification(
    config_path: Path,
    expected_sha: str,
    *,
    repo_root: Path | None = None,
    http_get: HttpGet | None = None,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], float] = time.time,
) -> dict[str, Any]:
    config = _load_config(config_path)
    branch = _branch(config)
    if repo_root is not None:
        stale_checkout_guard(repo_root, branch)
    return build_report(config, expected_sha, http_get=http_get, sleep=sleep, clock=clock, now=now)


def emit_summary(report: dict[str, Any], stream: TextIO = sys.stderr) -> None:
    status = str(report.get("status", "unknown")).upper()
    domains = report.get("domains", [])
    active = sum(1 for domain in domains if isinstance(domain, dict) and domain.get("domain_active"))
    matched = sum(1 for domain in domains if isinstance(domain, dict) and domain.get("deployment_id_match"))
    print(f"{status}: {matched}/{active} active domains matched expected deployment id", file=stream)
    for domain in domains:
        if not isinstance(domain, dict):
            continue
        domain_name = domain.get("domain", "unknown")
        status_code = domain.get("http_status", 0)
        match = "match" if domain.get("deployment_id_match") else "no-match"
        active_state = "active" if domain.get("domain_active") else "inactive"
        print(f"- {domain_name}: {active_state}, HTTP {status_code}, {match}", file=stream)
    for failure in report.get("failures", []):
        print(f"FAIL: {_sanitize_text(str(failure))}", file=stream)
    for warning in report.get("warnings", []):
        print(f"WARN: {_sanitize_text(str(warning))}", file=stream)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Cloudflare Pages deployment freshness and domain parity.")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args(argv)

    try:
        report = run_verification(args.config, args.expected_sha, repo_root=args.repo_root)
    except PagesDeployVerifierError as exc:
        message = _sanitize_text(str(exc))
        print(json.dumps({"status": "aborted", "error": message}, indent=2, sort_keys=True))
        print(f"ERROR: {message}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    emit_summary(report)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
