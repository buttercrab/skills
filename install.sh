#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
exec python3 "$REPO_DIR/scripts/install_skills.py" --repo "$REPO_DIR" "$@"
