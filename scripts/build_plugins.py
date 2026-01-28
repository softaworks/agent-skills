#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build per-plugin distribution directories.

Reads marketplace.json and creates a self-contained directory for each plugin
under dist/plugins/, so installing a single plugin only caches its own files
instead of the entire repository.

Usage:
    python scripts/build_plugins.py           # Build all plugins
    python scripts/build_plugins.py --dry-run # Preview without writing
    python scripts/build_plugins.py --verbose # Detailed output
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def get_root() -> Path:
    """Get the project root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent


def load_json(path: Path) -> dict:
    """Load a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """Save a JSON file with proper formatting."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def extract_paths(plugin: dict) -> list[tuple[str, str]]:
    """Extract (source_path, type) pairs from a plugin entry.

    Returns list of (relative_path, component_type) where component_type
    is 'skill_dir', 'agent_file', or 'command_file'.
    """
    paths = []

    for skill_path in plugin.get("skills", []):
        # "./skills/mermaid-diagrams" -> "skills/mermaid-diagrams"
        clean = skill_path.lstrip("./")
        paths.append((clean, "skill_dir"))

    for agent_path in plugin.get("agents", []):
        # "./agents/ui-ux-designer.md" -> "agents/ui-ux-designer.md"
        clean = agent_path.lstrip("./")
        paths.append((clean, "agent_file"))

    for command_path in plugin.get("commands", []):
        # "./commands/sync-branch.md" -> "commands/sync-branch.md"
        clean = command_path.lstrip("./")
        paths.append((clean, "command_file"))

    return paths


def build_plugin(root: Path, dist_dir: Path, plugin: dict,
                 dry_run: bool = False, verbose: bool = False) -> int:
    """Build a single plugin's distribution directory.

    Returns the number of files copied.
    """
    name = plugin["name"]
    plugin_dir = dist_dir / name
    paths = extract_paths(plugin)
    file_count = 0

    if not paths:
        if verbose:
            print(f"  skip {name}: no skills/agents/commands defined")
        return 0

    if not dry_run:
        plugin_dir.mkdir(parents=True, exist_ok=True)

    for rel_path, path_type in paths:
        src = root / rel_path
        dst = plugin_dir / rel_path

        if path_type == "skill_dir":
            if not src.is_dir():
                print(f"  ERROR: skill directory not found: {src}", file=sys.stderr)
                sys.exit(1)
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, dst, dirs_exist_ok=True)
            copied = sum(1 for _ in src.rglob("*") if _.is_file())
            file_count += copied
            if verbose:
                print(f"  {name}: copied {rel_path}/ ({copied} files)")

        elif path_type in ("agent_file", "command_file"):
            if not src.is_file():
                print(f"  ERROR: file not found: {src}", file=sys.stderr)
                sys.exit(1)
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            file_count += 1
            if verbose:
                print(f"  {name}: copied {rel_path}")

    return file_count


def build_all(dry_run: bool = False, verbose: bool = False) -> None:
    """Build distribution directories for all plugins."""
    root = get_root()
    marketplace_path = root / ".claude-plugin" / "marketplace.json"

    if not marketplace_path.exists():
        print(f"marketplace.json not found at {marketplace_path}", file=sys.stderr)
        sys.exit(1)

    marketplace = load_json(marketplace_path)
    plugins = marketplace.get("plugins", [])
    dist_dir = root / "dist" / "plugins"

    mode = "[DRY RUN] " if dry_run else ""
    print(f"{mode}Building {len(plugins)} plugins...")

    # Clean existing dist
    if not dry_run and dist_dir.exists():
        shutil.rmtree(dist_dir)

    total_files = 0
    built_count = 0

    for plugin in plugins:
        name = plugin["name"]
        files = build_plugin(root, dist_dir, plugin, dry_run, verbose)
        total_files += files
        if files > 0:
            built_count += 1

        # Update source path
        plugin["source"] = f"./dist/plugins/{name}"

    # Write updated marketplace.json
    if not dry_run:
        save_json(marketplace_path, marketplace)

    # Summary
    if dist_dir.exists():
        total_size = sum(f.stat().st_size for f in dist_dir.rglob("*") if f.is_file())
        size_str = f"{total_size / 1024:.0f}KB" if total_size < 1024 * 1024 else f"{total_size / 1024 / 1024:.1f}MB"
    else:
        size_str = "N/A"

    print(f"\n{mode}Done: {built_count} plugins built, {total_files} files, {size_str} total")
    if not dry_run:
        print(f"Updated marketplace.json source paths")


def main():
    parser = argparse.ArgumentParser(
        description="Build per-plugin distribution directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Each plugin gets its own directory under dist/plugins/ containing only
the files it needs. This prevents installing one plugin from caching
the entire repository.

Examples:
  %(prog)s              # Build all plugins
  %(prog)s --dry-run    # Preview without writing
  %(prog)s --verbose    # Show detailed output
        """
    )

    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview changes without writing files"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()
    build_all(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
