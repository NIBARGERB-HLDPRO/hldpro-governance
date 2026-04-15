#!/usr/bin/env python3
"""
Negative tests for audit writer and verifier.
Tests: chain integrity, HMAC forgery, manifest mismatch, file truncation, replay.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import audit
import verify_audit


class TestAuditChainIntegrity:
    """Test that tampering with a line breaks the chain."""

    def test_tamper_line_breaks_chain(self):
        """Tamper with line N and verify fails at line N+1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_dir = Path(tmpdir)
            os.environ['SOM_WINDOWS_AUDIT_HMAC_KEY'] = 'test-key-12345'

            # Write 3 entries
            writer = audit.AuditWriter(str(audit_dir), enable_append_only=False)
            for i in range(3):
                writer.write_entry(
                    principal=f'user{i}',
                    session_jti=f'jti{i}',
                    tool='test.submit',
                    args_dict={'test': f'arg{i}'},
                    status='ok'
                )

            # Read the file and tamper with line 1
            log_file = list(audit_dir.glob('*.jsonl'))[0]
            with open(log_file, 'r') as f:
                lines = f.readlines()

            assert len(lines) >= 2, "Expected at least 2 lines"

            # Modify line 1 (index 1)
            entry1 = json.loads(lines[1])
            entry1['seq'] = 999  # Tamper
            lines[1] = json.dumps(entry1, separators=(',', ':')) + '\n'

            with open(log_file, 'w') as f:
                f.writelines(lines)

            # Verify should fail
            success, errors = verify_audit.verify_audit_dir(str(audit_dir))
            assert not success, f"Verification should fail but got: {errors}"
            assert len(errors) > 0, "Expected errors"


class TestHmacForgery:
    """Test that replacing entry_hmac with wrong value fails verification."""

    def test_hmac_forgery_detected(self):
        """Replace entry_hmac with wrong value and verify fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_dir = Path(tmpdir)
            os.environ['SOM_WINDOWS_AUDIT_HMAC_KEY'] = 'test-key-12345'

            writer = audit.AuditWriter(str(audit_dir), enable_append_only=False)
            writer.write_entry(
                principal='user1',
                session_jti='jti1',
                tool='test.submit',
                args_dict={'test': 'arg1'},
                status='ok'
            )

            # Read and forge HMAC
            log_file = list(audit_dir.glob('*.jsonl'))[0]
            with open(log_file, 'r') as f:
                lines = f.readlines()

            entry = json.loads(lines[0])
            entry['entry_hmac'] = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
            lines[0] = json.dumps(entry, separators=(',', ':')) + '\n'

            with open(log_file, 'w') as f:
                f.writelines(lines)

            # Verify should fail
            success, errors = verify_audit.verify_audit_dir(str(audit_dir))
            assert not success, f"Verification should fail but got: {errors}"
            assert len(errors) > 0, "Expected errors"


class TestManifestMismatch:
    """Test that modifying manifest fails verification."""

    def test_manifest_first_hash_mismatch(self):
        """Modify first_hash in manifest and verify fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_dir = Path(tmpdir)
            os.environ['SOM_WINDOWS_AUDIT_HMAC_KEY'] = 'test-key-12345'

            writer = audit.AuditWriter(str(audit_dir), enable_append_only=False)
            writer.write_entry(
                principal='user1',
                session_jti='jti1',
                tool='test.submit',
                args_dict={'test': 'arg1'},
                status='ok'
            )

            # Modify manifest
            manifest_file = list(audit_dir.glob('*.manifest.json'))[0]
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)

            manifest['first_hash'] = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
            with open(manifest_file, 'w') as f:
                json.dump(manifest, f)

            # Verify should fail
            success, errors = verify_audit.verify_audit_dir(str(audit_dir))
            assert not success, f"Verification should fail but got: {errors}"
            assert len(errors) > 0, "Expected errors"


class TestFileTruncation:
    """Test that truncated file (missing last line) breaks manifest."""

    def test_file_truncation_detected(self):
        """Delete last line and verify detects entry_count mismatch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_dir = Path(tmpdir)
            os.environ['SOM_WINDOWS_AUDIT_HMAC_KEY'] = 'test-key-12345'

            writer = audit.AuditWriter(str(audit_dir), enable_append_only=False)
            for i in range(3):
                writer.write_entry(
                    principal=f'user{i}',
                    session_jti=f'jti{i}',
                    tool='test.submit',
                    args_dict={'test': f'arg{i}'},
                    status='ok'
                )

            # Delete last line
            log_file = list(audit_dir.glob('*.jsonl'))[0]
            with open(log_file, 'r') as f:
                lines = f.readlines()

            lines = lines[:-1]  # Remove last line
            with open(log_file, 'w') as f:
                f.writelines(lines)

            # Verify should fail
            success, errors = verify_audit.verify_audit_dir(str(audit_dir))
            assert not success, f"Verification should fail but got: {errors}"
            assert len(errors) > 0, "Expected errors about entry_count"


class TestReplay:
    """Test that duplicate line (replay) breaks seq monotonicity."""

    def test_duplicate_line_detected(self):
        """Duplicate a line and verify detects non-monotonic seq."""
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_dir = Path(tmpdir)
            os.environ['SOM_WINDOWS_AUDIT_HMAC_KEY'] = 'test-key-12345'

            writer = audit.AuditWriter(str(audit_dir), enable_append_only=False)
            writer.write_entry(
                principal='user1',
                session_jti='jti1',
                tool='test.submit',
                args_dict={'test': 'arg1'},
                status='ok'
            )
            writer.write_entry(
                principal='user2',
                session_jti='jti2',
                tool='test.submit',
                args_dict={'test': 'arg2'},
                status='ok'
            )

            # Duplicate the first line
            log_file = list(audit_dir.glob('*.jsonl'))[0]
            with open(log_file, 'r') as f:
                lines = f.readlines()

            # Insert duplicate of first line
            lines.insert(1, lines[0])

            with open(log_file, 'w') as f:
                f.writelines(lines)

            # Verify should fail (seq will not be monotonic)
            success, errors = verify_audit.verify_audit_dir(str(audit_dir))
            assert not success, f"Verification should fail but got: {errors}"
            assert len(errors) > 0, "Expected errors about seq"


if __name__ == '__main__':
    # Run tests
    test_classes = [
        TestAuditChainIntegrity,
        TestHmacForgery,
        TestManifestMismatch,
        TestFileTruncation,
        TestReplay,
    ]

    total = 0
    passed = 0

    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]

        for method_name in test_methods:
            total += 1
            method = getattr(instance, method_name)
            try:
                method()
                passed += 1
                print(f'PASS: {test_class.__name__}.{method_name}')
            except AssertionError as e:
                print(f'FAIL: {test_class.__name__}.{method_name}: {e}')
            except Exception as e:
                print(f'ERROR: {test_class.__name__}.{method_name}: {e}')

    print(f'\n{passed}/{total} tests passed')
    sys.exit(0 if passed == total else 1)
