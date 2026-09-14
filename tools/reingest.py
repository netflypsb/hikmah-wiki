#!/usr/bin/env python3
"""
Re-ingest tool: check watchlist.md for changed sources and re-ingest if drifted.

Usage:
    python3 reingest.py --check                # Check all watchlist entries
    python3 reingest.py --wiki <key>          # Check entries for one wiki
    python3 reingest.py --simulate             # Show what would change, don't write
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime
from urllib.request import urlopen

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
WATCHLIST_PATH = os.path.join(WIKI_ROOT, ".config", "watchlist.md")


def sha256_of_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def download_url(url):
    """Download URL and return body text."""
    try:
        with urlopen(url, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, str(e)
    return None, "unknown error"


def parse_watchlist():
    """Parse watchlist.md into entries."""
    if not os.path.exists(WATCHLIST_PATH):
        return []
    with open(WATCHLIST_PATH) as f:
        content = f.read()
    entries = []
    for line in content.split("\n"):
        if line.startswith("|") and "URL" not in line and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                entries.append({
                    "url": parts[1],
                    "wiki": parts[2],
                    "last_ingested": parts[3],
                    "stored_sha": parts[4],
                    "frequency": parts[5],
                    "status": parts[6],
                })
    return entries


def write_watchlist(entries):
    header = """# Ingest Watchlist

> Track online sources that change over time.
> The `reingest.py` tool polls these weekly.
> Last updated: {date} | Entries: {count}

| URL | Wiki | Last Ingested | SHA256 Body | Frequency | Status |
|-----|------|---------------|-------------|-----------|--------|
""".format(date=datetime.now().strftime("%Y-%m-%d"), count=len(entries))

    body = ""
    for e in entries:
        body += f"| {e['url']} | {e['wiki']} | {e['last_ingested']} | {e['stored_sha']} | {e['frequency']} | {e['status']} |\n"

    with open(WATCHLIST_PATH, "w") as f:
        f.write(header + body)


def check_entry(entry, simulate=False):
    url = entry["url"]
    wiki = entry["wiki"]
    stored_sha = entry["stored_sha"]

    print(f"  Checking: {url[:60]}...")
    body_or_err = download_url(url)
    if isinstance(body_or_err, tuple):
        # Error
        print(f"    ❌ FAILED: {body_or_err[1]}")
        return False, body_or_err[1]

    new_sha = sha256_of_text(body_or_err)
    if new_sha == stored_sha:
        print(f"    ✅ Unchanged (sha: {new_sha})")
        return False, None

    print(f"    ⚠️  CHANGED! old: {stored_sha} → new: {new_sha}")
    if not simulate:
        # Update watchlist
        entry["stored_sha"] = new_sha
        entry["last_ingested"] = datetime.now().strftime("%Y-%m-%d")
        entry["status"] = "updated"
        # Here: trigger actual ingest via llm-wiki skill (future integration)
        # For now, we just flag it
    return True, None


def main():
    parser = argparse.ArgumentParser(description="Re-ingest watchlist checker")
    parser.add_argument("--check", action="store_true", help="Check all entries")
    parser.add_argument("--wiki", type=str, help="Filter to one wiki")
    parser.add_argument("--simulate", action="store_true", help="Dry run: show changes without updating")
    args = parser.parse_args()

    if not os.path.exists(WATCHLIST_PATH):
        print("No watchlist found.")
        sys.exit(0)

    entries = parse_watchlist()
    if not entries:
        print("Watchlist is empty.")
        sys.exit(0)

    if args.wiki:
        entries = [e for e in entries if e["wiki"] == args.wiki]
        if not entries:
            print(f"No entries for wiki '{args.wiki}'.")
            sys.exit(0)

    print(f"Checking {len(entries)} watchlist entr{'y' if len(entries)==1 else 'ies'}...")
    changed_count = 0
    for entry in entries:
        changed, err = check_entry(entry, simulate=args.simulate)
        if changed:
            changed_count += 1

    if changed_count > 0 and not args.simulate:
        write_watchlist(entries)
        print(f"\nUpdated watchlist with {changed_count} changed entr{'y' if changed_count==1 else 'ies'}.")
        print("Run the llm-wiki ingest workflow for each flagged source.")
    elif changed_count > 0:
        print(f"\n{changed_count} entr{'y' if changed_count==1 else 'ies'} changed but --simulate: no writes.")
    else:
        print("\nAll sources unchanged.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("--check")
    main()
