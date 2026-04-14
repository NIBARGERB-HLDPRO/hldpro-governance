#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "::error::[require-lam-dual-signature] expected exactly one argument: <manifest.json>"
  exit 1
fi

MANIFEST_PATH="$1"
if [ ! -f "${MANIFEST_PATH}" ]; then
  echo "::error file=${MANIFEST_PATH}::[require-lam-dual-signature] manifest file not found"
  exit 1
fi

get_field() {
  local path="$1"
  jq -r "${path} // empty" "${MANIFEST_PATH}" 2>/dev/null
}

WORKER_MODEL_ID="$(get_field '.worker.model_id')"
WORKER_MODEL_FAMILY="$(get_field '.worker.model_family')"
REVIEWER_MODEL_ID="$(get_field '.reviewer.model_id')"
REVIEWER_MODEL_FAMILY="$(get_field '.reviewer.model_family')"
AGREEMENT_BIT="$(get_field '.agreement_bit')"
INPUT_HASH="$(get_field '.input_hash')"
OUTPUT_HASH="$(get_field '.output_hash')"

if [ -z "${WORKER_MODEL_ID}" ] || [ -z "${WORKER_MODEL_FAMILY}" ] || [ -z "${REVIEWER_MODEL_ID}" ] || [ -z "${REVIEWER_MODEL_FAMILY}" ] || [ -z "${AGREEMENT_BIT}" ] || [ -z "${INPUT_HASH}" ] || [ -z "${OUTPUT_HASH}" ]; then
  echo "::error file=${MANIFEST_PATH}::[require-lam-dual-signature] missing one or more required fields: worker.model_id, worker.model_family, reviewer.model_id, reviewer.model_family, agreement_bit, input_hash, output_hash"
  exit 1
fi

if [ "${WORKER_MODEL_FAMILY}" = "${REVIEWER_MODEL_FAMILY}" ]; then
  echo "::error file=${MANIFEST_PATH}::[require-lam-dual-signature] worker.model_family must differ from reviewer.model_family"
  exit 1
fi

if [ "${AGREEMENT_BIT}" != "true" ]; then
  echo "::error file=${MANIFEST_PATH}::[require-lam-dual-signature] agreement_bit must be true"
  exit 1
fi

echo "[require-lam-dual-signature] ${MANIFEST_PATH} passed validation"
