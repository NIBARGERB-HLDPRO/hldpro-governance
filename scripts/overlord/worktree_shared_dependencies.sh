#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  worktree_shared_dependencies.sh link --root-checkout PATH --worktree PATH [--artifact PATH ...]
  worktree_shared_dependencies.sh clean --worktree PATH [--artifact PATH ...]

Defaults:
  --artifact node_modules

Allowed artifacts:
  node_modules
  .yarn
  .yarn/cache
  .yarn/install-state.gz
  .pnpm-store

Notes:
  - root checkout and worktree must belong to the same git repo/common dir
  - lockfiles/manifests must match before linking
  - cleanup removes only symlinks previously created by this helper
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $1" >&2
    exit 1
  fi
}

realpath_safe() {
  local target="$1"
  cd "$target" >/dev/null 2>&1 && pwd -P
}

git_path() {
  git -C "$1" rev-parse --git-path "$2"
}

common_dir() {
  local dir
  dir="$(git -C "$1" rev-parse --git-common-dir)"
  if [[ "$dir" != /* ]]; then
    dir="$(cd "$1" && cd "$dir" && pwd -P)"
  else
    dir="$(cd "$dir" && pwd -P)"
  fi
  printf '%s\n' "$dir"
}

in_allowlist() {
  local candidate="$1"
  shift
  local item
  for item in "$@"; do
    if [[ "$candidate" == "$item" ]]; then
      return 0
    fi
  done
  return 1
}

ensure_same_repo() {
  local root="$1"
  local worktree="$2"

  local root_common
  local worktree_common
  root_common="$(common_dir "$root")"
  worktree_common="$(common_dir "$worktree")"

  if [[ "$root_common" != "$worktree_common" ]]; then
    echo "ERROR: root checkout and worktree are not from the same git common dir." >&2
    echo "  root:     $root_common" >&2
    echo "  worktree: $worktree_common" >&2
    exit 1
  fi
}

verify_lockfile_parity() {
  local root="$1"
  local worktree="$2"
  local files=(
    package.json
    package-lock.json
    pnpm-lock.yaml
    pnpm-workspace.yaml
    yarn.lock
    bun.lockb
  )

  local file
  for file in "${files[@]}"; do
    local root_file="$root/$file"
    local worktree_file="$worktree/$file"

    if [[ -e "$root_file" || -e "$worktree_file" ]]; then
      if [[ ! -e "$root_file" || ! -e "$worktree_file" ]]; then
        echo "ERROR: manifest/lockfile mismatch for $file (present in only one checkout)." >&2
        exit 1
      fi
      if ! cmp -s "$root_file" "$worktree_file"; then
        echo "ERROR: manifest/lockfile differs between root checkout and worktree: $file" >&2
        exit 1
      fi
    fi
  done
}

manifest_path() {
  git_path "$1" "shared-dependency-links.txt"
}

write_manifest_entry() {
  local worktree="$1"
  local artifact="$2"
  local manifest
  manifest="$(manifest_path "$worktree")"
  mkdir -p "$(dirname "$manifest")"
  touch "$manifest"
  if ! grep -Fxq "$artifact" "$manifest"; then
    printf '%s\n' "$artifact" >>"$manifest"
  fi
}

remove_manifest_entry() {
  local worktree="$1"
  local artifact="$2"
  local manifest
  manifest="$(manifest_path "$worktree")"
  [[ -f "$manifest" ]] || return 0
  grep -Fxv "$artifact" "$manifest" >"${manifest}.tmp" || true
  mv "${manifest}.tmp" "$manifest"
  if [[ ! -s "$manifest" ]]; then
    rm -f "$manifest"
  fi
}

read_manifest_entries() {
  local worktree="$1"
  local manifest
  manifest="$(manifest_path "$worktree")"
  if [[ -f "$manifest" ]]; then
    cat "$manifest"
  fi
}

load_manifest_into_artifacts() {
  local worktree="$1"
  artifacts=()
  while IFS= read -r artifact_line; do
    if [[ -n "$artifact_line" ]]; then
      artifacts+=("$artifact_line")
    fi
  done < <(read_manifest_entries "$worktree")
}

link_artifact() {
  local root="$1"
  local worktree="$2"
  local artifact="$3"

  local source_path="$root/$artifact"
  local target_path="$worktree/$artifact"

  if [[ ! -e "$source_path" ]]; then
    echo "ERROR: source artifact does not exist in root checkout: $artifact" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$target_path")"

  if [[ -L "$target_path" ]]; then
    local existing
    existing="$(readlink "$target_path")"
    if [[ "$existing" == "$source_path" ]]; then
      write_manifest_entry "$worktree" "$artifact"
      echo "OK already linked: $artifact"
      return 0
    fi
    echo "ERROR: target already exists as a different symlink: $artifact -> $existing" >&2
    exit 1
  fi

  if [[ -e "$target_path" ]]; then
    echo "ERROR: target path already exists and is not a symlink: $artifact" >&2
    exit 1
  fi

  ln -s "$source_path" "$target_path"
  write_manifest_entry "$worktree" "$artifact"
  echo "OK linked: $artifact"
}

cleanup_artifact() {
  local worktree="$1"
  local artifact="$2"
  local target_path="$worktree/$artifact"

  if [[ -L "$target_path" ]]; then
    rm "$target_path"
    remove_manifest_entry "$worktree" "$artifact"
    echo "OK removed: $artifact"
    return 0
  fi

  if [[ -e "$target_path" ]]; then
    echo "ERROR: cleanup target exists but is not a symlink: $artifact" >&2
    exit 1
  fi

  remove_manifest_entry "$worktree" "$artifact"
  echo "OK absent: $artifact"
}

main() {
  require_cmd git

  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi

  local command="$1"
  shift

  local root_checkout=""
  local worktree=""
  local -a artifacts=()
  local -a allowlist=(
    node_modules
    .yarn
    .yarn/cache
    .yarn/install-state.gz
    .pnpm-store
  )

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --root-checkout)
        root_checkout="$2"
        shift 2
        ;;
      --worktree)
        worktree="$2"
        shift 2
        ;;
      --artifact)
        artifacts+=("$2")
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "ERROR: unknown argument: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [[ ${#artifacts[@]} -eq 0 ]]; then
    artifacts=(node_modules)
  fi

  local artifact
  for artifact in "${artifacts[@]}"; do
    if ! in_allowlist "$artifact" "${allowlist[@]}"; then
      echo "ERROR: artifact is not in allowlist: $artifact" >&2
      exit 1
    fi
  done

  if [[ -z "$worktree" ]]; then
    echo "ERROR: --worktree is required." >&2
    exit 1
  fi
  worktree="$(realpath_safe "$worktree")"

  case "$command" in
    link)
      if [[ -z "$root_checkout" ]]; then
        echo "ERROR: --root-checkout is required for link." >&2
        exit 1
      fi
      root_checkout="$(realpath_safe "$root_checkout")"
      ensure_same_repo "$root_checkout" "$worktree"
      verify_lockfile_parity "$root_checkout" "$worktree"
      for artifact in "${artifacts[@]}"; do
        link_artifact "$root_checkout" "$worktree" "$artifact"
      done
      ;;
    clean)
      if [[ ${#artifacts[@]} -eq 1 && "${artifacts[0]}" == "node_modules" ]]; then
        load_manifest_into_artifacts "$worktree"
        if [[ ${#artifacts[@]} -eq 0 ]]; then
          artifacts=(node_modules)
        fi
      fi
      for artifact in "${artifacts[@]}"; do
        cleanup_artifact "$worktree" "$artifact"
      done
      ;;
    *)
      echo "ERROR: unknown command: $command" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
