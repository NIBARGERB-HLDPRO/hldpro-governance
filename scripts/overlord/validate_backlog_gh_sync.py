#!/usr/bin/env python3
"""Compatibility entrypoint for the governance backlog GitHub sync gate.

The canonical checker validates both actionable backlog sections:
`## Planned` and `## In Progress`.
"""

from __future__ import annotations

import check_overlord_backlog_github_alignment as alignment


def main() -> None:
    alignment.main()


if __name__ == "__main__":
    main()
