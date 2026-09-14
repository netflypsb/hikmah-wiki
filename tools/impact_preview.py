#!/usr/bin/env python3
"""
Impact Preview — before writing during ingest, compute blast radius.

Usage:
    python3 impact_preview.py --wiki <key> --entity "Entity Name" [--simulate]
    python3 impact_preview.py --wiki genesis/prism-intel --source <path-to-source>
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
GRAPH_CACHE = os.path.join(WIKI_ROOT, ".cache", "graphs")

def load_graph(wiki_key):
    cache_path = os.path.join(GRAPH_CACHE, f"{wiki_key.replace('/', '_')}.json")
    if not os.path.exists(cache_path):
        return None
    with open(cache_path) as f:
        return json.load(f)

def preview_impact(wiki_key, entity_slug):
    data = load_graph(wiki_key)
    if data is None:
        print(f"Graph for '{wiki_key}' not built. Run graph_engine.py --build first.")
        return

    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    # Build reverse edges
    inbound = defaultdict(list)
    for e in edges:
        inbound[e["to"]].append(e["from"])

    # Check if entity exists
    direct_affected = inbound.get(entity_slug, [])

    # BFS for blast radius
    visited = set()
    queue = [(n, 1) for n in direct_affected]
    blast = []
    while queue:
        current, depth = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        blast.append((current, depth))
        for e in edges:
            if e["from"] == current and e["to"] not in visited:
                queue.append((e["to"], depth + 1))

    print(f"\n  Impact Preview: '{entity_slug}' in {wiki_key}\n")
    print(f"    Direct dependents ({len(direct_affected)}):")
    for d in direct_affected:
        title = nodes.get(d, {}).get("title", d)
        print(f"      → {d}: {title}")

    if blast:
        print(f"\n    Blast radius ({len(blast)} total affected within {max(d for _, d in blast)} hops):")
        by_depth = defaultdict(list)
        for n, d in blast:
            by_depth[d].append(n)
        for d in sorted(by_depth):
            print(f"      Hop {d}: {len(by_depth[d])} page(s)")
            for n in by_depth[d][:3]:
                title = nodes.get(n, {}).get("title", n)
                print(f"        - {n}: {title}")
            if len(by_depth[d]) > 3:
                print(f"        ... and {len(by_depth[d]) - 3} more")

    return len(direct_affected), len(blast)


def preview_source(wiki_key, source_text):
    """Identify entities/concepts in source text and show affected pages."""
    data = load_graph(wiki_key)
    if data is None:
        print(f"Graph for '{wiki_key}' not built.")
        return

    # Simple heuristic: find matching node titles in source text
    source_lower = source_text.lower()
    matched = []
    for slug, attr in data.get("nodes", {}).items():
        title = attr.get("title", "").lower()
        if title and len(title) > 4 and title in source_lower:
            matched.append(slug)

    if not matched:
        print(f"  No existing pages seem referenced by this source.")
        print(f"  This would likely CREATE new pages, not UPDATE existing ones.")
        return

    print(f"\n  Source Preview for '{wiki_key}':")
    print(f"  Matched {len(matched)} existing page(s) that appear in source text:\n")
    for m in matched[:5]:
        title = data["nodes"].get(m, {}).get("title", m)
        print(f"    '{m}': {title}")
        preview_impact(wiki_key, m)


def main():
    parser = argparse.ArgumentParser(description="Impact Preview for Wiki Changes")
    parser.add_argument("--wiki", type=str, required=True)
    parser.add_argument("--entity", type=str, help="Existing entity slug to preview")
    parser.add_argument("--source", type=str, help="Path to source text file")
    args = parser.parse_args()

    if args.entity:
        preview_impact(args.wiki, args.entity)
    elif args.source:
        with open(args.source, "r", encoding="utf-8") as f:
            text = f.read()
        preview_source(args.wiki, text)
    else:
        print("Use --entity or --source.")
        sys.exit(1)


if __name__ == "__main__":
    main()
