#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

if __package__:
    from . import governed_repos
    from . import verify_governance_consumer
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import governed_repos  # type: ignore[no-redef]
    import verify_governance_consumer  # type: ignore[no-redef]

GOVERNANCE_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = GOVERNANCE_ROOT / 'docs' / 'governance-tooling-package.json'
DESIRED_STATE_PATH = GOVERNANCE_ROOT / 'docs' / 'governance-consumer-pull-state.json'


@dataclass(frozen=True)
class RepoStatus:
    repo: str
    display_name: str
    repo_path: str
    profile: str
    governance_ref: str
    package_version: str
    managed_files: list[str]
    local_overrides: list[dict[str, Any]]
    verifier_status: str
    workflow_pin_status: str
    critical_failures: list[str]
    migration_warnings: list[str]
    residual_drift: list[str]


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise ValueError(f'{path} must contain a JSON object')
    return payload


def _profile_state(desired_state: dict[str, Any], profile: str) -> dict[str, Any]:
    profiles = desired_state.get('profiles')
    if not isinstance(profiles, dict):
        return {}
    payload = profiles.get(profile)
    return payload if isinstance(payload, dict) else {}


def _record_path(manifest: dict[str, Any]) -> str:
    versioning = manifest.get('versioning')
    if isinstance(versioning, dict) and isinstance(versioning.get('consumer_record_path'), str):
        return str(versioning['consumer_record_path'])
    return '.hldpro/governance-tooling.json'


def _repo_profile(repo: Any, desired_state: dict[str, Any]) -> str:
    profiles = desired_state.get('profiles')
    if isinstance(profiles, dict):
        for candidate in (repo.repo_slug, repo.repo_dir_name, repo.display_name):
            if candidate in profiles:
                return str(candidate)
    return str(repo.repo_slug)


def resolve_repo_path(repo: Any, repos_root: Path) -> Path | None:
    candidates = [
        repos_root / str(repo.ci_checkout_path),
        repos_root / str(repo.repo_dir_name),
        repos_root / str(repo.local_path),
    ]
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve(strict=False)
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None


def _managed_paths(record_payload: dict[str, Any]) -> list[str]:
    raw = record_payload.get('managed_files')
    if not isinstance(raw, list):
        return []
    paths: list[str] = []
    for item in raw:
        if isinstance(item, dict) and isinstance(item.get('path'), str):
            paths.append(item['path'])
    return sorted(paths)


def _record_overrides(record_payload: dict[str, Any]) -> list[dict[str, Any]]:
    overrides: list[dict[str, Any]] = []
    for field in ('overrides', 'local_overrides'):
        raw = record_payload.get(field, [])
        if isinstance(raw, list):
            overrides.extend(item for item in raw if isinstance(item, dict))
    return overrides


def _load_record(target_repo: Path, manifest: dict[str, Any]) -> tuple[Path, dict[str, Any] | None, str | None]:
    path = target_repo / _record_path(manifest)
    if not path.exists():
        return path, None, f'consumer record missing: {path}'
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        return path, None, f'consumer record parse failure: {exc}'
    if not isinstance(payload, dict):
        return path, None, 'consumer record must be a JSON object'
    return path, payload, None


def workflow_pin_status(target_repo: Path, governance_ref: str | None = None) -> tuple[str, list[str]]:
    workflow_root = target_repo / '.github' / 'workflows'
    if not workflow_root.exists():
        return 'none', []
    refs: list[str] = []
    drift: list[str] = []
    for path in sorted(workflow_root.glob('*.y*ml')):
        text = path.read_text(encoding='utf-8', errors='replace')
        relpath = path.relative_to(target_repo).as_posix()
        for match in verify_governance_consumer.GOVERNANCE_WORKFLOW_REF_RE.finditer(text):
            ref = match.group('ref').rstrip('/')
            refs.append(ref)
            if not verify_governance_consumer.SHA_RE.fullmatch(ref):
                drift.append(f'{relpath} uses mutable governance workflow ref @{ref}')
            elif governance_ref and verify_governance_consumer.SHA_RE.fullmatch(governance_ref) and ref != governance_ref:
                drift.append(f'{relpath} uses governance workflow ref @{ref}, consumer record has @{governance_ref}')
    if not refs:
        return 'none', []
    if drift:
        return 'drift', drift
    return 'pinned', []


def _verifier_args(
    *,
    governance_root: Path,
    target_repo: Path,
    profile: str,
    record_payload: dict[str, Any] | None,
    expected_governance_ref: str | None,
    strict_expected_ref: bool,
    strict_desired_package: bool,
    desired_state: dict[str, Any],
) -> argparse.Namespace:
    expected_package = ''
    if strict_desired_package:
        state = _profile_state(desired_state, profile)
        expected_package = str(state.get('package_version') or '')
    elif record_payload and isinstance(record_payload.get('package_version'), str):
        expected_package = str(record_payload['package_version'])

    governance_ref = expected_governance_ref if strict_expected_ref and expected_governance_ref else ''
    return argparse.Namespace(
        governance_root=str(governance_root),
        manifest=str(governance_root / 'docs' / 'governance-tooling-package.json'),
        desired_state=str(governance_root / 'docs' / 'governance-consumer-pull-state.json'),
        target_repo=str(target_repo),
        record_path='',
        profile=profile,
        governance_ref=governance_ref,
        package_version=expected_package,
        allow_non_sha_ref=False,
    )


def _migration_warnings(
    *,
    repo_name: str,
    profile: str,
    record_payload: dict[str, Any] | None,
    desired_state: dict[str, Any],
    expected_governance_ref: str | None,
) -> list[str]:
    if not record_payload:
        return []
    warnings: list[str] = []
    state = _profile_state(desired_state, profile)
    expected_package = state.get('package_version')
    observed_package = record_payload.get('package_version')
    if isinstance(expected_package, str) and expected_package and observed_package != expected_package:
        warnings.append(
            f'{repo_name}: package_version migration drift: desired {expected_package}, observed {observed_package}'
        )
    observed_ref = record_payload.get('governance_ref')
    if expected_governance_ref and observed_ref != expected_governance_ref:
        warnings.append(
            f'{repo_name}: governance_ref migration drift: desired {expected_governance_ref}, observed {observed_ref}'
        )
    return warnings


def inspect_repo(
    repo: Any,
    *,
    repos_root: Path,
    governance_root: Path,
    manifest: dict[str, Any],
    desired_state: dict[str, Any],
    expected_governance_ref: str | None = None,
    strict_expected_ref: bool = False,
    strict_desired_package: bool = False,
) -> RepoStatus:
    repo_name = str(repo.repo_dir_name)
    profile = _repo_profile(repo, desired_state)
    target_repo = resolve_repo_path(repo, repos_root)
    if target_repo is None:
        return RepoStatus(
            repo=repo_name,
            display_name=str(repo.display_name),
            repo_path='',
            profile=profile,
            governance_ref='',
            package_version='',
            managed_files=[],
            local_overrides=[],
            verifier_status='critical',
            workflow_pin_status='unknown',
            critical_failures=[f'{repo_name}: checkout missing under {repos_root}'],
            migration_warnings=[],
            residual_drift=[f'{repo_name}: checkout missing under {repos_root}'],
        )

    _, record_payload, record_error = _load_record(target_repo, manifest)
    if record_error:
        workflow_status, workflow_drift = workflow_pin_status(target_repo)
        critical = [f'{repo_name}: {record_error}', *[f'{repo_name}: {item}' for item in workflow_drift]]
        return RepoStatus(
            repo=repo_name,
            display_name=str(repo.display_name),
            repo_path=str(target_repo),
            profile=profile,
            governance_ref='',
            package_version='',
            managed_files=[],
            local_overrides=[],
            verifier_status='critical',
            workflow_pin_status=workflow_status,
            critical_failures=critical,
            migration_warnings=[],
            residual_drift=critical,
        )

    assert record_payload is not None
    args = _verifier_args(
        governance_root=governance_root,
        target_repo=target_repo,
        profile=profile,
        record_payload=record_payload,
        expected_governance_ref=expected_governance_ref,
        strict_expected_ref=strict_expected_ref,
        strict_desired_package=strict_desired_package,
        desired_state=desired_state,
    )
    try:
        verifier_payload = verify_governance_consumer.verify(args)
        verifier_failures = [str(item) for item in verifier_payload.get('failures', [])]
        verifier_warnings = [str(item) for item in verifier_payload.get('warnings', [])]
    except verify_governance_consumer.ConsumerVerifyError as exc:
        verifier_failures = [str(exc)]
        verifier_warnings = []

    workflow_status, workflow_drift = workflow_pin_status(target_repo, str(record_payload.get('governance_ref') or ''))
    critical: list[str] = []
    warning_failures: list[str] = []
    for item in verifier_failures:
        message = f'{repo_name}: {item}'
        if item.startswith('reusable workflow ref SHA mismatch:') and not strict_expected_ref:
            warning_failures.append(message)
        else:
            critical.append(message)
    for item in workflow_drift:
        message = f'{repo_name}: {item}'
        if 'uses mutable governance workflow ref' in item:
            if message not in critical:
                critical.append(message)
        elif not strict_expected_ref:
            if message not in warning_failures:
                warning_failures.append(message)
        elif message not in critical:
            critical.append(message)
    warnings = [f'{repo_name}: {item}' for item in verifier_warnings]
    warnings.extend(warning_failures)
    warnings.extend(
        _migration_warnings(
            repo_name=repo_name,
            profile=profile,
            record_payload=record_payload,
            desired_state=desired_state,
            expected_governance_ref=expected_governance_ref,
        )
    )
    residual = [*critical, *warnings]
    if critical:
        status = 'critical'
    elif warnings:
        status = 'warning'
    else:
        status = 'passed'

    return RepoStatus(
        repo=repo_name,
        display_name=str(repo.display_name),
        repo_path=str(target_repo),
        profile=str(record_payload.get('profile') or profile),
        governance_ref=str(record_payload.get('governance_ref') or ''),
        package_version=str(record_payload.get('package_version') or ''),
        managed_files=_managed_paths(record_payload),
        local_overrides=_record_overrides(record_payload),
        verifier_status=status,
        workflow_pin_status=workflow_status,
        critical_failures=critical,
        migration_warnings=warnings,
        residual_drift=residual,
    )


def build_report(
    repos: Iterable[Any],
    *,
    repos_root: Path,
    governance_root: Path = GOVERNANCE_ROOT,
    expected_governance_ref: str | None = None,
    strict_expected_ref: bool = False,
    strict_desired_package: bool = False,
    generated_at: str | None = None,
) -> dict[str, Any]:
    manifest = _load_json(governance_root / 'docs' / 'governance-tooling-package.json')
    desired_state = _load_json(governance_root / 'docs' / 'governance-consumer-pull-state.json')
    statuses = [
        inspect_repo(
            repo,
            repos_root=repos_root,
            governance_root=governance_root,
            manifest=manifest,
            desired_state=desired_state,
            expected_governance_ref=expected_governance_ref,
            strict_expected_ref=strict_expected_ref,
            strict_desired_package=strict_desired_package,
        )
        for repo in repos
    ]
    critical = [item for status in statuses for item in status.critical_failures]
    warnings = [item for status in statuses for item in status.migration_warnings]
    payload = {
        'generated_at': generated_at or datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'governance_root': str(governance_root),
        'repos_root': str(repos_root),
        'expected_governance_ref': expected_governance_ref or '',
        'strict_expected_ref': strict_expected_ref,
        'strict_desired_package': strict_desired_package,
        'status': 'critical' if critical else 'warning' if warnings else 'passed',
        'totals': {
            'repos': len(statuses),
            'passed': sum(1 for item in statuses if item.verifier_status == 'passed'),
            'warning': sum(1 for item in statuses if item.verifier_status == 'warning'),
            'critical': sum(1 for item in statuses if item.verifier_status == 'critical'),
            'critical_failures': len(critical),
            'migration_warnings': len(warnings),
        },
        'repos': [status.__dict__ for status in statuses],
        'critical_failures': critical,
        'migration_warnings': warnings,
    }
    return payload


def _short_ref(value: str) -> str:
    return value[:12] if value else ''


def _count_or_none(items: list[Any]) -> str:
    return str(len(items)) if items else '0'


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append('# Governance Consumer Adoption Status')
    lines.append('')
    lines.append(f"Generated: {payload['generated_at']}")
    lines.append(f"Overall status: **{payload['status'].upper()}**")
    lines.append('')
    totals = payload['totals']
    lines.append(
        f"Repos: {totals['repos']} | Passed: {totals['passed']} | Warnings: {totals['warning']} | Critical: {totals['critical']}"
    )
    lines.append('')
    lines.append('| Repo | Profile | Governance SHA | Package | Managed Files | Local Overrides | Verifier | Workflow Pins | Residual Drift |')
    lines.append('|---|---|---:|---|---:|---:|---|---|---:|')
    for repo in payload['repos']:
        lines.append(
            '| {repo} | {profile} | `{sha}` | `{package}` | {managed} | {overrides} | {verifier} | {pins} | {drift} |'.format(
                repo=repo['repo'],
                profile=repo['profile'],
                sha=_short_ref(repo['governance_ref']),
                package=repo['package_version'],
                managed=len(repo['managed_files']),
                overrides=_count_or_none(repo['local_overrides']),
                verifier=repo['verifier_status'],
                pins=repo['workflow_pin_status'],
                drift=len(repo['residual_drift']),
            )
        )
    lines.append('')
    lines.append('## Critical Failures')
    lines.append('')
    if payload['critical_failures']:
        lines.extend(f'- {item}' for item in payload['critical_failures'])
    else:
        lines.append('- None')
    lines.append('')
    lines.append('## Migration Warnings')
    lines.append('')
    if payload['migration_warnings']:
        lines.extend(f'- {item}' for item in payload['migration_warnings'])
    else:
        lines.append('- None')
    lines.append('')
    return '\n'.join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Report governed repo SSOT consumer adoption status.')
    parser.add_argument('--governance-root', default=str(GOVERNANCE_ROOT), help='hldpro-governance checkout root')
    parser.add_argument('--repos-root', default='', help='Root containing governed repo checkouts')
    parser.add_argument('--output-json', default='', help='Write JSON report to this path')
    parser.add_argument('--output-md', default='', help='Write Markdown report to this path')
    parser.add_argument('--expected-governance-ref', default='', help='Optional desired governance SHA for migration reporting')
    parser.add_argument('--strict-expected-ref', action='store_true', help='Treat expected governance SHA mismatch as verifier failure')
    parser.add_argument('--strict-desired-package', action='store_true', help='Treat desired-state package mismatch as verifier failure')
    parser.add_argument('--fail-on-critical', action='store_true', help='Exit nonzero when critical drift is present')
    return parser


def _write(path: str, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    governance_root = Path(args.governance_root).resolve()
    repos_root = Path(args.repos_root).resolve() if args.repos_root else governed_repos.repos_root().resolve()
    repos = governed_repos.repos_enabled_for('sweep', governance_root / 'docs' / 'governed_repos.json')
    payload = build_report(
        repos,
        repos_root=repos_root,
        governance_root=governance_root,
        expected_governance_ref=args.expected_governance_ref or None,
        strict_expected_ref=args.strict_expected_ref,
        strict_desired_package=args.strict_desired_package,
    )
    markdown = render_markdown(payload)
    if args.output_json:
        _write(args.output_json, json.dumps(payload, indent=2) + '\n')
    if args.output_md:
        _write(args.output_md, markdown)
    if not args.output_json and not args.output_md:
        print(markdown)
    return 1 if args.fail_on_critical and payload['status'] == 'critical' else 0


if __name__ == '__main__':
    raise SystemExit(main())
