#!/bin/bash
set -euo pipefail

repo_path="${1:-.}"
scanner_repo="https://github.com/el-zachariah/ai-agent-safety-starter-pack.git"
tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

echo "Cloning free agent preflight scanner..." >&2
git clone --depth 1 "$scanner_repo" "$tmp_dir/agent-preflight" >/dev/null 2>&1

echo "Running local preflight against: $repo_path" >&2
python3 "$tmp_dir/agent-preflight/agent_preflight_lite.py" "$repo_path" --json
