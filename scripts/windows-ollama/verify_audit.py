#!/usr/bin/env python3
"""
Standalone verifier for Windows-Ollama audit logs.
Checks schema, hash-chain integrity, HMAC validity, and manifest consistency.
"""

import hashlib
import hmac
import json
import os
import sys
from pathlib import Path


def canonical_json(obj):
    """Return canonical JSON for HMAC computation."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    ).encode('utf-8')


def compute_sha256(data):
    """Compute SHA256 hash of bytes."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def compute_entry_hmac(entry_dict, key):
    """Compute HMAC-SHA256 over entry without entry_hmac field."""
    if not key:
        return None
    entry_copy = {k: v for k, v in entry_dict.items() if k != 'entry_hmac'}
    canonical = canonical_json(entry_copy)
    return hmac.new(
        key.encode('utf-8') if isinstance(key, str) else key,
        canonical,
        hashlib.sha256
    ).hexdigest()


def verify_hmac(entry, computed_hmac, provided_hmac):
    """Safely compare HMACs using constant-time comparison."""
    if computed_hmac is None or provided_hmac is None:
        return True  # Skip if key not available
    return hmac.compare_digest(computed_hmac, provided_hmac)


def verify_audit_dir(audit_dir):
    """
    Verify all audit logs in the directory.
    Returns (success: bool, errors: list[str])
    """
    audit_path = Path(audit_dir)
    if not audit_path.is_dir():
        return False, [f'{audit_dir} is not a directory']

    hmac_key = os.environ.get('SOM_WINDOWS_AUDIT_HMAC_KEY')
    if not hmac_key:
        print('Warning: SOM_WINDOWS_AUDIT_HMAC_KEY not set; skipping HMAC verification', file=sys.stderr)

    errors = []

    # Find all .jsonl files
    jsonl_files = sorted(audit_path.glob('*.jsonl'))
    if not jsonl_files:
        return True, []  # No audit files yet is OK

    for jsonl_file in jsonl_files:
        manifest_file = jsonl_file.with_suffix('.manifest.json')

        # Verify entries in the JSONL file
        entries = []
        with open(jsonl_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f'{jsonl_file.name}:{line_num} - invalid JSON: {e}')
                    continue

                # Check required fields
                required_fields = [
                    'ts', 'seq', 'prev_hash', 'principal', 'session_jti',
                    'tool', 'args_hmac', 'status', 'reject_reason', 'latency_ms', 'entry_hmac'
                ]
                for field in required_fields:
                    if field not in entry:
                        errors.append(f'{jsonl_file.name}:{line_num} - missing field: {field}')

                entries.append((line_num, entry))

        if not entries:
            continue

        # Verify sequence monotonicity
        for i, (line_num, entry) in enumerate(entries):
            expected_seq = i
            if entry.get('seq') != expected_seq:
                errors.append(
                    f'{jsonl_file.name}:{line_num} - seq {entry.get("seq")} != expected {expected_seq}'
                )

        # Verify hash chain
        for i, (line_num, entry) in enumerate(entries):
            if i == 0:
                expected_prev = '0' * 64
            else:
                prev_entry = entries[i - 1][1]
                prev_entry_copy = {k: v for k, v in prev_entry.items() if k != 'entry_hmac'}
                expected_prev = compute_sha256(canonical_json(prev_entry_copy))

            if entry.get('prev_hash') != expected_prev:
                errors.append(
                    f'{jsonl_file.name}:{line_num} - prev_hash mismatch'
                )

        # Verify entry HMACs
        if hmac_key:
            for line_num, entry in entries:
                computed = compute_entry_hmac(entry, hmac_key)
                provided = entry.get('entry_hmac')
                if not verify_hmac(entry, computed, provided):
                    errors.append(
                        f'{jsonl_file.name}:{line_num} - entry_hmac verification failed'
                    )

        # Verify manifest consistency
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    manifest = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f'{manifest_file.name} - invalid JSON: {e}')
                continue

            # Check required manifest fields
            for field in ['first_hash', 'last_hash', 'entry_count', 'sha256_of_file']:
                if field not in manifest:
                    errors.append(f'{manifest_file.name} - missing field: {field}')

            # Verify entry_count
            if manifest.get('entry_count') != len(entries):
                errors.append(
                    f'{manifest_file.name} - entry_count {manifest.get("entry_count")} != actual {len(entries)}'
                )

            # Verify first_hash
            first_entry_copy = {k: v for k, v in entries[0][1].items() if k != 'entry_hmac'}
            expected_first_hash = compute_sha256(canonical_json(first_entry_copy))
            if manifest.get('first_hash') != expected_first_hash:
                errors.append(f'{manifest_file.name} - first_hash mismatch')

            # Verify last_hash
            last_entry_copy = {k: v for k, v in entries[-1][1].items() if k != 'entry_hmac'}
            expected_last_hash = compute_sha256(canonical_json(last_entry_copy))
            if manifest.get('last_hash') != expected_last_hash:
                errors.append(f'{manifest_file.name} - last_hash mismatch')

            # Verify file SHA256
            with open(jsonl_file, 'rb') as f:
                expected_file_sha = compute_sha256(f.read())
            if manifest.get('sha256_of_file') != expected_file_sha:
                errors.append(f'{manifest_file.name} - sha256_of_file mismatch')
        else:
            # If entries exist but no manifest, that's a warning (but not failure for verification)
            if entries:
                print(f'Warning: {manifest_file.name} not found', file=sys.stderr)

    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print('Usage: verify_audit.py <audit_dir>', file=sys.stderr)
        sys.exit(1)

    audit_dir = sys.argv[1]
    success, errors = verify_audit_dir(audit_dir)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
