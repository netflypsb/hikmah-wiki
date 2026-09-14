#!/usr/bin/env python3
"""
Wiki Analytics — track metrics over time.

Usage:
    python3 analytics.py --summary               # Overview across all wikis
    python3 analytics.py --wiki <key>          # Per-wiki detail
    python3 analytics.py --trend pages_created   # Show trend for metric
    python3 analytics.py --health-check          # Flag metrics outside thresholds
"""

import argparse
import json
import os
from datetime import datetime
from collections import defaultdict

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
STATS_DIR = os.path.join(WIKI_ROOT, ".stats")
GRAPH_CACHE = os.path.join(WIKI_ROOT, ".cache", "graphs")


def load_graph(wiki_key):
    cache_path = os.path.join(GRAPH_CACHE, f"{wiki_key.replace('/', '_')}.json")
    if not os.path.exists(cache_path):
        return None
    with open(cache_path) as f:
        return json.load(f)


def analyze_wiki(wiki_key):
    """Return metrics dict for a wiki."""
    data = load_graph(wiki_key)
    if data is None:
        return {"error": "Graph not built. Run graph_engine.py --build first."}

    # Parse graph
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])
    node_list = list(nodes.keys())
    edge_list = [(e["from"], e["to"]) for e in edges]

    # Build adjacency
    inbound = defaultdict(int)
    outbound = defaultdict(int)
    for u, v in edge_list:
        outbound[u] += 1
        inbound[v] += 1

    # Metrics
    page_count = len(node_list)
    orphan_count = sum(1 for n in node_list if inbound.get(n, 0) == 0 and outbound.get(n, 0) == 0)
    orphan_rate = (orphan_count / page_count * 100) if page_count > 0 else 0
    max_out_degree = max((outbound[n] for n in node_list), default=0)
    avg_out_degree = sum(outbound.values()) / page_count if page_count > 0 else 0
    has_content = page_count > 3  # SCHEMA, index, log are boilerplate

    return {
        "wiki": wiki_key,
        "page_count": page_count,
        "edge_count": len(edges),
        "orphan_count": orphan_count,
        "orphan_rate": round(orphan_rate, 1),
        "max_out_degree": max_out_degree,
        "avg_out_degree": round(avg_out_degree, 2),
        "boilerplate_only": not has_content or page_count <= 3,
        "status": "⚠️  empty" if not has_content else "✅ active" if orphan_rate < 30 else "⚠️  orphaned" if orphan_rate < 70 else "❌ dead",
    }


def health_check(all_metrics):
    """Flag metrics outside thresholds."""
    issues = []
    for m in all_metrics:
        if m.get("boilerplate_only"):
            issues.append((m["wiki"], "No content pages (boilerplate only)"))
        elif m["orphan_rate"] > 50:
            issues.append((m["wiki"], f"Orphan rate {m['orphan_rate']}% (>50%)"))
        elif m["orphan_rate"] > 30:
            issues.append((m["wiki"], f"Orphan rate {m['orphan_rate']}% (>30%)"))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Wiki Analytics Dashboard")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--wiki", type=str)
    parser.add_argument("--health-check", action="store_true")
    args = parser.parse_args()

    if args.wiki:
        metrics = analyze_wiki(args.wiki)
        print(json.dumps(metrics, indent=2))
        return

    # Discover all wikis
    import yaml
    registry_path = os.path.join(WIKI_ROOT, ".config", "wikis.yaml")
    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    wiki_keys = []
    for domain, items in registry.items():
        if domain == "meta" and isinstance(items, dict) and "path" in items:
            wiki_keys.append("meta")
        elif isinstance(items, dict):
            for k in items:
                if isinstance(items[k], dict) and "path" in items[k]:
                    wiki_keys.append(f"{domain}/{k}")

    all_metrics = [analyze_wiki(k) for k in wiki_keys]

    if args.summary:
        print(f"\n=== Wiki Analytics Summary ===\n")
        print(f"{'Wiki':<35} {'Pages':>6} {'Edges':>6} {'Orphans':>7} {'Rate':>5} {'Max Out':>7} {'Avg Out':>7} {'Status'}")
        print("-" * 90)
        for m in sorted(all_metrics, key=lambda x: x.get("page_count", 0), reverse=True):
            if "error" in m:
                print(f"{m['wiki']:<35} {m['error']}")
                continue
            wiki_short = m["wiki"].replace("genesis/", "g/").replace("personal/", "p/").replace("projects/", "pr/").replace("reference/", "ref/")
            print(f"{wiki_short:<35} {m['page_count']:>6} {m['edge_count']:>6} {m['orphan_count']:>7} {m['orphan_rate']:>4.0f}% {m['max_out_degree']:>7} {m['avg_out_degree']:>7.1f} {m['status']}")

    if args.health_check:
        issues = health_check(all_metrics)
        if issues:
            print(f"\n=== Health Check: {len(issues)} issue(s) ===\n")
            for wiki, issue in issues:
                print(f"  ⚠️  {wiki}: {issue}")
        else:
            print("\n✅ All wikis within health thresholds.")

    # Save summary to stats
    os.makedirs(STATS_DIR, exist_ok=True)
    stats_path = os.path.join(STATS_DIR, f"summary-{datetime.now().strftime('%Y%m%d')}.json")
    with open(stats_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "wikis": all_metrics,
        }, f, indent=2)


if __name__ == "__main__":
    main()
