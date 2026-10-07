#!/usr/bin/env bash
# Instructor-driven ZOO demo; storage and release identity must be configured first.
set -euo pipefail
mode=${1:-inspect}
: "${API:?Set API to the configured ZOO API base URL}"
process_id=${PROCESS_ID:-waterbodies}
mkdir -p build/slides/deployment
case "$mode" in
  deploy)
    : "${EOAP_REF:?Set EOAP_REF to the reviewed promoted artifact digest}"
    if [[ ! "$EOAP_REF" =~ @sha256:[[:xdigit:]]{64}$ ]]; then
      echo 'EOAP_REF must contain a complete promoted sha256 digest.' >&2
      exit 1
    fi
    oras discover "$EOAP_REF"
    package_directory=$(mktemp -d build/slides/deployment/package.XXXXXX)
    oras pull "$EOAP_REF" -o "$package_directory"
    curl --fail-with-body -X POST "$API/processes?w=$process_id" \
      -H 'Accept: application/json' -H 'Content-Type: application/cwl+yaml' \
      --data-binary "@$package_directory/waterbodies.cwl"
    ;;
  inspect)
    curl --fail-with-body "$API/processes"
    curl --fail-with-body "$API/processes/$process_id"
    curl --fail-with-body "$API/processes/$process_id/package"
    ;;
  execute)
    test -f build/execute.json
    curl --fail-with-body -D build/slides/deployment/job.headers \
      -o build/slides/deployment/job.json \
      -X POST "$API/processes/$process_id/execution" \
      -H 'Content-Type: application/json' -H 'Prefer: respond-async' \
      --data-binary @build/execute.json
    ;;
  monitor)
    : "${JOB_ID:?Set JOB_ID to the returned job identifier}"
    curl --fail-with-body "$API/jobs/$JOB_ID"
    curl --fail-with-body "$API/jobs/$JOB_ID/results"
    ;;
  *)
    echo 'Mode must be inspect, deploy, execute or monitor.' >&2
    exit 1
    ;;
esac
