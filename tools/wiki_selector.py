#!/usr/bin/env python3
"""Wiki selector: discover WIKI_PATH from current working directory.

Uses wikis.yaml registry. Prevents cross-contamination between domains.

Usage (as shell function):
    eval $(python3 wiki_selector.py --cwd "$(pwd)")

Usage (explicit):
    python3 wiki_selector.py --wiki genesis/prism-intel
"""

import argparse
import os
import sys
from pathlib import Path
import yaml

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "wikis.yaml")

# CWD → wiki domain mappings
GENESIS_ROOT = "/root/genesis/companies"
PERSONAL_ROOT = "/root/"


def load_registry():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def resolve_wiki_from_cwd(cwd):
    """Given a cwd path, return the appropriate wiki path."""
    registry = load_registry()
    all_wikis = {}
    if "genesis" in registry:
        all_wikis.update({f"genesis/{k}": v for k, v in registry["genesis"].items()})
    if "personal" in registry:
        all_wikis.update({f"personal/{k}": v for k, v in registry["personal"].items()})
    if "projects" in registry:
        all_wikis.update({f"projects/{k}": v for k, v in registry["projects"].items()})
    if "reference" in registry:
        all_wikis.update({f"reference/{k}": v for k, v in registry["reference"].items()})
    if "meta" in registry:
        all_wikis["meta"] = registry["meta"]

    cwd = os.path.abspath(cwd)

    # Genesis: if cwd is under /root/genesis/companies/<biz>/
    if cwd.startswith(GENESIS_ROOT):
        rest = cwd[len(GENESIS_ROOT):].lstrip("/")
        parts = rest.split("/")
        if parts:
            biz = parts[0]
            key = f"genesis/{biz}"
            if key in all_wikis:
                return all_wikis[key]["path"], key, "genesis"

    # Projects: if cwd is under /root/projects/<proj>/
    PROJECTS_ROOT = "/root/projects"
    if cwd.startswith(PROJECTS_ROOT):
        rest = cwd[len(PROJECTS_ROOT):].lstrip("/")
        parts = rest.split("/")
        if parts:
            proj = parts[0]
            key = f"projects/{proj}"
            if key in all_wikis:
                return all_wikis[key]["path"], key, "projects"

    # Shafira special case for reference: if cwd is /root/shafira/
    # Extract project name from /root/<proj>/
    if cwd.startswith(PERSONAL_ROOT):
        rest = cwd[len(PERSONAL_ROOT):].lstrip("/")
        parts = rest.split("/")
        if parts:
            proj = parts[0]
            key = f"personal/{proj}"
            if key in all_wikis:
                return all_wikis[key]["path"], key, "personal"

    # Meta: if cwd is under ~/.llm-wiki/
    if cwd.startswith(WIKI_ROOT):
        return registry["meta"]["path"], "meta", "meta"

    return None, None, None


def resolve_wiki_by_name(name):
    """Given an explicit wiki key, return its path."""
    registry = load_registry()
    all_wikis = {}
    if "genesis" in registry:
        all_wikis.update({f"genesis/{k}": v for k, v in registry["genesis"].items()})
    if "personal" in registry:
        all_wikis.update({f"personal/{k}": v for k, v in registry["personal"].items()})
    if "projects" in registry:
        all_wikis.update({f"projects/{k}": v for k, v in registry["projects"].items()})
    if "reference" in registry:
        all_wikis.update({f"reference/{k}": v for k, v in registry["reference"].items()})
    if "meta" in registry:
        all_wikis["meta"] = registry["meta"]

    if name in all_wikis:
        return all_wikis[name]["path"], name, all_wikis[name].get("domain", "unknown")
    return None, None, None


def list_available_wikis():
    """Print all available wiki keys."""
    registry = load_registry()
    keys = []
    for domain_name, items in registry.items():
        if isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict) and "path" in v:
                    keys.append(f"{domain_name}/{k}")
    return keys


def main():
    parser = argparse.ArgumentParser(description="Auto-discover WIKI_PATH")
    parser.add_argument("--cwd", type=str, help="Current working directory")
    parser.add_argument("--wiki", type=str, help="Explicit wiki key (e.g., genesis/prism-intel)")
    parser.add_argument("--print-path", action="store_true", help="Print path only")
    parser.add_argument("--export-shell", action="store_true", help="Print export WIKI_PATH=... for shell eval")
    args = parser.parse_args()

    if args.wiki:
        path, key, domain = resolve_wiki_by_name(args.wiki)
    elif args.cwd:
        path, key, domain = resolve_wiki_from_cwd(args.cwd)
    else:
        path, key, domain = resolve_wiki_from_cwd(os.getcwd())

    if path is None:
        print("# No wiki matched for this directory.", file=sys.stderr)
        print("# Available wikis:", file=sys.stderr)
        registry = load_registry()
        for domain_name, items in registry.items():
            if isinstance(items, dict):
                for k, v in items.items():
                    if isinstance(v, dict) and "path" in v:
                        print(f"#   {domain_name}/{k}", file=sys.stderr)
        print("export WIKI_PATH=\"\"", file=sys.stdout)
        sys.exit(1)

    if args.print_path:
        print(os.path.expanduser(path))
    elif args.export_shell:
        print(f'export WIKI_PATH="{os.path.expanduser(path)}"')
        print(f'export WIKI_KEY="{key}"')
        print(f'export WIKI_DOMAIN="{domain}"')
    else:
        print(f"WIKI_PATH={os.path.expanduser(path)} (key={key}, domain={domain})")


if __name__ == "__main__":
    main()
