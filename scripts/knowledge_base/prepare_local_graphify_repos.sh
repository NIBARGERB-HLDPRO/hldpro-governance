#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  prepare_local_graphify_repos.sh link [--base-dir PATH]
  prepare_local_graphify_repos.sh clean

Purpose:
  Create or remove helper-managed symlinks under repos/ so manifest-driven
  graphify validation can run from an isolated hldpro-governance worktree.

Defaults:
  --base-dir <governance parent>/..  (the HLDPRO repo root that contains sibling repos)

Managed repos:
  ai-integration-services
  HealthcarePlatform
  local-ai-machine
  knocktracker
  ASC-Evaluator
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LINK_ROOT="${REPO_ROOT}/repos"
MANIFEST_PATH="$(git -C "${REPO_ROOT}" rev-parse --git-path graphify-local-repo-links.txt)"

REPOS=(
  "ai-integration-services"
  "HealthcarePlatform"
  "local-ai-machine"
  "knocktracker"
  "ASC-Evaluator"
)

default_base_dir() {
  if [[ "$(basename "$(dirname "${REPO_ROOT}")")" == "_worktrees" ]]; then
    cd "${REPO_ROOT}/../.." >/dev/null 2>&1 && pwd -P
  else
    cd "${REPO_ROOT}/.." >/dev/null 2>&1 && pwd -P
  fi
}

record_link() {
  local name="$1"
  mkdir -p "$(dirname "${MANIFEST_PATH}")"
  touch "${MANIFEST_PATH}"
  if ! grep -Fxq "${name}" "${MANIFEST_PATH}"; then
    printf '%s\n' "${name}" >> "${MANIFEST_PATH}"
  fi
}

remove_record() {
  local name="$1"
  [[ -f "${MANIFEST_PATH}" ]] || return 0
  grep -Fxv "${name}" "${MANIFEST_PATH}" > "${MANIFEST_PATH}.tmp" || true
  mv "${MANIFEST_PATH}.tmp" "${MANIFEST_PATH}"
  [[ -s "${MANIFEST_PATH}" ]] || rm -f "${MANIFEST_PATH}"
}

link_repo() {
  local base_dir="$1"
  local name="$2"
  local source="${base_dir}/${name}"
  local target="${LINK_ROOT}/${name}"

  if [[ ! -d "${source}" ]]; then
    echo "ERROR: sibling repo not found: ${source}" >&2
    exit 1
  fi

  mkdir -p "${LINK_ROOT}"

  if [[ -L "${target}" ]]; then
    local existing
    existing="$(readlink "${target}")"
    if [[ "${existing}" == "${source}" ]]; then
      record_link "${name}"
      echo "OK already linked: ${name}"
      return 0
    fi
    echo "ERROR: target already linked elsewhere: ${target} -> ${existing}" >&2
    exit 1
  fi

  if [[ -e "${target}" ]]; then
    echo "ERROR: target exists and is not a helper-managed symlink: ${target}" >&2
    exit 1
  fi

  ln -s "${source}" "${target}"
  record_link "${name}"
  echo "OK linked: ${name}"
}

clean_repo() {
  local name="$1"
  local target="${LINK_ROOT}/${name}"

  if [[ -L "${target}" ]]; then
    rm "${target}"
    remove_record "${name}"
    echo "OK removed: ${name}"
    return 0
  fi

  if [[ -e "${target}" ]]; then
    echo "ERROR: target exists but is not a symlink: ${target}" >&2
    exit 1
  fi

  remove_record "${name}"
  echo "OK absent: ${name}"
}

main() {
  [[ $# -ge 1 ]] || { usage; exit 1; }
  local command="$1"
  shift

  case "${command}" in
    link)
      local base_dir
      base_dir="$(default_base_dir)"
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --base-dir)
            base_dir="$2"
            shift 2
            ;;
          -h|--help)
            usage
            exit 0
            ;;
          *)
            echo "ERROR: unknown argument: $1" >&2
            exit 1
            ;;
        esac
      done
      local repo
      for repo in "${REPOS[@]}"; do
        link_repo "${base_dir}" "${repo}"
      done
      ;;
    clean)
      local repo
      for repo in "${REPOS[@]}"; do
        clean_repo "${repo}"
      done
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown command: ${command}" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
