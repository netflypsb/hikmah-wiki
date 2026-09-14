#!/usr/bin/env python3
"""
scan_wikis.py — Scan the server for LLM Wiki directories.

Detects wikis by looking for the "LLM Wiki signature":
  - Contains a SCHEMA.md file
  - Contains an index.md file
  - Contains an entities/ or concepts/ directory
  - Contains a log.md file

Scans known root directories:
  - /root/.llm-wiki/
  - /root/tarbiyyah/
  - /root/qaradawi-library/
  - /root/shafira/
  - /root/projects/

Outputs a JSON array of discovered wikis with metadata.
Updates /root/.llm-wiki/.config/wiki-registry.md if --update flag is set.
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Directories to scan for wikis
SCAN_ROOTS = [
    Path("/root/.llm-wiki"),
    Path("/root/tarbiyyah"),
    Path("/root/qaradawi-library"),
    Path("/root/shafira"),
    Path("/root/projects"),
]

# Wiki signature: must have SCHEMA.md or index.md, plus at least one of:
# entities/, concepts/, comparisons/, queries/
def is_wiki_dir(path: Path) -> bool:
    """Check if a directory looks like an LLM Wiki."""
    if not path.is_dir():
        return False
    # Must have SCHEMA.md or index.md
    has_schema = (path / "SCHEMA.md").exists()
    has_index = (path / "index.md").exists()
    if not (has_schema or has_index):
        return False
    # Must have at least one content directory
    content_dirs = ["entities", "concepts", "comparisons", "queries", "surahs", "chapters"]
    has_content = any((path / d).is_dir() for d in content_dirs)
    if not has_content:
        return False
    # Exclude node_modules, .git, etc.
    if path.name.startswith(".") and path.name != ".llm-wiki":
        return False
    if path.name in ("node_modules", "__pycache__", ".git", ".next", "out", "dist"):
        return False
    return True

def get_wiki_info(path: Path) -> dict[str, object]:
    """Gather metadata about a wiki directory."""
    # Resolve symlinks so the path points to the real directory
    real_path = path.resolve()
    info = {
        "path": str(real_path),
        "symlink_path": str(path) if str(path) != str(real_path) else None,
        "name": real_path.name,
    }

    # Git status
    git_dir = (real_path / ".git")
    if git_dir.exists():
        info["has_git"] = True
        # Get remote
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=str(real_path), capture_output=True, text=True, timeout=5
            )
            info["remote"] = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            info["remote"] = None
        # Get last commit
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%h %ci"],
                cwd=str(real_path), capture_output=True, text=True, timeout=5
            )
            info["last_commit"] = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            info["last_commit"] = None
        # Tracked file count
        try:
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=str(real_path), capture_output=True, text=True, timeout=5
            )
            info["tracked_files"] = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
        except Exception:
            info["tracked_files"] = 0
    else:
        info["has_git"] = False
        info["remote"] = None
        info["last_commit"] = None
        info["tracked_files"] = 0

    # Size (du -sh, excluding raw/ if .gitignore excludes it)
    try:
        result = subprocess.run(
            ["du", "-sh", str(real_path)],
            capture_output=True, text=True, timeout=10
        )
        info["size"] = result.stdout.split("\t")[0].strip() if result.returncode == 0 else "?"
    except Exception:
        info["size"] = "?"

    return info

def scan_for_wikis() -> list:
    """Scan all root directories for LLM Wiki signatures."""
    found = []
    seen_paths = set()

    for root in SCAN_ROOTS:
        if not root.exists():
            continue

        # Check if root itself is a wiki
        if is_wiki_dir(root):
            real = str(root.resolve())
            if real not in seen_paths:
                found.append(get_wiki_info(root))
                seen_paths.add(real)
                seen_paths.add(str(root))

        # Scan subdirectories (depth 1-2)
        for child in root.iterdir():
            if not child.is_dir():
                continue
            if child.name.startswith(".") and child.name != ".llm-wiki":
                continue
            if child.name in ("node_modules", "__pycache__", ".git", ".next", "out", "dist", "raw"):
                continue

            if is_wiki_dir(child):
                real = str(child.resolve())
                if real not in seen_paths:
                    found.append(get_wiki_info(child))
                    seen_paths.add(real)
                    seen_paths.add(str(child))

            # Depth 2
            for grandchild in child.iterdir():
                if not grandchild.is_dir():
                    continue
                if grandchild.name.startswith(".") or grandchild.name in ("node_modules", "__pycache__", ".git", "raw", "out", "dist"):
                    continue
                if is_wiki_dir(grandchild):
                    real = str(grandchild.resolve())
                    if real not in seen_paths:
                        found.append(get_wiki_info(grandchild))
                        seen_paths.add(real)
                        seen_paths.add(str(grandchild))

    return found

def update_registry(wikis: list, registry_path: Path):
    """Update the wiki-registry.md file with discovered wikis."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# LLM Wiki Registry — Server Wiki Inventory",
        f"# Auto-maintained by scan_wikis.py (called from cron-backup.sh)",
        f"# Last scan: {now}",
        "",
        "## Active Wikis",
        "",
        "| # | Wiki Name | Path | Git Remote | Tracked Files | Size | Has Git? |",
        "|---|-----------|------|------------|---------------|------|----------|",
    ]

    for i, w in enumerate(wikis, 1):
        remote = w.get("remote") or "(none)"
        if remote and "github.com" in remote:
            # Shorten GitHub URLs and strip any embedded tokens
            remote = remote.replace("https://github.com/", "github.com/").replace(".git", "")
            # Strip credentials: anything before github.com
            if "github.com/" in remote:
                remote = "github.com/" + remote.split("github.com/")[-1]
        tracked = str(w.get("tracked_files", "?"))
        size = w.get("size", "?")
        has_git = "✅" if w.get("has_git") else "❌"
        lines.append(f"| {i} | {w['name']} | `{w['path']}` | {remote} | {tracked} | {size} | {has_git} |")

    lines.extend([
        "",
        f"## Summary",
        f"- Total wikis discovered: {len(wikis)}",
        f"- Wikis with git: {sum(1 for w in wikis if w.get('has_git'))}",
        f"- Wikis with remote: {sum(1 for w in wikis if w.get('remote'))}",
        f"- Wikis without backup: {sum(1 for w in wikis if not w.get('remote'))}",
        f"- Last scan: {now}",
        "",
        "## Notes",
        "- This file is auto-regenerated by `scan_wikis.py` on each cron backup run.",
        "- Manual edits will be overwritten. To add a wiki manually, create it at the path",
        "  and it will be auto-discovered on the next scan.",
        "- Wikis are identified by the signature: SCHEMA.md or index.md + content directories",
        "  (entities/, concepts/, comparisons/, queries/, surahs/, chapters/).",
    ])

    registry_path.write_text("\n".join(lines))
    return registry_path

def main():
    parser = argparse.ArgumentParser(description="Scan server for LLM Wikis")
    parser.add_argument("--update", action="store_true", help="Update wiki-registry.md")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    wikis = scan_for_wikis()

    if args.json:
        print(json.dumps(wikis, indent=2, ensure_ascii=False))
    else:
        print(f"Discovered {len(wikis)} wikis:")
        for w in wikis:
            git_status = "✅" if w.get("has_git") else "❌"
            remote = w.get("remote") or "(no remote)"
            print(f"  {git_status} {w['name']:30s} {w['path']:50s} {remote}")

    if args.update:
        registry_path = Path("/root/.llm-wiki/.config/wiki-registry.md")
        update_registry(wikis, registry_path)
        if not args.json:
            print(f"\nRegistry updated: {registry_path}")

    # Report wikis without backup (only in non-JSON mode)
    if not args.json:
        no_backup = [w for w in wikis if not w.get("remote")]
        if no_backup:
            print(f"\n⚠ Wikis without git remote ({len(no_backup)}):")
            for w in no_backup:
                print(f"  {w['name']:30s} {w['path']}")

if __name__ == "__main__":
    main()