#!/usr/bin/env bash
# deploy-hldpro-sim.sh <consumer-repo-path> [--dry-run]
# Installs hldpro-sim package + managed personas into a consumer repo.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOVERNANCE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SIM_PKG="$GOVERNANCE_ROOT/packages/hldpro-sim"
PERSONAS_SRC="$SIM_PKG/personas"
PINNED_SHA="fed5ead670cf6834e5c73bffcaf64e41cc483fce"
VERSION="0.1.0"
TAG="hldpro-sim-v0.1.0"

usage() { echo "Usage: $0 <consumer-repo-path> [--dry-run]"; exit 1; }

[[ $# -lt 1 ]] && usage
CONSUMER="$1"
DRY_RUN=false
[[ "${2:-}" == "--dry-run" ]] && DRY_RUN=true

log() { echo "[deploy-hldpro-sim] $*"; }
drylog() { echo "[deploy-hldpro-sim][DRY-RUN] would: $*"; }
run() { $DRY_RUN && drylog "$*" || eval "$*"; }

[[ -d "$SIM_PKG" ]] || { echo "ERROR: $SIM_PKG not found"; exit 1; }

if ! $DRY_RUN; then
  [[ -d "$CONSUMER" ]] || { echo "ERROR: consumer path '$CONSUMER' does not exist"; exit 1; }
fi

log "Installing hldpro-sim $VERSION into $CONSUMER"

# Step 1: install package
INSTALL_METHOD="pip-editable"
if $DRY_RUN; then
  drylog "pip install -e $SIM_PKG (or fallback: directory copy to $CONSUMER/hldpro-sim/)"
else
  if python3 -m pip install -e "$SIM_PKG" --quiet 2>/dev/null; then
    log "pip-editable install succeeded"
  else
    log "pip-editable failed — falling back to directory copy"
    INSTALL_METHOD="directory-copy"
    cp -r "$SIM_PKG" "$CONSUMER/hldpro-sim"
    log "copied $SIM_PKG → $CONSUMER/hldpro-sim"
  fi
fi

# Step 2: deploy managed personas (read-only)
PERSONAS_DEST="$CONSUMER/sim-personas/shared"
if $DRY_RUN; then
  drylog "mkdir -p $PERSONAS_DEST"
  drylog "cp $PERSONAS_SRC/*.json → $PERSONAS_DEST/"
  drylog "chmod 444 $PERSONAS_DEST/*.json"
else
  mkdir -p "$PERSONAS_DEST"
  cp "$PERSONAS_SRC"/*.json "$PERSONAS_DEST/"
  chmod 444 "$PERSONAS_DEST"/*.json
  log "deployed personas → $PERSONAS_DEST"
fi

# Step 3: write consumer record
RECORD_DIR="$CONSUMER/.hldpro"
RECORD_FILE="$RECORD_DIR/hldpro-sim.json"
if $DRY_RUN; then
  drylog "mkdir -p $RECORD_DIR"
  drylog "write $RECORD_FILE with install_method=$INSTALL_METHOD pinned_sha=$PINNED_SHA"
  # Write to /tmp for dry-run inspection
  mkdir -p "$CONSUMER/.hldpro"
  cat > "$RECORD_FILE" << JSON
{
  "package": "hldpro-sim",
  "version": "$VERSION",
  "tag": "$TAG",
  "pinned_sha": "$PINNED_SHA",
  "install_method": "$INSTALL_METHOD",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "personas_path": "sim-personas/shared/",
  "governance_source": "hldpro-governance"
}
JSON
  log "dry-run consumer record written to $RECORD_FILE"
else
  mkdir -p "$RECORD_DIR"
  cat > "$RECORD_FILE" << JSON
{
  "package": "hldpro-sim",
  "version": "$VERSION",
  "tag": "$TAG",
  "pinned_sha": "$PINNED_SHA",
  "install_method": "$INSTALL_METHOD",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "personas_path": "sim-personas/shared/",
  "governance_source": "hldpro-governance"
}
JSON
  log "consumer record written to $RECORD_FILE"
fi

log "Done. hldpro-sim $VERSION deployed to $CONSUMER"
