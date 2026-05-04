#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_SKILLS_DIR="${REPO_DIR}/skills"
SKILLS_DIR="${HOME}/.agents/skills"

mkdir -p "$SKILLS_DIR"

backup_existing() {
  local name="$1"
  local target="${SKILLS_DIR}/${name}"

  if [[ -L "$target" ]]; then
    rm "$target"
    return 0
  fi

  if [[ -e "$target" ]]; then
    local backup_root="${SKILLS_DIR}/.backup-skills-install-$(date +%Y%m%d%H%M%S)"
    mkdir -p "$backup_root"
    mv "$target" "$backup_root/${name}"
    echo "Backed up ${target} to ${backup_root}/${name}"
  fi
}

link_skill() {
  local name="$1"
  local target="${SKILLS_DIR}/${name}"
  local desired="${REPO_SKILLS_DIR}/${name}"

  [[ -d "$desired" ]] || {
    echo "missing skill: $desired" >&2
    exit 1
  }

  if [[ -L "$target" && "$(readlink "$target")" == "$desired" ]]; then
    return 0
  fi

  backup_existing "$name"
  ln -s "$desired" "$target"
}

link_skill agent-mail
link_skill front-agent-orchestration

if command -v go >/dev/null 2>&1; then
  (
    cd "${REPO_SKILLS_DIR}/front-agent-orchestration"
    go build -o scripts/front-agent-bin ./cmd/front-agent
  )
else
  echo "Go is not available; front-agent will fall back to go run only after Go is installed." >&2
fi

echo "Installed repo skills into ${SKILLS_DIR}."
