# Living Knowledge Base — Claude CLI Instructions
# HLD Pro Governance + Knowledge System
# Version 1.0 · April 2026
# Drop this file into hldpro-governance/.claude/plans/

---

## CONTEXT

You are implementing a three-phase Living Knowledge Base system across two repos:
- `hldpro-governance` — receives all knowledge infrastructure
- `ai-integration-services` — gets read-only pointers and a PreToolUse hook only

Three tools. Three distinct strategies:
- **graphify** -> install as-is (pip + CLI)
- **Karpathy Loop** -> build our own (pattern, not a package)
- **MBIF Crew** -> take pieces only (dispatcher pattern from CLAUDE.md, nothing else)

You are a solo operator. Do not add new agents. Do not change product code. Do not modify STANDARDS.md or any existing governance files without explicit instruction.

---

## PHASE 1 — graphify Install + Initial Graph Build
### Target: ~2–3 hrs · Do this first, it is independent

**Step 1.1 — Install graphify**

```bash
pip install graphifyy && graphify install
```

Verify:
```bash
graphify --version
# Should return without error
ls ~/.claude/skills/graphify/SKILL.md
# Should exist
```

---

**Step 1.2 — Install graphify PreToolUse hook in ai-integration-services**

Run this from the `ai-integration-services` repo root:
```bash
graphify claude install
```

Verify `.claude/settings.json` now contains a graphify PreToolUse hook entry.
Verify `CLAUDE.md` now has a graphify section pointing to `graphify-out/GRAPH_REPORT.md`.

---

**Step 1.3 — Build the initial knowledge graph**

From `ai-integration-services` root, open Claude Code and run:
```text
/graphify .
```

This will:
- Run deterministic AST pass over all 131 edge functions (local, no API cost)
- Run Claude subagents over migrations, plan docs, markdown files
- Produce `graphify-out/GRAPH_REPORT.md`, `graph.json`, `graph.html`

Expected runtime: 20–40 minutes on first run.

After it completes, verify `graphify-out/GRAPH_REPORT.md` exists and contains:
- God nodes section (highest-degree concepts)
- Community clusters
- Suggested questions

---

**Step 1.4 — Move graphify-out/ to hldpro-governance**

```bash
# From ai-integration-services root
mv graphify-out/ ../hldpro-governance/graphify-out/

# Update ai-integration-services .gitignore to exclude graph.html (large binary)
echo "graphify-out/graph.html" >> .gitignore
echo "graphify-out/cache/" >> .gitignore
```

Update `ai-integration-services/CLAUDE.md` graphify pointer to the new path:
```text
Read ../hldpro-governance/graphify-out/GRAPH_REPORT.md before answering architecture questions.
```

---

**Step 1.5 — Install graphify git hook in ai-integration-services**

```bash
# From ai-integration-services root
graphify hook install
graphify hook status
# Should return: installed
```

This rebuilds the graph on every commit automatically.

---

**Step 1.6 — Generate initial wiki stub**

From `hldpro-governance` root, with `ai-integration-services` as the target:
```bash
graphify ../ai-integration-services --wiki
# Outputs wiki/ directory with index.md + community articles
mv wiki/ hldpro-governance/wiki/
```

---

**Step 1.7 — Phase 1 completion check**

Run all of these. All must pass before moving to Phase 2:

```bash
# 1. graphify CLI works
graphify --version

# 2. Graph report exists
ls hldpro-governance/graphify-out/GRAPH_REPORT.md

# 3. PreToolUse hook exists in ai-integration-services
grep -l "graphify" ai-integration-services/.claude/settings.json

# 4. Wiki stub exists
ls hldpro-governance/wiki/index.md

# 5. Git hook installed
cd ai-integration-services && graphify hook status
```

---

## PHASE 2 — Dispatcher CLAUDE.md + Wiki Write-Back
### Target: ~4–5 hrs · Requires Phase 1 complete

**Step 2.1 — Rewrite hldpro-governance/CLAUDE.md as pure dispatcher**

Replace the existing CLAUDE.md with the following pattern (adapted from My Brain Is Full Crew):

```markdown
# hldpro-governance — Agent Dispatcher

## CRITICAL RULE
NEVER RESPOND DIRECTLY TO THE USER IF AN AGENT EXISTS FOR THE TASK.
You are the dispatcher. The user talks to you. The agents do the work.
Your only job: recognize intent and delegate to the right agent.

## Pre-Session Context (read before every session)
1. Read `wiki/index.md` — current knowledge base state
2. Read `graphify-out/GRAPH_REPORT.md` — god nodes and community structure
3. Read `OVERLORD_BACKLOG.md` — cross-repo governance work tracking

## Routing Table

| User Intent | Agent | Trigger Phrases |
|---|---|---|
| Standards drift check | `overlord` | "check standards", "session start", "what's drifted" |
| Weekly audit / metrics | `overlord-sweep` | "run sweep", "weekly audit", "check all repos" |
| Deep pattern analysis | `overlord-audit` | "deep audit", "analyze patterns", "PR recommendations" |
| Completion verification | `verify-completion` | "verify done", "check artifacts", "mark complete" |

## Delegation Rules
- DO NOT answer governance questions yourself — route to overlord
- DO NOT run audits yourself — route to overlord-sweep
- DO NOT verify completion yourself — route to verify-completion
- If the request doesn't match any agent: say which agent is closest and ask for clarification
- NEVER skip pre-session context reads (wiki/index.md + GRAPH_REPORT.md)
```

---

**Step 2.2 — Create raw/ directory structure**

```bash
cd hldpro-governance
mkdir -p raw/conversations
mkdir -p raw/github-issues
mkdir -p raw/closeouts
mkdir -p raw/operator-context

# Create .gitkeep files so empty dirs are tracked
touch raw/conversations/.gitkeep
touch raw/github-issues/.gitkeep
touch raw/closeouts/.gitkeep
touch raw/operator-context/.gitkeep

# Add raw/ to .gitignore exceptions (track structure, ignore large files)
echo "raw/**/*.mp3" >> .gitignore
echo "raw/**/*.wav" >> .gitignore
```

---

**Step 2.3 — Create wiki/ structure**

```bash
cd hldpro-governance
mkdir -p wiki/hldpro
mkdir -p wiki/decisions
mkdir -p wiki/patterns

# Move Phase 1 wiki output into correct subdirectories
# Community articles from graphify go to wiki/hldpro/
```

Create `wiki/index.md` with this template:

```markdown
# HLD Pro — Knowledge Base Index
Last updated: {{DATE}}
Generated by: overlord-sweep (weekly) + graphify (per-commit)

## Platform Status
<!-- overlord-sweep writes here weekly -->
- Overall: HEALTHY | ATTENTION NEEDED | ACTION REQUIRED
- Last sweep: {{DATE}}

## Recent Decisions
<!-- Stage 6 closeouts write here -->
{{LIST OF RECENT DECISION FILES IN wiki/decisions/}}

## Open Patterns
<!-- Recurring issues, unresolved architectural questions -->
{{LIST OF PATTERN FILES IN wiki/patterns/}}

## Knowledge Graph Summary
<!-- Extracted from graphify-out/GRAPH_REPORT.md -->
- God nodes: {{TOP 5 GOD NODES}}
- Communities: {{COMMUNITY COUNT}} clusters identified
- Full report: ../graphify-out/GRAPH_REPORT.md

## Navigation
- [HLD Pro architecture](hldpro/architecture.md)
- [Decision log](decisions/)
- [Pattern library](patterns/)
- [Raw feeds](../raw/)
```

---

**Step 2.4 — Extend overlord-sweep.md with wiki write-back**

Add the following section to the END of `agents/overlord-sweep.md`:

```markdown
## Wiki Write-Back (Final Step — Always Run)

After completing the weekly audit, perform the following Karpathy Loop steps:

### 1. Read raw feeds
Read everything new in:
- `raw/closeouts/` since last sweep date
- `raw/github-issues/` since last sweep date
- `raw/operator-context/` since last sweep date

### 2. Update wiki
For each significant finding or pattern identified:
- New architectural decision -> create `wiki/decisions/YYYY-MM-DD-{slug}.md`
- Recurring failure pattern -> create or update `wiki/patterns/{slug}.md`
- Update `wiki/index.md` with latest status and links

### 3. File back
Commit all wiki/ changes to hldpro-governance with message:
`docs(wiki): weekly sweep write-back YYYY-MM-DD`

### 4. Health check
Run lint pass on wiki/:
- Find broken wikilinks (links to files that don't exist)
- Identify wiki pages with no inbound links (orphans)
- Flag pages not updated in 30+ days
- Suggest 2-3 new connections between recent raw/ entries and existing wiki pages

Report health check findings in the sweep report under section: WIKI HEALTH
```

---

**Step 2.5 — Add wiki/index.md pointer to all overlord agents**

Add this line to the top of the ## How you work section in each of the four agent files:
`overlord.md`, `overlord-sweep.md`, `overlord-audit.md`, `verify-completion.md`:

```markdown
## Pre-Session Context (read before starting)
1. Read `wiki/index.md` for current knowledge base state
2. Read `graphify-out/GRAPH_REPORT.md` for god nodes and community structure
Proceed only after reading both.
```

---

**Step 2.6 — Seed raw/conversations/ with key decisions**

Manually create 5–10 markdown files in `raw/conversations/` from recent Claude.ai session decisions. Format:

```markdown
# Decision: [Title]
Date: YYYY-MM-DD
Source: Claude.ai session
Session URL: https://claude.ai/chat/[id]

## Context
[Why this decision was needed]

## Decision Made
[What was decided]

## Rationale
[Why this choice over alternatives]

## Links To
- [Related wiki page if exists]
- [Related edge function / migration]
```

Priority decisions to seed first:
- CRMConnector abstraction (never write vendor-specific code)
- VAPI -> PersonaPlex architecture decision
- Qwen3-32B as fine-tune target (not 8B)
- graphify install in hldpro-governance (this decision)
- Six-stage development cycle adoption

---

**Step 2.7 — Phase 2 completion check**

```bash
# 1. Dispatcher rule exists in governance CLAUDE.md
grep "NEVER RESPOND DIRECTLY" hldpro-governance/CLAUDE.md

# 2. raw/ structure exists
ls hldpro-governance/raw/conversations/
ls hldpro-governance/raw/github-issues/
ls hldpro-governance/raw/closeouts/

# 3. wiki/ structure exists
ls hldpro-governance/wiki/index.md
ls hldpro-governance/wiki/decisions/
ls hldpro-governance/wiki/patterns/

# 4. Sweep has wiki write-back section
grep "Wiki Write-Back" hldpro-governance/agents/overlord-sweep.md

# 5. All agents have pre-session context reads
grep "wiki/index.md" hldpro-governance/agents/overlord.md
grep "wiki/index.md" hldpro-governance/agents/overlord-sweep.md
grep "wiki/index.md" hldpro-governance/agents/overlord-audit.md
grep "wiki/index.md" hldpro-governance/agents/verify-completion.md
```

---

## PHASE 3 — Karpathy Loop + Closeout Hook
### Target: ~6–8 hrs · Requires Phase 2 complete

**Step 3.1 — Create Stage 6 closeout template**

Create `hldpro-governance/raw/closeouts/TEMPLATE.md`:

```markdown
# Stage 6 Closeout
Date: YYYY-MM-DD
Repo: [ai-integration-services | hldpro-governance | other]
Task ID: [PROGRESS.md entry ID or GitHub issue #]
Six-Stage Cycle: Stage 6 / Audit + Closeout
Completed By: Benji

## Decision Made
[One sentence: what was decided or built]

## Pattern Identified
[Optional: recurring pattern this reveals — e.g., "all edge functions calling external APIs need explicit timeout handling"]

## Contradicts Existing
[Optional: does this contradict or update anything in wiki/? Link to the page.]

## Files Changed
[List of key files modified]

## Wiki Pages Updated
[List of wiki/ pages this closeout should update. If none exist yet, note what should be created.]

## operator_context Written
[ ] Yes — row ID: [id]
[ ] No — reason: [reason]

## Links To
[Links to related decisions, patterns, or wiki pages]
```

---

**Step 3.2 — Add Stage 6 closeout steps to governance CLAUDE.md**

Add a Stage 6 section to `hldpro-governance/CLAUDE.md`:

```markdown
## Stage 6 — Closeout Protocol (Required for All Completed Work)

Before marking any task DONE in PROGRESS.md:

1. Fill in `raw/closeouts/YYYY-MM-DD-{task-slug}.md` from TEMPLATE.md
2. Run `hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task-slug}.md`
3. Verify graphify-out/GRAPH_REPORT.md reflects the change (may take one commit cycle)
4. Update PROGRESS.md task status to DONE

Route to `verify-completion` agent for artifact verification before step 4.
```

---

**Step 3.3 — Write closeout-hook.sh**

Create `hldpro-governance/hooks/closeout-hook.sh`:

```bash
#!/bin/bash
# closeout-hook.sh — Stage 6 Karpathy Loop write-back
# Usage: ./hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task}.md

set -e

CLOSEOUT_FILE="$1"
GOVERNANCE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AI_INTEGRATION_ROOT="${GOVERNANCE_ROOT}/../ai-integration-services"

if [ -z "$CLOSEOUT_FILE" ]; then
  echo "ERROR: No closeout file specified."
  echo "Usage: ./hooks/closeout-hook.sh raw/closeouts/YYYY-MM-DD-{task}.md"
  exit 1
fi

if [ ! -f "$CLOSEOUT_FILE" ]; then
  echo "ERROR: Closeout file not found: $CLOSEOUT_FILE"
  exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  HLD Pro — Stage 6 Closeout Hook"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Validate template fields filled
echo "[1/4] Validating closeout template..."
REQUIRED_FIELDS=("Date:" "Repo:" "Task ID:" "Decision Made")
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! grep -q "$field" "$CLOSEOUT_FILE"; then
    echo "ERROR: Required field missing from closeout: $field"
    exit 1
  fi
done
echo "  ✓ Template validated"

# 2. Run graphify --update on ai-integration-services
echo "[2/4] Updating knowledge graph..."
if [ -d "$AI_INTEGRATION_ROOT" ]; then
  cd "$AI_INTEGRATION_ROOT"
  graphify . --update --no-viz 2>&1 | tail -5
  echo "  ✓ Knowledge graph updated"
else
  echo "  ⚠ ai-integration-services not found at $AI_INTEGRATION_ROOT — skipping graph update"
fi

# 3. Remind to create operator_context row
echo "[3/4] operator_context check..."
if grep -q "Yes — row ID:" "$CLOSEOUT_FILE"; then
  echo "  ✓ operator_context row confirmed in closeout"
else
  echo "  ⚠ REMINDER: Create operator_context row for this decision"
  echo "    Table: operator_context"
  echo "    context_type: 'decision'"
  echo "    content: Decision summary from closeout"
  echo "    relevance_tags: extract from closeout content"
fi

# 4. Commit closeout to governance repo
echo "[4/4] Committing closeout..."
cd "$GOVERNANCE_ROOT"
git add "$CLOSEOUT_FILE"
git commit -m "docs(closeout): $(basename $CLOSEOUT_FILE .md)" --no-verify

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✓ Stage 6 Closeout Complete"
echo "  Next: update wiki/ pages listed in closeout"
echo "        run overlord-sweep to wire new wiki entries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

```bash
chmod +x hldpro-governance/hooks/closeout-hook.sh
```

---

**Step 3.4 — Create GitHub Actions raw feed job**

Create `.github/workflows/raw-feed-sync.yml` in `hldpro-governance`:

```yaml
name: Raw Feed Sync
on:
  schedule:
    - cron: '0 6 * * *'  # Daily 6 AM CT (12 UTC)
  workflow_dispatch:

jobs:
  sync-github-issues:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: read
    steps:
      - uses: actions/checkout@v4

      - name: Fetch GitHub issues from governed repos
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ORG: NIBARGERB-HLDPRO
        run: |
          DATE=$(date +%Y-%m-%d)
          mkdir -p raw/github-issues

          for REPO in ai-integration-services HealthcarePlatform local-ai-machine knocktracker; do
            echo "Fetching issues from $REPO..."
            gh issue list \
              --repo "$ORG/$REPO" \
              --state open \
              --json number,title,body,labels,createdAt,updatedAt \
              --limit 50 \
              > /tmp/issues-$REPO.json || true

            # Convert to markdown
            python3 - << 'PYEOF'
import json, sys, os
repo = os.environ.get('CURRENT_REPO', 'unknown')
date = os.environ.get('DATE', 'unknown')
try:
    issues = json.load(open(f'/tmp/issues-{repo}.json'))
    if not issues:
        sys.exit(0)
    lines = [f"# GitHub Issues — {repo}\nDate: {date}\n"]
    for i in issues:
        labels = ', '.join(l['name'] for l in i.get('labels', []))
        lines.append(f"## #{i['number']}: {i['title']}")
        lines.append(f"Labels: {labels or 'none'} | Created: {i['createdAt'][:10]}")
        lines.append("")
        if i.get('body'):
            lines.append(i['body'][:500])
        lines.append("---")
    open(f'raw/github-issues/{date}-{repo}.md', 'w').write('\n'.join(lines))
    print(f"Written: raw/github-issues/{date}-{repo}.md")
except Exception as e:
    print(f"Warning: {e}")
PYEOF
          done
        env:
          CURRENT_REPO: ${{ env.REPO }}
          DATE: ${{ env.DATE }}

      - name: Commit raw feed updates
        run: |
          git config user.name "overlord-bot"
          git config user.email "overlord@hldpro.com"
          git add raw/github-issues/
          git diff --staged --quiet || git commit -m "chore(raw): nightly github issues feed $(date +%Y-%m-%d)"
          git push
```

---

**Step 3.5 — Wire operator_context to raw/operator-context/**

Add this pg_cron job to ai-integration-services (new migration):

```sql
-- Migration: add operator_context -> governance write-back trigger
-- This is a notification trigger — actual file write happens in edge function

CREATE OR REPLACE FUNCTION notify_operator_context_insert()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify(
    'operator_context_new',
    json_build_object(
      'id', NEW.id,
      'context_type', NEW.context_type,
      'content', LEFT(NEW.content, 500),
      'relevance_tags', NEW.relevance_tags,
      'created_at', NEW.created_at
    )::text
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER operator_context_insert_notify
  AFTER INSERT ON operator_context
  FOR EACH ROW EXECUTE FUNCTION notify_operator_context_insert();
```

The edge function `operator-context-bridge` listens for this notification and writes a markdown summary to `raw/operator-context/` via GitHub API. Build this edge function in Phase 3.

---

**Step 3.6 — Add graphify --update to overlord-sweep.yml**

Add to the existing `overlord-sweep.yml` workflow, after the main sweep steps:

```yaml
      - name: Update knowledge graph
        run: |
          pip install graphifyy -q
          cd ai-integration-services
          graphify . --update --no-viz
          cp -r graphify-out/ ../hldpro-governance/graphify-out/

      - name: Commit updated graph
        run: |
          cd hldpro-governance
          git add graphify-out/GRAPH_REPORT.md graphify-out/graph.json
          git diff --staged --quiet || git commit -m "chore(graphify): weekly graph update $(date +%Y-%m-%d)"
          git push
```

---

**Step 3.7 — End-to-end loop validation**

Run one complete task using the full six-stage cycle:

```text
Suggested validation task: "Add wiki/index.md pointer to QUICKREF.md in ai-integration-services"

Stage 1: Research — read wiki/index.md and GRAPH_REPORT.md first
Stage 2: Plan — write locked JSON spec
Stage 3: Specialist Review — run edge-fn-reviewer (n/a for this task — run schema-reviewer)
Stage 4: Alternate Review — optional for low-complexity task
Stage 5: Execute — make the QUICKREF.md change
Stage 6: Closeout — fill TEMPLATE.md, run closeout-hook.sh, verify raw/closeouts/ has new file
```

After closeout, verify:
```bash
# New closeout file exists
ls hldpro-governance/raw/closeouts/

# graphify-out/GRAPH_REPORT.md updated (may need one commit cycle)
git log hldpro-governance/graphify-out/GRAPH_REPORT.md | head -5

# wiki/index.md reflects new decision (after next sweep)
grep -i "quickref" hldpro-governance/wiki/decisions/ -r
```

---

**Step 3.8 — Phase 3 completion check**

```bash
# 1. closeout-hook.sh is executable
ls -la hldpro-governance/hooks/closeout-hook.sh

# 2. Closeout template exists
ls hldpro-governance/raw/closeouts/TEMPLATE.md

# 3. GitHub Actions raw feed workflow exists
ls hldpro-governance/.github/workflows/raw-feed-sync.yml

# 4. Stage 6 closeout steps in governance CLAUDE.md
grep "Stage 6" hldpro-governance/CLAUDE.md

# 5. Loop is observable (at least one closeout file exists from validation task)
ls hldpro-governance/raw/closeouts/*.md | grep -v TEMPLATE
```

---

## HARD RULES FOR THIS IMPLEMENTATION

1. **Never modify STANDARDS.md** without explicit instruction from Benji
2. **Never add new agents** — the four overlord agents are sufficient; extend them, don't multiply them
3. **Never change product code** in ai-integration-services — only CLAUDE.md and .claude/settings.json
4. **Never run graphify on HealthcarePlatform** until HIPAA doc extraction privacy boundary is verified
5. **graphify output lives in hldpro-governance** — never commit graphify-out/ to a product repo
6. **raw/ feeds are append-only** — never delete or overwrite files in raw/
7. **wiki/ is generated/maintained by agents** — never manually edit wiki/ files (except wiki/index.md structure)
8. **The overlord agents remain read-only** — wiki write-back happens in overlord-sweep only, with controlled scope

---

## COMPLETION CRITERIA (ALL THREE PHASES)

The Living Knowledge Base is complete when all of the following are true:

- [ ] `graphify --version` works on local machine
- [ ] `hldpro-governance/graphify-out/GRAPH_REPORT.md` exists with god nodes + communities
- [ ] `hldpro-governance/wiki/index.md` exists and is linked from all 4 overlord agents
- [ ] `hldpro-governance/CLAUDE.md` contains NEVER RESPOND DIRECTLY dispatcher rule
- [ ] `hldpro-governance/raw/` has all four subdirectories with at least one file each
- [ ] `hldpro-governance/agents/overlord-sweep.md` has Wiki Write-Back section
- [ ] `hldpro-governance/hooks/closeout-hook.sh` is executable and tested
- [ ] `.github/workflows/raw-feed-sync.yml` exists and has run at least once
- [ ] One complete six-stage cycle has been run with Stage 6 closeout filed to raw/closeouts/
- [ ] `wiki/decisions/` has at least 5 decision files
- [ ] The Karpathy Loop is observable: a closeout -> graphify update -> wiki entry can be traced end-to-end

---

*HLD Pro Living Knowledge Base Implementation Plan v1.0 — April 2026*
*Three tools. Three strategies. One compounding knowledge system.*
