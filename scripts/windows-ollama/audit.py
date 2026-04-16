#!/usr/bin/env python3
"""
Append-only audit writer for Windows-Ollama submission tracking.
Mirrors Remote MCP Bridge audit format with hash-chain and daily manifest.
"""

import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
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
    """
    Compute HMAC-SHA256 over canonical JSON of entry (without entry_hmac field).
    Returns hex digest.
    """
    if not key:
        return None

    # Create copy without entry_hmac for signing
    entry_copy = {k: v for k, v in entry_dict.items() if k != 'entry_hmac'}
    canonical = canonical_json(entry_copy)
    return hmac.new(
        key.encode('utf-8') if isinstance(key, str) else key,
        canonical,
        hashlib.sha256
    ).hexdigest()


class AuditWriter:
    """Append-only audit log writer with hash-chain and daily manifest."""

    def __init__(self, audit_dir='raw/remote-windows-audit', enable_append_only=True):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.hmac_key = os.environ.get('SOM_WINDOWS_AUDIT_HMAC_KEY')
        self.enable_append_only = enable_append_only

    def _get_today_path(self):
        """Return path to today's audit log."""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        return self.audit_dir / f'{today}.jsonl'

    def _get_today_manifest_path(self):
        """Return path to today's manifest."""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        return self.audit_dir / f'{today}.manifest.json'

    def _read_last_entry(self):
        """Read the last entry from today's log, or None if file doesn't exist."""
        path = self._get_today_path()
        if not path.exists():
            return None

        try:
            with open(path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return None
                last_line = lines[-1].strip()
                if last_line:
                    return json.loads(last_line)
        except (IOError, json.JSONDecodeError):
            pass
        return None

    def _get_next_seq(self):
        """Get next sequence number for today."""
        last_entry = self._read_last_entry()
        if last_entry is None:
            return 0
        return last_entry.get('seq', -1) + 1

    def _get_prev_hash(self):
        """Get previous entry's hash (or zero for seq=0)."""
        last_entry = self._read_last_entry()
        if last_entry is None:
            return '0' * 64  # 64 zero characters for seq=0

        # Reconstruct the canonical JSON that was signed as entry_hmac
        entry_copy = {k: v for k, v in last_entry.items() if k != 'entry_hmac'}
        return compute_sha256(canonical_json(entry_copy))

    def write_entry(self, principal, session_jti, tool, args_dict, status,
                    reject_reason=None, latency_ms=0):
        """
        Write an audit entry. Returns True if successful, False otherwise.

        Args:
            principal: subject claim from token
            session_jti: jti from token
            tool: tool name (e.g., 'windows-ollama.submit')
            args_dict: tool arguments as dict
            status: 'ok', 'rejected', 'error'
            reject_reason: reason code if status='rejected'
            latency_ms: request latency
        """
        try:
            ts = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
            seq = self._get_next_seq()
            prev_hash = self._get_prev_hash()

            # Compute args HMAC (always, even if key is None — compute as None placeholder)
            args_hmac = compute_entry_hmac(args_dict, self.hmac_key) if self.hmac_key else None

            entry = {
                'ts': ts,
                'seq': seq,
                'prev_hash': prev_hash,
                'principal': principal,
                'session_jti': session_jti,
                'tool': tool,
                'args_hmac': args_hmac,
                'status': status,
                'reject_reason': reject_reason,
                'latency_ms': latency_ms,
            }

            # Compute entry HMAC
            entry['entry_hmac'] = compute_entry_hmac(entry, self.hmac_key)

            # Append to today's log
            log_path = self._get_today_path()

            # Remove append-only flag if it exists (for rewriting in tests)
            if self.enable_append_only and sys.platform == 'darwin':
                try:
                    os.system(f'chflags noupappnd "{log_path}" 2>/dev/null')
                except Exception:
                    pass

            with open(log_path, 'a') as f:
                f.write(json.dumps(entry, separators=(',', ':'), ensure_ascii=False) + '\n')

            # Set file permissions to 0600
            os.chmod(log_path, 0o600)

            # Attempt append-only flag on macOS (only in production)
            if self.enable_append_only and sys.platform == 'darwin':
                try:
                    os.system(f'chflags uappnd "{log_path}" 2>/dev/null')
                except Exception:
                    pass

            # Update daily manifest
            self._write_manifest()

            return True
        except Exception as e:
            print(f'Error writing audit entry: {e}', file=sys.stderr)
            return False

    def _write_manifest(self):
        """Write or update today's manifest."""
        try:
            log_path = self._get_today_path()
            manifest_path = self._get_today_manifest_path()

            if not log_path.exists():
                return

            # Read all entries to compute first/last hash and count
            entries = []
            with open(log_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))

            if not entries:
                return

            # Compute first_hash (hash of first entry)
            first_entry_copy = {k: v for k, v in entries[0].items() if k != 'entry_hmac'}
            first_hash = compute_sha256(canonical_json(first_entry_copy))

            # Compute last_hash (hash of last entry)
            last_entry_copy = {k: v for k, v in entries[-1].items() if k != 'entry_hmac'}
            last_hash = compute_sha256(canonical_json(last_entry_copy))

            # Compute SHA256 of the entire log file
            with open(log_path, 'rb') as f:
                file_sha256 = compute_sha256(f.read())

            manifest = {
                'first_hash': first_hash,
                'last_hash': last_hash,
                'entry_count': len(entries),
                'sha256_of_file': file_sha256
            }

            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, separators=(',', ':'))

            os.chmod(manifest_path, 0o600)
        except Exception as e:
            print(f'Error writing manifest: {e}', file=sys.stderr)


# CLI usage for direct invocation (e.g., from tests)
if __name__ == '__main__':
    if len(sys.argv) < 8:
        print('Usage: audit.py <principal> <session_jti> <tool> <args_json> <status> [reject_reason] [latency_ms]', file=sys.stderr)
        sys.exit(1)

    principal = sys.argv[1]
    session_jti = sys.argv[2]
    tool = sys.argv[3]
    args_json = sys.argv[4]
    status = sys.argv[5]
    reject_reason = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != 'None' else None
    latency_ms = int(sys.argv[7]) if len(sys.argv) > 7 else 0

    try:
        args_dict = json.loads(args_json)
    except json.JSONDecodeError as e:
        print(f'Invalid JSON args: {e}', file=sys.stderr)
        sys.exit(1)

    writer = AuditWriter()
    if writer.write_entry(principal, session_jti, tool, args_dict, status, reject_reason, latency_ms):
        sys.exit(0)
    else:
        sys.exit(1)
