#!/usr/bin/env python3
"""Scaffold new wikis from the wikis.yaml registry.

Usage:
    python3 scaffold-wiki.py --all          # Scaffold all registered wikis
    python3 scaffold-wiki.py --wiki <name>  # Scaffold one wiki
"""

import argparse
import os
import sys
from datetime import datetime
from string import Template
import yaml

WIKI_ROOT = os.path.expanduser("~/.llm-wiki")
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "wikis.yaml")
TEMPLATES_DIR = os.path.join(WIKI_ROOT, ".tools", "templates")

SUBDIRS = [
    "raw/articles", "raw/papers", "raw/transcripts", "raw/assets",
    "entities", "concepts", "comparisons", "queries", "claims",
]


def load_registry():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def load_template(name):
    path = os.path.join(TEMPLATES_DIR, f"{name}.template")
    with open(path) as f:
        return f.read()


def scaffold_wiki(wiki_key, wiki_info):
    path = os.path.expanduser(wiki_info["path"])
    domain = wiki_info.get("domain", "general")
    created = wiki_info.get("created", datetime.now().strftime("%Y-%m-%d"))

    # Create subdirectories
    for sub in SUBDIRS:
        os.makedirs(os.path.join(path, sub), exist_ok=True)

    # Write SCHEMA.md
    schema_template = load_template("SCHEMA.md")
    schema = Template(schema_template).safe_substitute(
        DOMAIN=domain,
        CREATED_DATE=created,
    )
    schema_path = os.path.join(path, "SCHEMA.md")
    if not os.path.exists(schema_path):
        with open(schema_path, "w") as f:
            f.write(schema)
        print(f"  Created {schema_path}")
    else:
        print(f"  Exists {schema_path}")

    # Write index.md
    index_template = load_template("index.md")
    index = Template(index_template).safe_substitute(
        LAST_UPDATED=created,
        TOTAL_PAGES="0",
    )
    index_path = os.path.join(path, "index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w") as f:
            f.write(index)
        print(f"  Created {index_path}")
    else:
        print(f"  Exists {index_path}")

    # Write log.md
    log_template = load_template("log.md")
    log = Template(log_template).safe_substitute(
        CREATED_DATE=created,
        DOMAIN=domain,
    )
    log_path = os.path.join(path, "log.md")
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write(log)
        print(f"  Created {log_path}")
    else:
        print(f"  Exists {log_path}")

    print(f"Done: {wiki_key}")


def main():
    parser = argparse.ArgumentParser(description="Scaffold LLM Wikis")
    parser.add_argument("--all", action="store_true", help="Scaffold all registered wikis")
    parser.add_argument("--wiki", type=str, help="Scaffold a specific wiki key")
    args = parser.parse_args()

    registry = load_registry()

    # Flatten the registry into a single dict
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

    if args.all:
        for key, info in sorted(all_wikis.items()):
            print(f"Scaffolding {key}...")
            scaffold_wiki(key, info)
    elif args.wiki:
        if args.wiki not in all_wikis:
            print(f"Error: wiki '{args.wiki}' not found in registry.")
            print("Available:", ", ".join(sorted(all_wikis.keys())))
            sys.exit(1)
        print(f"Scaffolding {args.wiki}...")
        scaffold_wiki(args.wiki, all_wikis[args.wiki])
    else:
        parser.print_help()
        sys.exit(1)

    print("Scaffolding complete.")


if __name__ == "__main__":
    main()
