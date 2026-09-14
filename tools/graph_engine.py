#!/usr/bin/env python3
"""
Graph Engine — NetworkX-based wikilink graph for all LLM Wiki domains.

Builds a DirectedGraph from [[wikilink]] references across all wiki files.
Supports: orphans, hubs, communities, blast radius, structural gaps.

Usage:
    python3 graph_engine.py --build                # Build/rebuild all graphs
    python3 graph_engine.py --wiki genesis/prism-intel --orphans
    python3 graph_engine.py --wiki genesis/prism-intel --hubs --top 10
    python3 graph_engine.py --blast-radius "chapter-13"  # What pages need review if this changes
    python3 graph_engine.py --communities        # Louvain clustering
    python3 graph_engine.py --structural-gaps    # Same tag, no path
    python3 graph_engine.py --all-wikis --summary
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

try:
    import networkx as nx
    from networkx.algorithms import community as nx_comm
except ImportError:
    print("ERROR: networkx required. Install: pip install networkx")
    sys.exit(1)

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "wikis.yaml")
CACHE_DIR = os.path.join(WIKI_ROOT, ".cache", "graphs")

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TAG_RE = re.compile(r"^tags:\s*\[(.*?)\]", re.MULTILINE)


def load_registry():
    import yaml
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def discover_wikis(registry):
    """Return list of (key, path) for all wikis."""
    wikis = []
    for domain, items in registry.items():
        if domain == "meta" and isinstance(items, dict) and "path" in items:
            wikis.append(("meta", os.path.expanduser(items["path"])))
        elif isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict) and "path" in v:
                    wikis.append((f"{domain}/{k}", os.path.expanduser(v["path"])))
    return wikis


def extract_wikilinks(content):
    """Extract [[wikilink]] targets from markdown content."""
    return WIKILINK_RE.findall(content)


def extract_frontmatter_tags(content):
    """Extract tags from YAML frontmatter."""
    m = TAG_RE.search(content)
    if m:
        tags_str = m.group(1)
        return [t.strip().strip('"').strip("'") for t in tags_str.split(",") if t.strip()]
    return []


def extract_title(content, filepath):
    """Extract title from frontmatter or first H1."""
    fm = FRONTMATTER_RE.search(content)
    if fm:
        yaml_text = fm.group(1)
        title_match = re.search(r'^title:\s*"([^"]+)"', yaml_text, re.MULTILINE)
        if title_match:
            return title_match.group(1)
    # Fallback: first H1
    h1 = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if h1:
        return h1.group(1).strip()
    return os.path.basename(filepath)


def build_wiki_graph(wiki_path, wiki_key):
    """Build a DiGraph for one wiki."""
    G = nx.DiGraph()
    G.graph["wiki_key"] = wiki_key
    G.graph["wiki_path"] = wiki_path
    G.graph["built_at"] = datetime.now().isoformat()

    md_files = []
    for root, _, files in os.walk(wiki_path):
        # Skip raw/, .cache/, .git
        if any(skip in root for skip in ["/raw/", "/.cache/", "/.git/"]):
            continue
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))

    pages = {}
    for fp in md_files:
        rel = os.path.relpath(fp, wiki_path)
        # Remove .md extension for node ID
        node_id = rel.replace(".md", "")
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"  Warning: could not read {fp}: {e}")
            continue

        title = extract_title(content, fp)
        tags = extract_frontmatter_tags(content)
        pages[node_id] = {"path": fp, "title": title, "tags": tags}
        G.add_node(node_id, title=title, tags=tags, path=fp)

    # Second pass: build edges
    for node_id, info in pages.items():
        with open(info["path"], "r", encoding="utf-8") as f:
            content = f.read()
        links = extract_wikilinks(content)
        for target in links:
            # Handle cross-wiki links: "genesis/prism-intel/entities/foo"
            if "hof" not in target and "meta" not in target and "/" in target:
                # This is a cross-wiki link — note it but don't add as edge (different graph)
                G.add_edge(node_id, target, cross_wiki=True)
            else:
                # Local link — resolve relative to node path
                target_clean = target.replace(".md", "").lstrip("/")
                if target_clean in pages:
                    G.add_edge(node_id, target_clean, cross_wiki=False)

    G.graph["page_count"] = G.number_of_nodes()
    G.graph["link_count"] = G.number_of_edges()
    return G


def build_all_graphs():
    """Build graphs for all wikis + a federated graph."""
    registry = load_registry()
    wikis = discover_wikis(registry)

    os.makedirs(CACHE_DIR, exist_ok=True)
    all_graphs = {}
    fed_G = nx.DiGraph()

    print(f"Building graphs for {len(wikis)} wikis...")
    for key, path in wikis:
        print(f"\n  {key}:")
        if not os.path.exists(path):
            print(f"    SKIP: path does not exist: {path}")
            continue
        G = build_wiki_graph(path, key)
        all_graphs[key] = G

        # Cache to JSON (adjacency + node attributes)
        cache_path = os.path.join(CACHE_DIR, f"{key.replace('/', '_')}.json")
        serialized = {
            "wiki_key": key,
            "built_at": G.graph["built_at"],
            "nodes": {},
            "edges": [],
        }
        for n, attr in G.nodes(data=True):
            serialized["nodes"][n] = {k: v for k, v in attr.items() if k != "path"}
        for u, v, attr in G.edges(data=True):
            serialized["edges"].append({"from": u, "to": v, **attr})
        with open(cache_path, "w") as f:
            json.dump(serialized, f, indent=2)
        print(f"    Cached to {cache_path}")

        # Add to federated graph with namespace
        for n, attr in G.nodes(data=True):
            fed_G.add_node(f"{key}/{n}", wiki=key, **attr)
        for u, v, attr in G.edges(data=True):
            if attr.get("cross_wiki"):
                fed_G.add_edge(f"{key}/{u}", v, **attr)
            else:
                fed_G.add_edge(f"{key}/{u}", f"{key}/{v}", **attr)

    # Cache federated graph
    fed_path = os.path.join(CACHE_DIR, "_federated.json")
    fed_serial = {
        "wiki_key": "_federated",
        "built_at": datetime.now().isoformat(),
        "nodes": {n: {k: v for k, v in attr.items() if k != "path"}
                  for n, attr in fed_G.nodes(data=True)},
        "edges": [{"from": u, "to": v, **attr} for u, v, attr in fed_G.edges(data=True)],
    }
    with open(fed_path, "w") as f:
        json.dump(fed_serial, f, indent=2)
    print(f"\n  Federated graph cached to {fed_path}")
    print(f"  Total nodes: {fed_G.number_of_nodes()}, edges: {fed_G.number_of_edges()}")

    return all_graphs, fed_G


def load_cached_graph(wiki_key):
    cache_path = os.path.join(CACHE_DIR, f"{wiki_key.replace('/', '_')}.json")
    if not os.path.exists(cache_path):
        return None
    with open(cache_path) as f:
        data = json.load(f)
    G = nx.DiGraph()
    G.graph["wiki_key"] = data["wiki_key"]
    G.graph["built_at"] = data["built_at"]
    for n, attr in data["nodes"].items():
        G.add_node(n, **attr)
    for e in data["edges"]:
        G.add_edge(e["from"], e["to"], cross_wiki=e.get("cross_wiki", False))
    return G


def report_orphans(G):
    """Pages with zero inbound links."""
    orphans = [n for n in G.nodes() if G.in_degree(n) == 0]
    if not orphans:
        print("  ✅ No orphan pages found.")
        return []
    print(f"  ⚠️  {len(orphans)} orphan page(s) (no inbound links):")
    for n in sorted(orphans):
        title = G.nodes[n].get("title", n)
        print(f"    - {n}: {title}")
    return orphans


def report_hubs(G, top=10):
    """Pages with highest out-degree (most links)."""
    if G.number_of_nodes() == 0:
        print("  Graph is empty.")
        return []
    hubs = sorted(G.nodes(), key=lambda n: G.out_degree(n), reverse=True)[:top]
    print(f"  Top {top} hub pages (most outbound links):")
    for n in hubs:
        title = G.nodes[n].get("title", n)
        print(f"    {G.out_degree(n):3d} links → {n}: {title}")
    return hubs


def report_blast_radius(G, node, max_depth=3):
    """What pages need review if this node changes."""
    if node not in G:
        print(f"  Node '{node}' not found in graph.")
        return
    reachable = set()
    for depth in range(1, max_depth + 1):
        for successor in nx.single_source_shortest_path_length(G, node, cutoff=depth):
            if successor != node:
                reachable.add((successor, depth))
    print(f"  Blast radius for '{node}':")
    print(f"    {len(reachable)} pages reachable within {max_depth} hops")
    by_depth = defaultdict(list)
    for succ, d in sorted(reachable, key=lambda x: x[1]):
        by_depth[d].append(succ)
    for d in sorted(by_depth):
        print(f"    Hop {d}: {len(by_depth[d])} page(s)")
        for n in by_depth[d][:5]:
            title = G.nodes[n].get("title", n)
            print(f"      - {n}: {title}")
        if len(by_depth[d]) > 5:
            print(f"      ... and {len(by_depth[d]) - 5} more")


def report_communities(G):
    """Louvain clustering for topic discovery."""
    if G.number_of_nodes() == 0:
        print("  Graph is empty, no communities.")
        return []
    # Louvain needs undirected
    UG = G.to_undirected()
    try:
        comms = nx_comm.louvain_communities(UG, seed=42)
    except Exception as e:
        print(f"  Could not compute communities: {e}")
        return []
    print(f"  Detected {len(comms)} community clusters:")
    for i, c in enumerate(sorted(comms, key=len, reverse=True)[:10]):
        titles = [UG.nodes[n].get("title", n) for n in list(c)[:3]]
        print(f"    Cluster {i+1}: {len(c)} nodes — e.g., {', '.join(titles)}")
    return comms


def report_structural_gaps(G):
    """Nodes sharing tags but no path between them."""
    by_tag = defaultdict(list)
    for n, attr in G.nodes(data=True):
        for tag in attr.get("tags", []):
            by_tag[tag].append(n)

    gaps = []
    for tag, nodes in by_tag.items():
        if len(nodes) < 2:
            continue
        # Check if any pair is disconnected
        disconnected = []
        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                if not nx.has_path(G.to_undirected(), a, b):
                    disconnected.append((a, b))
        if disconnected:
            gaps.append((tag, disconnected))
    if not gaps:
        print("  ✅ No structural gaps found (all same-tag nodes reachable).")
        return []
    print(f"  ⚠️  {len(gaps)} tag(s) with structural gaps:")
    for tag, pairs in gaps[:5]:
        print(f"    Tag '{tag}': {len(pairs)} disconnected pair(s)")
    return gaps


def run_lint(G):
    """Run all lint checks on a graph."""
    issues = 0
    issues += len(report_orphans(G))
    report_hubs(G, top=5)
    report_structural_gaps(G)
    return issues


def main():
    parser = argparse.ArgumentParser(description="LLM Wiki Graph Engine")
    parser.add_argument("--build", action="store_true", help="Build all graphs")
    parser.add_argument("--wiki", type=str, help="Target wiki (e.g., genesis/prism-intel)")
    parser.add_argument("--orphans", action="store_true", help="Find orphan pages")
    parser.add_argument("--hubs", action="store_true", help="Find hub pages")
    parser.add_argument("--top", type=int, default=10, help="Limit for hubs")
    parser.add_argument("--blast-radius", type=str, metavar="NODE", help="Compute blast radius for node")
    parser.add_argument("--communities", action="store_true", help="Detect communities")
    parser.add_argument("--structural-gaps", action="store_true", help="Find structural gaps")
    parser.add_argument("--lint", action="store_true", help="Run full lint on target wiki")
    parser.add_argument("--all-wikis", action="store_true", help="Target all wikis for operations")
    parser.add_argument("--summary", action="store_true", help="Print summary of all wikis")
    args = parser.parse_args()

    if args.build:
        build_all_graphs()

    if args.summary:
        registry = load_registry()
        wikis = discover_wikis(registry)
        print("\n=== Wiki Graph Summary ===\n")
        print(f"{'Wiki':<35} {'Nodes':>6} {'Edges':>6} {'Orphans':>8} {'Hubs':>6}")
        print("-" * 70)
        for key, path in sorted(wikis):
            G = load_cached_graph(key)
            if G is None:
                print(f"{key:<35} {'(not built)':>20}")
                continue
            orphans = len([n for n in G.nodes() if G.in_degree(n) == 0])
            print(f"{key:<35} {G.number_of_nodes():>6} {G.number_of_edges():>6} {orphans:>8} {max((G.out_degree(n) for n in G.nodes()), default=0):>6}")
        return

    if args.wiki:
        G = load_cached_graph(args.wiki)
        if G is None:
            print(f"Graph for '{args.wiki}' not found. Run --build first.")
            sys.exit(1)
        print(f"\n=== {args.wiki} ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges) ===\n")

        if args.orphans:
            report_orphans(G)
        if args.hubs:
            report_hubs(G, top=args.top)
        if args.blast_radius:
            report_blast_radius(G, args.blast_radius)
        if args.communities:
            report_communities(G)
        if args.structural_gaps:
            report_structural_gaps(G)
        if args.lint:
            run_lint(G)

    if args.all_wikis and not args.build:
        registry = load_registry()
        wikis = discover_wikis(registry)
        for key, path in sorted(wikis):
            G = load_cached_graph(key)
            if G is None:
                continue
            print(f"\n=== {key} ===")
            if args.orphans:
                report_orphans(G)
            if args.hubs:
                report_hubs(G, top=args.top)
            if args.lint:
                run_lint(G)

    if not any([args.build, args.summary, args.wiki, args.all_wikis]):
        parser.print_help()


if __name__ == "__main__":
    main()
