#!/usr/bin/env python3
"""
quota_check.py — Disk quota, rotation, and auto-archive for the LLM Wiki Hub.

Usage:
    python3 quota_check.py [--summary] [--enforce] [--wiki <key>]

Rules:
    - Max 500 MB per wiki (business or personal)
    - When exceeded: flag oldest raw/ files without outbound links for archive
    - Archive target: ~/.llm-wiki/_archive/{wiki}/
    - log.md rotation at 500 entries (older lines removed, summary header kept)
    - raw/ sources older than 1 year without cross-references → auto-archive
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WIKI_ROOT = Path.home() / ".llm-wiki"
WIKIS_YAML = WIKI_ROOT / ".config" / "wikis.yaml"
ARCHIVE_ROOT = WIKI_ROOT / "_archive"
MAX_WIKI_MB = 500
LOG_MAX_ENTRIES = 500
RAW_AGE_DAYS = 365


def load_wikis():
    """Load wiki registry from wikis.yaml."""
    import yaml
    with open(WIKIS_YAML) as f:
        data = yaml.safe_load(f)
    wikis = {}
    for tier in ["genesis", "personal", "projects", "reference"]:
        if tier in data:
            for key, cfg in data[tier].items():
                wikis[key] = {**cfg, "tier": tier, "key": key}
    if "meta" in data:
        wikis["meta"] = {**data["meta"], "tier": "meta", "key": "meta"}
    return wikis


def get_wiki_path(key, cfg):
    """Resolve wiki path from config."""
    raw = cfg.get("path", "")
    if raw.startswith("~/"):
        return Path.home() / raw[2:]
    return Path(raw)


def du_mb(path):
    """Return total MB used by path (recursive)."""
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / (1024 * 1024)


def count_lines(path):
    """Count lines in a file."""
    try:
        with open(path) as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_raw_files(wiki_path):
    """List all files under wiki_path/raw/ with metadata."""
    raw_dir = wiki_path / "raw"
    if not raw_dir.exists():
        return []
    files = []
    for root, _dirs, fnames in os.walk(raw_dir):
        for f in fnames:
            p = Path(root) / f
            stat = p.stat()
            files.append({
                "path": p,
                "size": p.stat().st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                "age_days": (datetime.now(timezone.utc) - datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)).days,
            })
    return sorted(files, key=lambda x: x["mtime"])


def has_outbound_links(raw_file, wiki_path):
    """Check if any .md file in the wiki references this raw file by name."""
    # Simple heuristic: does any markdown file contain the filename (or basename) as a link or mention?
    basename = raw_file["path"].name
    stem = raw_file["path"].stem
    for md in wiki_path.rglob("*.md"):
        if md.name == "log.md":
            continue
        try:
            text = md.read_text()
            if basename in text or stem in text:
                return True
        except Exception:
            pass
    return False


def rotate_log(wiki_path, enforce=False):
    """Rotate log.md if it exceeds LOG_MAX_ENTRIES lines."""
    log_file = wiki_path / "log.md"
    if not log_file.exists():
        return 0
    lines = count_lines(log_file)
    if lines <= LOG_MAX_ENTRIES:
        return 0
    removed = lines - LOG_MAX_ENTRIES
    if enforce:
        with open(log_file) as f:
            all_lines = f.readlines()
        # Keep the first line (title/header) + last N entries
        header = all_lines[:1] if all_lines else []
        keep = all_lines[-LOG_MAX_ENTRIES:]
        with open(log_file, "w") as f:
            f.writelines(header + ["\n", f"_Auto-rotated: {removed} older entries archived to log_archive.md_\n\n"])
            f.writelines(keep)
        archive = wiki_path / "log_archive.md"
        with open(archive, "a") as f:
            f.writelines(all_lines[1:lines - LOG_MAX_ENTRIES])
    return removed


def archive_raw(wiki_path, key, enforce=False):
    """Archive raw files that are old and unreferenced."""
    raw_files = get_raw_files(wiki_path)
    to_archive = []
    for f in raw_files:
        if f["age_days"] > RAW_AGE_DAYS and not has_outbound_links(f, wiki_path):
            to_archive.append(f)
    if enforce and to_archive:
        dest_dir = ARCHIVE_ROOT / key / "raw"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in to_archive:
            target = dest_dir / f["path"].relative_to(wiki_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f["path"]), str(target))
    return to_archive


def check_wiki(key, cfg, enforce=False):
    """Run all quota checks for one wiki."""
    wiki_path = get_wiki_path(key, cfg)
    if not wiki_path.exists():
        return {"key": key, "exists": False}

    size_mb = du_mb(wiki_path)
    over_quota = size_mb > MAX_WIKI_MB
    log_rotated = rotate_log(wiki_path, enforce)
    archived = archive_raw(wiki_path, key, enforce)

    return {
        "key": key,
        "tier": cfg.get("tier", "?"),
        "exists": True,
        "size_mb": round(size_mb, 2),
        "over_quota": over_quota,
        "quota_limit_mb": MAX_WIKI_MB,
        "log_rotated": log_rotated,
        "archived_files": len(archived),
        "archived_details": [
            {"file": str(a["path"].relative_to(wiki_path)), "age_days": a["age_days"], "size_kb": round(a["size"] / 1024, 1)}
            for a in archived
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="LLM Wiki quota and rotation checker")
    parser.add_argument("--wiki", help="Check a single wiki key")
    parser.add_argument("--enforce", action="store_true", help="Actually rotate logs and archive files")
    parser.add_argument("--summary", action="store_true", help="Print summary table")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    wikis = load_wikis()
    if args.wiki:
        if args.wiki not in wikis:
            print(f"Unknown wiki: {args.wiki}", file=sys.stderr)
            sys.exit(1)
        keys = [args.wiki]
    else:
        keys = list(wikis.keys())

    results = []
    for k in keys:
        results.append(check_wiki(k, wikis[k], enforce=args.enforce))

    if args.json:
        print(json.dumps(results, indent=2, default=str))
        return

    if args.summary or not args.json:
        # Print table
        print(f"{'Wiki':<20} {'Tier':<12} {'Size MB':<10} {'Quota':<8} {'Log Δ':<8} {'Archived':<10}")
        print("-" * 70)
        total = 0
        for r in results:
            if not r["exists"]:
                print(f"{r['key']:<20} {'?':<12} {'N/A':<10} {'N/A':<8} {'N/A':<8} {'N/A':<10}")
                continue
            total += r["size_mb"]
            status = "⚠️ OVER" if r["over_quota"] else "OK"
            log_str = str(r["log_rotated"]) if r["log_rotated"] else "-"
            arch_str = str(r["archived_files"]) if r["archived_files"] else "-"
            print(f"{r['key']:<20} {r['tier']:<12} {r['size_mb']:<10.1f} {status:<8} {log_str:<8} {arch_str:<10}")
        print("-" * 70)
        print(f"{'TOTAL':<20} {'':<12} {total:<10.1f}")
        if args.enforce:
            print("\n✅ Enforcement applied: logs rotated, files archived.")
        else:
            print("\nℹ️  Dry-run. Use --enforce to apply changes.")


if __name__ == "__main__":
    main()
