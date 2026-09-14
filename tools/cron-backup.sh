#!/bin/bash
# ~/.llm-wiki/.tools/cron-backup.sh
# Weekly backup of the LLM Wiki Hub AND all independent wiki repos.
# Called by Hermes cron job (40263c86856a).
#
# This script:
# 1. Scans the server for LLM Wiki directories (via scan_wikis.py)
# 2. Updates the wiki registry (.config/wiki-registry.md)
# 3. Commits + pushes the .llm-wiki hub repo
# 4. For each independent wiki with a git remote, commits + pushes it
# 5. Reports disk usage via quota_check.py

set -e

WIKI_ROOT="$HOME/.llm-wiki"
LOG="$WIKI_ROOT/.stats/backup.log"
TIMESTAMP="$(date -Iseconds)"

# Ensure log directory exists
mkdir -p "$WIKI_ROOT/.stats"

echo "[$TIMESTAMP] === LLM Wiki Weekly Backup Started ===" >> "$LOG"

# ── Step 1: Scan for wikis and update registry ──────────────────────
echo "[$TIMESTAMP] Scanning for wikis..." >> "$LOG"
python3 "$WIKI_ROOT/.tools/scan_wikis.py" --update >> "$LOG" 2>&1 || true

# Get the list of independent wikis with git remotes (excluding .llm-wiki itself)
# We read from the scanner output by re-running it and parsing JSON
WIKIS_JSON=$(python3 "$WIKI_ROOT/.tools/scan_wikis.py" --json 2>/dev/null || echo "[]")

# ── Step 2: Backup the .llm-wiki hub repo ────────────────────────────
echo "[$TIMESTAMP] Backing up .llm-wiki hub..." >> "$LOG"
cd "$WIKI_ROOT"

HUB_PUSHED=false
if ! git diff --quiet || ! git diff --cached --quiet; then
    MSG="auto: weekly wiki snapshot $(date +%F_%H-%M)"
    git add -A
    git commit -m "$MSG" >> "$LOG" 2>&1 || true
    git push origin master >> "$LOG" 2>&1 || git push origin main >> "$LOG" 2>&1 || true
    HUB_PUSHED=true
    echo "[$TIMESTAMP] Hub pushed: $MSG" >> "$LOG"
else
    echo "[$TIMESTAMP] Hub: no changes to commit" >> "$LOG"
fi

# ── Step 3: Backup independent wiki repos with remotes ───────────────
# Parse the JSON to get wiki paths that have remotes and are NOT inside .llm-wiki
INDEPENDENT_WIKIS=$(echo "$WIKIS_JSON" | python3 -c "
import json, sys
wikis = json.load(sys.stdin)
for w in wikis:
    path = w.get('path', '')
    remote = w.get('remote')
    has_git = w.get('has_git', False)
    # Skip wikis inside .llm-wiki (they're covered by the hub repo)
    if path.startswith('$WIKI_ROOT'):
        continue
    # Skip if no git or no remote
    if not has_git or not remote:
        continue
    print(path)
" 2>/dev/null)

WIKI_COUNT=0
FAILED_COUNT=0

for WIKI_PATH in $INDEPENDENT_WIKIS; do
    if [ ! -d "$WIKI_PATH/.git" ]; then
        continue
    fi

    WIKI_COUNT=$((WIKI_COUNT + 1))
    WIKI_NAME=$(basename "$WIKI_PATH")
    echo "[$TIMESTAMP] Backing up: $WIKI_NAME ($WIKI_PATH)" >> "$LOG"

    cd "$WIKI_PATH"

    # Check for changes
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$TIMESTAMP]   $WIKI_NAME: no changes" >> "$LOG"
        continue
    fi

    MSG="auto: weekly wiki backup $(date +%F_%H-%M)"
    git add -A >> "$LOG" 2>&1 || true
    git commit -m "$MSG" >> "$LOG" 2>&1 || true

    # Determine branch
    BRANCH=$(git branch --show-current 2>/dev/null || echo "master")
    if git push origin "$BRANCH" >> "$LOG" 2>&1; then
        echo "[$TIMESTAMP]   $WIKI_NAME: pushed ($BRANCH)" >> "$LOG"
    else
        echo "[$TIMESTAMP]   $WIKI_NAME: PUSH FAILED" >> "$LOG"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
done

# ── Step 4: Quota check ──────────────────────────────────────────────
echo "[$TIMESTAMP] Running quota check..." >> "$LOG"
python3 "$WIKI_ROOT/.tools/quota_check.py" --summary >> "$LOG" 2>&1 || true

# ── Step 5: Summary report ──────────────────────────────────────────
echo "[$TIMESTAMP] === Backup Complete ===" >> "$LOG"
echo "[$TIMESTAMP] Hub pushed: $HUB_PUSHED | Independent wikis: $WIKI_COUNT | Failed: $FAILED_COUNT" >> "$LOG"

# Output summary for cron job delivery
if [ "$FAILED_COUNT" -gt 0 ]; then
    echo "BACKUP WARNING: $FAILED_COUNT wiki repos failed to push."
    echo "Hub pushed: $HUB_PUSHED"
    echo "Independent wikis backed up: $WIKI_COUNT (failed: $FAILED_COUNT)"
else
    echo "BACKUP OK: Hub pushed=$HUB_PUSHED, Independent wikis=$WIKI_COUNT, all successful."
fi