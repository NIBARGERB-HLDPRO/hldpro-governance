from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "pages_deploy_verifier.py"
SPEC = importlib.util.spec_from_file_location("pages_deploy_verifier", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
pages_deploy_verifier = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pages_deploy_verifier
SPEC.loader.exec_module(pages_deploy_verifier)


EXPECTED_SHA = "a" * 40
OTHER_SHA = "b" * 40


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, url, headers):
        self.calls.append((url, dict(headers)))
        if not self.responses:
            raise AssertionError("unexpected HTTP call")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        if callable(response):
            return response(url, headers)
        return response


def response(status=200, url="https://example.com/cdn-cgi/pages/deployment", headers=None, body=b""):
    return pages_deploy_verifier.HttpResponse(status=status, url=url, headers=headers or {}, body=body)


def write_config(payload):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    with tmp:
        json.dump(payload, tmp)
    return Path(tmp.name)


def run_report(config, transport, expected_sha=EXPECTED_SHA):
    path = write_config(config)
    try:
        return pages_deploy_verifier.run_verification(
            path,
            expected_sha,
            http_get=transport,
            sleep=mock.Mock(),
            now=mock.Mock(side_effect=[1.0, 2.0, 3.0, 4.0, 5.0]),
        )
    finally:
        path.unlink(missing_ok=True)


def test_matching_deployment_id():
    transport = FakeTransport(
        [
            response(headers={"cf-deployment-id": EXPECTED_SHA}, url="https://alias.pages.dev/cdn-cgi/pages/deployment"),
            response(headers={"cf-deployment-id": EXPECTED_SHA}, url="https://www.example.com/cdn-cgi/pages/deployment"),
        ]
    )

    report = run_report(
        {"pages_alias": "alias.pages.dev", "custom_domains": ["www.example.com"], "branch": "main"},
        transport,
    )

    assert report["status"] == "passed"
    assert all(domain["deployment_id_match"] for domain in report["domains"])


def test_stale_source_sha():
    transport = FakeTransport([response(headers={"cf-deployment-id": OTHER_SHA})])

    report = run_report({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"}, transport)

    assert report["status"] == "failed"
    assert report["domains"][0]["deployment_id_match"] is False
    assert "did not match expected" in "\n".join(report["failures"])


def test_domain_not_200():
    transport = FakeTransport([response(status=404, headers={"content-type": "text/plain"}, body=b"missing")])

    report = run_report({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"}, transport)

    assert report["status"] == "passed"
    assert report["domains"][0]["domain_active"] is False
    assert report["domains"][0]["http_status"] == 404


def test_different_deployment_ids():
    transport = FakeTransport(
        [
            response(headers={"cf-deployment-id": EXPECTED_SHA}, url="https://alias.pages.dev/cdn-cgi/pages/deployment"),
            response(headers={"cf-deployment-id": OTHER_SHA}, url="https://www.example.com/cdn-cgi/pages/deployment"),
        ]
    )

    report = run_report(
        {"pages_alias": "alias.pages.dev", "custom_domains": ["www.example.com"], "branch": "main"},
        transport,
    )

    assert report["status"] == "failed"
    assert "different deployment ids" in "\n".join(report["failures"])


def test_redacted_output():
    config_path = write_config({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"})
    secret = "SECRET_TOKEN_VALUE"
    transport = FakeTransport(
        [
            response(
                status=302,
                url=f"https://alias.pages.dev/cdn-cgi/pages/deployment?access_token={secret}",
                headers={"location": f"https://alias.pages.dev/cdn-cgi/pages/deployment?token={secret}"},
            ),
            response(
                headers={"cf-deployment-id": EXPECTED_SHA},
                url=f"https://alias.pages.dev/cdn-cgi/pages/deployment?token={secret}",
            ),
        ]
    )

    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with (
            mock.patch.object(pages_deploy_verifier, "_urllib_get", transport),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            code = pages_deploy_verifier.main(["--config", str(config_path), "--expected-sha", EXPECTED_SHA])
    finally:
        config_path.unlink(missing_ok=True)

    assert code == 0
    combined = stdout.getvalue() + stderr.getvalue()
    assert secret not in combined
    assert "REDACTED" in combined


def test_retry_backoff():
    sleep = mock.Mock()
    transport = FakeTransport(
        [
            OSError("temporary failure one"),
            OSError("temporary failure two"),
            response(headers={"cf-deployment-id": EXPECTED_SHA}),
        ]
    )
    config_path = write_config({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"})

    try:
        report = pages_deploy_verifier.run_verification(
            config_path,
            EXPECTED_SHA,
            http_get=transport,
            sleep=sleep,
            clock=mock.Mock(side_effect=[0, 0, 0, 1, 1]),
            now=mock.Mock(side_effect=[1.0, 2.0, 3.0]),
        )
    finally:
        config_path.unlink(missing_ok=True)

    assert report["status"] == "passed"
    assert len(transport.calls) == 3
    assert sleep.call_count == 2


def test_redirect_chain_recorded():
    transport = FakeTransport(
        [
            response(
                status=301,
                url="https://alias.pages.dev/cdn-cgi/pages/deployment",
                headers={"location": "https://www.example.com/cdn-cgi/pages/deployment"},
            ),
            response(headers={"cf-deployment-id": EXPECTED_SHA}, url="https://www.example.com/cdn-cgi/pages/deployment"),
        ]
    )

    report = run_report({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"}, transport)

    assert [item["status"] for item in report["domains"][0]["redirect_chain"]] == [301, 200]
    assert report["domains"][0]["final_url"] == "https://www.example.com/cdn-cgi/pages/deployment"
    assert all("nocache=" in url for url, _headers in transport.calls)


def test_cache_busting_headers():
    transport = FakeTransport(
        [
            response(headers={"cf-deployment-id": EXPECTED_SHA}),
            response(headers={"cf-deployment-id": EXPECTED_SHA}),
        ]
    )

    report = run_report(
        {"pages_alias": "alias.pages.dev", "custom_domains": ["www.example.com"], "branch": "main"},
        transport,
    )

    assert report["status"] == "passed"
    for url, headers in transport.calls:
        assert headers["Cache-Control"] == "no-cache"
        assert "nocache=" in url


def test_stable_endpoint_not_html():
    html = f"<html><body>{EXPECTED_SHA}</body></html>".encode()

    def assert_endpoint(url, headers):
        assert Path(url.split("?", 1)[0]).as_posix().endswith("/cdn-cgi/pages/deployment")
        return response(headers={"content-type": "text/html"}, body=html)

    transport = FakeTransport([assert_endpoint])

    report = run_report({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"}, transport)

    assert report["status"] == "failed"
    assert "deployment id unavailable" in "\n".join(report["failures"])
    assert EXPECTED_SHA not in json.dumps(report["domains"][0].get("deployment_id"))


def test_cname_mismatch_not_blocking():
    transport = FakeTransport(
        [
            response(
                status=530,
                headers={"cf-pages-error": "cname_mismatch"},
                url="https://www.example.com/cdn-cgi/pages/deployment",
            )
        ]
    )

    report = run_report({"pages_alias": "www.example.com", "custom_domains": [], "branch": "main"}, transport)

    assert report["status"] == "passed"
    assert report["domains"][0]["domain_active"] is False
    assert "CNAME mismatch" in report["domains"][0]["asset_hash_note"]


def test_stale_checkout_refused():
    config_path = write_config({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"})
    transport = mock.Mock()
    completed_fetch = subprocess.CompletedProcess(["git"], 0, stdout="", stderr="")
    completed_log = subprocess.CompletedProcess(["git"], 0, stdout="abc123 local commit\n", stderr="")

    try:
        with mock.patch.object(pages_deploy_verifier.subprocess, "run", side_effect=[completed_fetch, completed_log]):
            with pytest.raises(pages_deploy_verifier.PagesDeployVerifierError):
                pages_deploy_verifier.run_verification(
                    config_path,
                    EXPECTED_SHA,
                    repo_root=Path("/tmp/repo"),
                    http_get=transport,
                )
    finally:
        config_path.unlink(missing_ok=True)

    transport.assert_not_called()


def test_per_domain_report_fields():
    transport = FakeTransport([response(headers={"cf-deployment-id": EXPECTED_SHA})])

    report = run_report({"pages_alias": "alias.pages.dev", "custom_domains": [], "branch": "main"}, transport)

    domain = report["domains"][0]
    for field in ("domain_active", "deployment_id_match", "http_status", "redirect_chain", "asset_hash_note"):
        assert field in domain
