# GitHub Issues — knocktracker
Date: 2026-04-09

## #142: Add CODEOWNERS baseline for GitHub Enterprise Sprint 1
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary\nAdd a minimal .github/CODEOWNERS baseline for Sprint 1 GitHub Enterprise governance rollout.\n\n## Why\n- Align knocktracker with org-wide CODEOWNERS enforcement planning\n- Prepare staged ruleset rollout without surprising active work\n- Keep ownership explicit for workflow, app, docs, and scripts paths\n\n## Scope\n- add .github/CODEOWNERS\n- keep owner mapping minimal and conservative for first pass\n- do not change GitHub branch protection or rulesets in this issue\n\n## Acceptan
---
## #138: Doc consistency scaffolding for governance docs
Labels: none | Created: 2026-04-07 | Updated: 2026-04-07

## Summary
Bring knocktracker governance docs into the shared minimum contract without flattening repo-specific style.

## Scope
- tighten docs/FEATURE_REGISTRY.md metadata and source-of-truth wording
- tighten docs/DATA_DICTIONARY.md metadata while keeping the lightweight shape
- keep repo-specific service and progress doc structure intact

## Acceptance Criteria
- FEATURE_REGISTRY has required metadata and summary-table contract
- DATA_DICTIONARY has clear source-of-truth metadata
- governance
---
## #135: Document CLAUDE.md conflict runbook and Codex contract
Labels: none | Created: 2026-04-06 | Updated: 2026-04-06

Docs/governance slice for adding a reusable CLAUDE.md conflict-resolution runbook, Codex contract, and aligned PR handoff requirements.
---
## #121: chore: migrate sase-microvm runner to ubuntu-latest
Labels: none | Created: 2026-04-02 | Updated: 2026-04-02

The self-hosted sase-microvm runner no longer exists. All workflows referencing it are stuck. Migrate to ubuntu-latest.
---
## #111: Security/documentation/gate remediation runbook and doc alignment
Labels: none | Created: 2026-03-09 | Updated: 2026-03-09

## Summary
Create a remediation runbook and align documentation around secret handling, GHL legacy status, and governance enforcement gaps identified in repository review.

## Impact
Current docs and repo artifacts contain conflicting GHL secret guidance, stale product framing, and governance requirements that are not clearly operationalized for contributors.

## Exit Criteria
- Create a markdown runbook for remediation sequencing.
- Update top-level documentation to remove or quarantine insecur
---
## #108: Consolidate Routes UX Into Map Panel; Remove Bottom Routes Tab
Labels: none | Created: 2026-02-19 | Updated: 2026-02-20

Status: queued

## Summary
Remove the bottom-tab Routes screen and consolidate route management into the Map screen route icon panel.

## Requested UX
- Remove `Routes` icon/tab from main bottom navigation.
- Keep route management under Map header route icon.
- Keep ability to:
  - create/save route
  - name route
  - delete route
- Simplify route list rows to clickable entries (same interaction model as current map route selector).
- Remove extra route card metadata from this list view:
  - hou
---
## #107: Fix Start Pin Anchor: Stop #1 Must Begin Near Selected Pin
Labels: none | Created: 2026-02-19 | Updated: 2026-02-20

Status: queued

## Summary
Route numbering/order is not consistently anchored to the selected start pin; first knocks can begin elsewhere even when a start pin is set.

## Observed
- User set start pin near stop ~48 area.
- Numbered route started away from pin and was not most efficient around immediate area.

## Scope
- Ensure first stop (and numbering) begins at closest eligible stop to start pin.
- Keep start pin visible while numbered route overlays are shown.
- Preserve closed-loop objectiv
---
## #106: Fix Route Numbering + Street Coverage Guard for Target Home Count
Labels: none | Created: 2026-02-19 | Updated: 2026-02-20

Status: queued

## Summary
Fix route build behavior where selected routes do not show numbered house stops and may skip an interior street/cul-de-sac while trying to satisfy target home count.

## Observed in field test
- Route polyline rendered, but house stop numbering was missing.
- At least one street/cul-de-sac inside selected area was skipped.
- User requested XX-home target should be met as closely as possible **without dropping streets**, while keeping route efficient.

## Problem
Curren
---
## #96: Implement Hierarchical RBAC: Admin, Manager, User
Labels: none | Created: 2026-02-19 | Updated: 2026-02-19

Status: queued

## Summary
Introduce a hierarchical role model where Admin can manage Managers and Users, and Managers can manage Users within their workspace scope.

## Problem
Current permissions are not clearly defined for multi-level administration. We need explicit role boundaries for user management, invites, territory assignment, and manager settings.

## Proposed Role Hierarchy
- Admin: full workspace administration, can create/manage managers and users.
- Manager: operational management
---
## #95: Manager Settings: Add Invite Users Flow
Labels: none | Created: 2026-02-19 | Updated: 2026-02-19

Status: queued

## Summary
Add a manager-only user invitation flow inside Manager Settings so managers can onboard reps directly from one admin location.

## Problem
Managers currently lack a clear in-app path to invite users, and this should live in Manager Settings to avoid cluttering primary workflow screens.

## Scope
- Add "Invite Users" section in Manager Settings.
- Support invite by email with role selection (e.g., rep/admin where allowed).
- Show invite status list (pending/accepted/exp
---
## #93: Add Manager Settings Section for Admin/Manager Controls
Labels: none | Created: 2026-02-19 | Updated: 2026-02-19

Status: queued

## Summary
Add a dedicated Manager Settings page/section in Settings to centralize manager-only controls and reduce clutter across primary app pages.

## Problem
Manager features (territory assignment, routing controls, integration admin, etc.) are spread across screens, increasing navigation friction and crowding day-to-day rep workflows.

## Scope
- Add Manager Settings entry in Settings navigation (role-gated).
- Group manager-only items in one location with clear labels and d
---
## #92: Document and Implement Manager Flow: Create Territories and Assign Users
Labels: none | Created: 2026-02-19 | Updated: 2026-02-19

Status: queued

## Summary
Define and ship a clear manager workflow to create territories and assign them to users from the app.

## Problem
The current flow is unclear for managers: how to create territories, assign reps, and verify assignments is not obvious/end-to-end validated.

## Scope
- Identify the manager entry point(s) for territory creation.
- Add/confirm assignment UI and API behavior for assigning territory to workspace users.
- Provide a visible assignment state (who is assigned, w
---
## #89: Add Face ID / Passkey Login to Mobile App
Labels: none | Created: 2026-02-19 | Updated: 2026-02-19

Status: queued

## Summary
Add biometric and passkey-based sign-in options to reduce password friction while keeping Supabase auth, tenant boundaries, and existing session security intact.

## Problem
Current login relies on email/password only. This increases friction for repeat field use and slows re-entry in low-connectivity, high-frequency mobile workflows.

## Scope
- iOS/Android biometric unlock (Face ID / Touch ID / Android biometrics) for returning authenticated users.
- Optional passkey
---