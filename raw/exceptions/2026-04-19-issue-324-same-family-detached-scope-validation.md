# Issue #324 Same-Family Exception

Anchor: issue-324-same-family-exception
Date: 2026-04-19
Expires: 2026-05-19

This exception permits same-family Codex planning and implementation for the focused execution-scope detached-checkout fix.

Controls:

- Scope is limited to `assert_execution_scope.py`, its focused tests, and issue #324 evidence docs.
- The implementation must preserve local wrong-branch failures.
- Downstream acceptance requires rerunning the EmailAssistant#1 governance PR check after this fix lands.
