#!/usr/bin/env python3
"""
Federated Query — search across all wikis for a term.

Usage:
    python3 federated_query.py "PostgreSQL"          # Search all wikis
    python3 federated_query.py "postgresql" --rank     # Ranked results
    python3 federated_query.py "AML" --wiki reference/hoffbrand-9th-edition
    python3 federated_query.py "chapter-13" --exact    # Exact match in filenames
"""

import argparse
import os
import re
import sys
import yaml
from collections import defaultdict

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "wikis.yaml")


def load_registry():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def discover_wikis(registry):
    wikis = []
    for domain, items in registry.items():
        if domain == "meta" and isinstance(items, dict) and "path" in items:
            wikis.append(("meta", os.path.expanduser(items["path"])))
        elif isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict) and "path" in v:
                    wikis.append((f"{domain}/{k}", os.path.expanduser(v["path"])))
    return wikis


def search_wiki(wiki_key, wiki_path, query, exact=False):
    """Search all .md files in a wiki for query string."""
    results = []
    query_lower = query.lower()

    for root, _, files in os.walk(wiki_path):
        if any(skip in root for skip in ["/raw/", "/.cache/", "/.git/"]):
            continue
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, "r", encoding="utf-8") as fh:
                    content = fh.read()
            except Exception:
                continue

            rel = os.path.relpath(filepath, wiki_path)
            page_id = rel.replace(".md", "")

            # Check filename
            filename_match = query_lower in f.lower()

            # Check content
            lines = content.split("\n")
            matches = []
            for i, line in enumerate(lines, 1):
                line_lower = line.lower()
                if query_lower in line_lower:
                    matches.append((i, line.strip()[:120]))

            if matches or filename_match:
                # Extract title
                title_match = re.search(r'title:\s*"([^"]+)"', content)
                title = title_match.group(1) if title_match else page_id
                results.append({
                    "wiki": wiki_key,
                    "page": page_id,
                    "title": title,
                    "matches": len(matches),
                    "filename_match": filename_match,
                    "sample": matches[0][1] if matches else "",
                })
    return results


def main():
    parser = argparse.ArgumentParser(description="Federated search across all wikis")
    parser.add_argument("query", help="Search term")
    parser.add_argument("--wiki", type=str, help="Search only one wiki")
    parser.add_argument("--exact", action="store_true", help="Exact filename match only")
    parser.add_argument("--rank", action="store_true", help="Score and rank results")
    parser.add_argument("--top", type=int, default=20, help="Limit results")
    args = parser.parse_args()

    registry = load_registry()
    wikis = discover_wikis(registry)

    if args.wiki:
        wikis = [(k, p) for k, p in wikis if k == args.wiki]
        if not wikis:
            print(f"Wiki '{args.wiki}' not found.")
            return

    all_results = []
    for key, path in wikis:
        results = search_wiki(key, path, args.query, exact=args.exact)
        all_results.extend(results)

    if not all_results:
        print(f'No results for "{args.query}".')
        return

    if args.rank:
        # Simple scoring: filename match = +10, content match = +matches found
        for r in all_results:
            r["score"] = (10 if r["filename_match"] else 0) + r["matches"]
        all_results.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n=== Federated Query Results: '{args.query}' ===\n")
    print(f"{'Score/Rank':<12} {'Wiki':<30} {'Page':<25} {'Title':<40}")
    print("-" * 110)

    for r in all_results[:args.top]:
        if args.rank:
            display = f"{r['score']:<12}"
        else:
            display = f"{'':<12}"
        wiki_short = r["wiki"].replace("genesis/", "g/").replace("personal/", "p/").replace("projects/", "pr/").replace("reference/", "ref/")
        print(f"{display} {wiki_short:<30} {r['page']:<25} {r['title'][:38]:<40}")
        if r["sample"]:
            print(f"{'':<12} {'':<30} ... {r['sample']}")

    if len(all_results) > args.top:
        print(f"\n... and {len(all_results) - args.top} more results.")


if __name__ == "__main__":
    # Handle no-argument case
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        main()
    else:
        print("Usage: python3 federated_query.py <query> [options]")
