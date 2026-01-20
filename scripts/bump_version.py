#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bump the version of the agent-skills plugin.

Usage:
    python scripts/bump_version.py major|minor|patch

Examples:
    python scripts/bump_version.py patch   # 1.0.0 -> 1.0.1
    python scripts/bump_version.py minor   # 1.0.0 -> 1.1.0
    python scripts/bump_version.py major   # 1.0.0 -> 2.0.0
"""

import argparse
import json
import sys
from pathlib import Path


def get_root() -> Path:
    """Get the project root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse a semantic version string into (major, minor, patch)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def bump_version(version: str, bump_type: str) -> str:
    """Bump a semantic version."""
    major, minor, patch = parse_version(version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def load_json(path: Path) -> dict:
    """Load a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """Save a JSON file with proper formatting."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def bump_plugin_version(bump_type: str) -> None:
    """Bump the version in marketplace.json."""
    root = get_root()

    # Path
    marketplace_path = root / ".claude-plugin" / "marketplace.json"

    if not marketplace_path.exists():
        print(f"✗ marketplace.json not found at {marketplace_path}")
        sys.exit(1)

    # Load file
    marketplace = load_json(marketplace_path)

    # Get current version from metadata
    current_version = marketplace.get("metadata", {}).get("version", "1.0.0")
    new_version = bump_version(current_version, bump_type)

    print(f"Bumping agent-skills: {current_version} → {new_version}")

    # Update marketplace.json metadata version
    if "metadata" not in marketplace:
        marketplace["metadata"] = {}
    marketplace["metadata"]["version"] = new_version
    save_json(marketplace_path, marketplace)
    print(f"✓ Updated {marketplace_path}")

    print(f"\n🎉 Version bumped successfully!")
    print(f"\nNext steps:")
    print(f"  1. Review changes: git diff")
    print(f"  2. Commit: git commit -am 'chore: bump version to {new_version}'")
    print(f"  3. Push: git push")


def show_version() -> None:
    """Show current version."""
    root = get_root()
    marketplace_path = root / ".claude-plugin" / "marketplace.json"

    if marketplace_path.exists():
        marketplace = load_json(marketplace_path)
        version = marketplace.get("metadata", {}).get("version", "unknown")
        print(f"Current version: {version}")
    else:
        print("✗ marketplace.json not found")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Bump agent-skills plugin version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Semantic versioning:
  major  Breaking changes           (1.0.0 → 2.0.0)
  minor  New features, refactoring  (1.0.0 → 1.1.0)
  patch  Bug fixes, docs            (1.0.0 → 1.0.1)

Examples:
  %(prog)s patch
  %(prog)s minor
  %(prog)s --show
        """
    )

    parser.add_argument(
        "bump_type",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version bump type"
    )
    parser.add_argument(
        "--show", "-s",
        action="store_true",
        help="Show current version"
    )

    args = parser.parse_args()

    # Show mode
    if args.show:
        show_version()
        return

    # Validate args
    if not args.bump_type:
        parser.print_help()
        sys.exit(1)

    bump_plugin_version(args.bump_type)


if __name__ == "__main__":
    main()
