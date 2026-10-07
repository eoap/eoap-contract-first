#!/usr/bin/env bash
# Inspect actual images through a disposable localhost registry, without public pushes.
set -euo pipefail
output=${1:-build/sbom-local}
if [[ -e "$output" ]]; then
  echo 'Choose a new output directory; cwl2sbom refuses existing directories.' >&2
  exit 1
fi
registry_name="waterbodies-inventory-$$"
docker run -d --name "$registry_name" -p 127.0.0.1::5000 registry:2
trap 'docker rm -f "$registry_name" >/dev/null' EXIT
registry_address=$(docker port "$registry_name" 5000/tcp)
for component in crop norm-diff otsu stac; do
  docker tag "ghcr.io/eoap/waterbodies-$component:1.0.0" "$registry_address/waterbodies-$component:1.0.0"
  docker push "$registry_address/waterbodies-$component:1.0.0"
done
mkdir -p build
export WATERBODIES_LOCAL_REGISTRY="$registry_address"
python - <<'PY'
import os
from pathlib import Path
contract = Path('reference/waterbodies.cwl').read_text()
Path('build/local-registry.cwl').write_text(contract.replace('ghcr.io/eoap/', os.environ['WATERBODIES_LOCAL_REGISTRY'] + '/'))
PY
TRIVY_INSECURE=true transpiler-mate cwl2sbom --platform linux/amd64 \
  --output "$output" build/local-registry.cwl#waterbodies
python scripts/supply_chain.py check --contract build/local-registry.cwl --bundle "$output"
