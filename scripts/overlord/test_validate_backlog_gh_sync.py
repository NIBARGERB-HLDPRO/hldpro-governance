#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest import mock

import validate_backlog_gh_sync


class TestValidateBacklogGhSync(unittest.TestCase):
    def test_delegates_to_hardened_overlord_alignment_checker(self) -> None:
        with mock.patch.object(validate_backlog_gh_sync.alignment, "main") as alignment_main:
            validate_backlog_gh_sync.main()

        alignment_main.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
