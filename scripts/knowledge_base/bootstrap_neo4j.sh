#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${NEO4J_CONTAINER_NAME:-hldpro-governance-neo4j}"
IMAGE="${NEO4J_IMAGE:-neo4j:5-community}"
HTTP_PORT="${NEO4J_HTTP_PORT:-7474}"
BOLT_PORT="${NEO4J_BOLT_PORT:-7687}"
PASSWORD="${NEO4J_PASSWORD:-governance-dev-password}"
VOLUME_NAME="${NEO4J_VOLUME_NAME:-${CONTAINER_NAME}-data}"
WAIT_SECONDS="${NEO4J_WAIT_SECONDS:-90}"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is required for Neo4j bootstrap."
  exit 1
fi

ensure_container_running() {
  local state
  state="$(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME" 2>/dev/null || true)"

  if [[ "$state" == "running" ]]; then
    return 0
  fi

  if [[ -n "$state" ]]; then
    docker start "$CONTAINER_NAME" >/dev/null
    return 0
  fi

  docker volume create "$VOLUME_NAME" >/dev/null
  docker run -d \
    --name "$CONTAINER_NAME" \
    -p "${HTTP_PORT}:7474" \
    -p "${BOLT_PORT}:7687" \
    -e "NEO4J_AUTH=neo4j/${PASSWORD}" \
    -e "NEO4J_server_memory_heap_initial__size=512m" \
    -e "NEO4J_server_memory_heap_max__size=512m" \
    -v "${VOLUME_NAME}:/data" \
    "$IMAGE" >/dev/null
}

wait_for_neo4j() {
  local start now
  start="$(date +%s)"
  while true; do
    if docker exec "$CONTAINER_NAME" cypher-shell -u neo4j -p "$PASSWORD" "RETURN 1 AS ok;" >/tmp/neo4j-bootstrap.out 2>/tmp/neo4j-bootstrap.err; then
      return 0
    fi
    now="$(date +%s)"
    if (( now - start >= WAIT_SECONDS )); then
      echo "ERROR: Neo4j did not become ready within ${WAIT_SECONDS}s."
      echo "--- stderr ---"
      cat /tmp/neo4j-bootstrap.err || true
      exit 1
    fi
    sleep 2
  done
}

ensure_container_running
wait_for_neo4j

echo "Neo4j runtime is ready."
echo "Container: ${CONTAINER_NAME}"
echo "HTTP: http://localhost:${HTTP_PORT}"
echo "Bolt: bolt://localhost:${BOLT_PORT}"
echo "Auth: neo4j / ${PASSWORD}"
