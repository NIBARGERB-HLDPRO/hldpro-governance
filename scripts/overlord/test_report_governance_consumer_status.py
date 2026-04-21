#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))

import report_governance_consumer_status as report

REPO_ROOT = Path(__file__).resolve().parents[2]
SHA = 'a' * 40
OTHER_SHA = 'b' * 40


def _repo(name: str = 'healthcareplatform') -> SimpleNamespace:
    dir_name = 'HealthcarePlatform' if name == 'healthcareplatform' else name
    return SimpleNamespace(
        repo_slug=name,
        display_name=dir_name,
        repo_dir_name=dir_name,
        local_path=dir_name,
        ci_checkout_path=f'repos/{dir_name}',
    )


class TestReportGovernanceConsumerStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repos_root = self.root / 'repos-root'
        self.repos_root.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _init_repo(self, name: str = 'HealthcarePlatform') -> Path:
        target = self.repos_root / name
        target.mkdir()
        subprocess.run(['git', 'init'], cwd=target, check=True, capture_output=True, text=True)
        return target

    def _write_consumer(self, target: Path, *, profile: str = 'healthcareplatform', ref: str = SHA) -> None:
        shim = target / '.hldpro' / 'local-ci.sh'
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text(
            f'#!/usr/bin/env bash\n# hldpro-governance local-ci gate managed\n# governance_ref={ref}\n',
            encoding='utf-8',
        )
        record = {
            'schema_version': 2,
            'consumer_repo': str(target),
            'governance_repo': 'NIBARGERB-HLDPRO/hldpro-governance',
            'governance_ref': ref,
            'package_version': '0.2.0-ssot-bootstrap',
            'deployed_at': '2026-04-21T00:00:00Z',
            'managed_files': [
                {'path': '.hldpro/local-ci.sh', 'type': 'local_ci_shim'},
                {'path': '.hldpro/governance-tooling.json', 'type': 'consumer_record'},
            ],
            'profile': profile,
            'profile_constraints': [
                'HIPAA and PHI controls must not be weakened',
                'PII/PHI routing must fail closed',
                'strict lane naming policy must be preserved',
                'healthcare-specific audit and RLS controls remain authoritative',
            ] if profile == 'healthcareplatform' else [],
            'local_verification': {'status': 'passed'},
            'github_verification': {'status': 'passed'},
            'overrides': [],
        }
        (target / '.hldpro' / 'governance-tooling.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')

    def test_valid_consumer_reports_warning_only_for_report_only_central_surface(self) -> None:
        target = self._init_repo()
        self._write_consumer(target)

        payload = report.build_report([_repo()], repos_root=self.repos_root, governance_root=REPO_ROOT, generated_at='2026-04-21T00:00:00Z')

        self.assertEqual(payload['totals']['critical'], 0)
        self.assertEqual(payload['totals']['warning'], 1)
        row = payload['repos'][0]
        self.assertEqual(row['repo'], 'HealthcarePlatform')
        self.assertEqual(row['profile'], 'healthcareplatform')
        self.assertEqual(row['governance_ref'], SHA)
        self.assertEqual(row['package_version'], '0.2.0-ssot-bootstrap')
        self.assertEqual(row['managed_files'], ['.hldpro/governance-tooling.json', '.hldpro/local-ci.sh'])
        self.assertEqual(row['workflow_pin_status'], 'none')
        self.assertIn('central GitHub rules/settings are report-only', '\n'.join(row['migration_warnings']))

    def test_missing_record_is_critical(self) -> None:
        self._init_repo()

        payload = report.build_report([_repo()], repos_root=self.repos_root, governance_root=REPO_ROOT, generated_at='2026-04-21T00:00:00Z')

        self.assertEqual(payload['status'], 'critical')
        self.assertEqual(payload['totals']['critical'], 1)
        self.assertIn('consumer record missing', '\n'.join(payload['critical_failures']))
        self.assertEqual(payload['migration_warnings'], [])

    def test_desired_ref_drift_is_migration_warning_when_not_strict(self) -> None:
        target = self._init_repo()
        self._write_consumer(target, ref=SHA)

        payload = report.build_report(
            [_repo()],
            repos_root=self.repos_root,
            governance_root=REPO_ROOT,
            expected_governance_ref=OTHER_SHA,
            strict_expected_ref=False,
            generated_at='2026-04-21T00:00:00Z',
        )

        self.assertEqual(payload['totals']['critical'], 0)
        self.assertIn('governance_ref migration drift', '\n'.join(payload['migration_warnings']))

    def test_mutable_workflow_ref_is_critical(self) -> None:
        target = self._init_repo()
        self._write_consumer(target)
        workflow = target / '.github' / 'workflows' / 'governance.yml'
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            'jobs:\n  check:\n    uses: NIBARGERB-HLDPRO/hldpro-governance/.github/workflows/governance-check.yml@main\n',
            encoding='utf-8',
        )

        payload = report.build_report([_repo()], repos_root=self.repos_root, governance_root=REPO_ROOT, generated_at='2026-04-21T00:00:00Z')

        row = payload['repos'][0]
        self.assertEqual(row['workflow_pin_status'], 'drift')
        self.assertEqual(row['verifier_status'], 'critical')
        self.assertIn('mutable governance workflow ref @main', '\n'.join(payload['critical_failures']))

    def test_markdown_has_required_sections(self) -> None:
        self._init_repo()
        payload = report.build_report([_repo()], repos_root=self.repos_root, governance_root=REPO_ROOT, generated_at='2026-04-21T00:00:00Z')

        markdown = report.render_markdown(payload)

        self.assertIn('| Repo | Profile | Governance SHA | Package | Managed Files | Local Overrides | Verifier | Workflow Pins | Residual Drift |', markdown)
        self.assertIn('## Critical Failures', markdown)
        self.assertIn('## Migration Warnings', markdown)


if __name__ == '__main__':
    unittest.main()
