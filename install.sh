#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_SKILLS_DIR="${REPO_DIR}/skills"
AGENT_SKILLS_DIR="${HOME}/.agents/skills"
CODEX_SKILLS_DIR="${HOME}/.codex/skills"

mkdir -p "$AGENT_SKILLS_DIR" "$CODEX_SKILLS_DIR"

backup_existing() {
  local target_dir="$1"
  local name="$2"
  local target="${target_dir}/${name}"

  if [[ -L "$target" ]]; then
    rm "$target"
    return 0
  fi

  if [[ -e "$target" ]]; then
    local backup_root="${target_dir}/.backup-skills-install-$(date +%Y%m%d%H%M%S)"
    mkdir -p "$backup_root"
    mv "$target" "$backup_root/${name}"
    echo "Backed up ${target} to ${backup_root}/${name}"
  fi
}

link_skill_to_dir() {
  local target_dir="$1"
  local skill_dir="$2"
  local name
  name="$(basename "$skill_dir")"
  local target="${target_dir}/${name}"
  local desired="${skill_dir}"

  [[ -d "$desired" ]] || {
    echo "missing skill: $desired" >&2
    exit 1
  }

  if [[ -L "$target" && "$(readlink "$target")" == "$desired" ]]; then
    return 0
  fi

  backup_existing "$target_dir" "$name"
  ln -s "$desired" "$target"
}

install_skills_to_dir() {
  local target_dir="$1"
  local skill_dir

  for skill_dir in "${REPO_SKILLS_DIR}"/*; do
    [[ -f "${skill_dir}/SKILL.md" ]] || continue
    link_skill_to_dir "$target_dir" "$skill_dir"
  done
}

install_skills_to_dir "$AGENT_SKILLS_DIR"
install_skills_to_dir "$CODEX_SKILLS_DIR"

if command -v go >/dev/null 2>&1; then
  (
    cd "${REPO_SKILLS_DIR}/front-agent-orchestration"
    go build -o scripts/front-agent-bin ./cmd/front-agent
  )
else
  echo "Go is not available; front-agent will fall back to go run only after Go is installed." >&2
fi

echo "Installed repo skills into ${AGENT_SKILLS_DIR} and ${CODEX_SKILLS_DIR}."
