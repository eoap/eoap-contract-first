#!/usr/bin/env bash
# Transparent capstone policy: reject unfixed or fixed HIGH/CRITICAL vulnerabilities.
set -euo pipefail
bundle=${1:-build/sbom}
for evidence in "$bundle"/images/*.cdx.json; do
  trivy sbom --severity HIGH,CRITICAL --exit-code 1 "$evidence"
done
