from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import validate_provisioning_evidence as validator


class ValidateProvisioningEvidenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_file(self, rel_path: str, content: str) -> Path:
        path = self.root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_validator(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = validator.main(["--root", str(self.root), *args])
        return rc, out.getvalue()

    def test_safe_name_only_missing_secret_output_passes(self) -> None:
        self.write_file(
            "raw/validation/safe.md",
            "Missing required secret variables: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID.\n"
            "Provision them through hldpro-governance/.env.shared plus bootstrap.\n"
            "Values are intentionally not accepted here.\n",
        )

        rc, output = self.run_validator("raw/validation/safe.md")

        self.assertEqual(rc, 0)
        self.assertIn("PASS provisioning evidence scan", output)

    def test_token_like_string_fails_without_echoing_value(self) -> None:
        token = "sk" + "_live_" + "abcdefghijklmnopqrstuvwxyz123456"
        self.write_file("raw/validation/leak.md", f"Token: {token}\n")

        rc, output = self.run_validator("raw/validation/leak.md")

        self.assertEqual(rc, 1)
        self.assertIn("token-like-string", output)
        self.assertNotIn(token, output)

    def test_jwt_fragment_fails(self) -> None:
        self.write_file(
            "raw/validation/jwt.md",
            "JWT: eyJhbGciOiJIUzI1NiJ9.abcdefghijklmnopqrstuvwxyz123456.abcdefghijklmnopqrstuvwxyz123456\n",
        )

        rc, output = self.run_validator("raw/validation/jwt.md")

        self.assertEqual(rc, 1)
        self.assertIn("jwt-fragment", output)

    def test_authorization_header_fails(self) -> None:
        self.write_file("raw/validation/header.md", "Authorization: Bearer abcdefghijklmnop1234567890\n")

        rc, output = self.run_validator("raw/validation/header.md")

        self.assertEqual(rc, 1)
        self.assertIn("authorization-header", output)
        self.assertNotIn("abcdefghijklmnop1234567890", output)

    def test_signed_url_fails(self) -> None:
        self.write_file("raw/validation/url.md", "https://example.com/path?X-Amz-Signature=abcdef1234567890\n")

        rc, output = self.run_validator("raw/validation/url.md")

        self.assertEqual(rc, 1)
        self.assertIn("signed-url", output)
        self.assertNotIn("abcdef1234567890", output)

    def test_raw_phone_number_fails(self) -> None:
        self.write_file("raw/validation/phone.md", "Test phone: +18175550123\n")

        rc, output = self.run_validator("raw/validation/phone.md")

        self.assertEqual(rc, 1)
        self.assertIn("raw-phone-number", output)
        self.assertNotIn("+18175550123", output)

    def test_generated_env_file_content_fails(self) -> None:
        self.write_file(".env.local", "CLOUDFLARE_API_TOKEN=token-value-that-should-not-appear\n")

        rc, output = self.run_validator(".env.local")

        self.assertEqual(rc, 1)
        self.assertIn("generated-env-file-content", output)
        self.assertNotIn("token-value-that-should-not-appear", output)

    def test_changed_files_file_limits_scan(self) -> None:
        changed = self.write_file("changed-files.txt", "raw/validation/leak.md\n")
        self.write_file("raw/validation/leak.md", "Authorization: Bearer abcdefghijklmnop1234567890\n")
        ignored_token = "sk" + "_live_" + "abcdefghijklmnopqrstuvwxyz123456"
        self.write_file("raw/validation/ignored.md", f"Token: {ignored_token}\n")

        rc, output = self.run_validator("--changed-files-file", str(changed))

        self.assertEqual(rc, 1)
        self.assertIn("raw/validation/leak.md:1", output)
        self.assertNotIn("raw/validation/ignored.md", output)


if __name__ == "__main__":
    unittest.main()
