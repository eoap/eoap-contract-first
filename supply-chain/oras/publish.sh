#!/usr/bin/env bash
# Called only after verified inventory and vulnerability gates in protected release CI.
set -euo pipefail
version=${1:?Provide release version}
reference="ghcr.io/eoap/waterbodies:$version-candidate"
oras cp --from-oci-layout "build/oci:$version" "$reference"
digest=$(oras resolve "$reference")
oras attach --artifact-type application/vnd.cyclonedx+json "ghcr.io/eoap/waterbodies@$digest" \
  build/sbom/workflow.cdx.json:application/vnd.cyclonedx+json
python - <<'PY' > build/image-evidence.tsv
import json
from pathlib import Path
lock = json.loads(Path('build/sbom/images.lock.json').read_text())
for image in lock['images']:
    print(image['repository_digests'][0] + '\tbuild/sbom/' + image['sbom'])
PY
while IFS=$'\t' read -r image evidence; do
  oras attach --artifact-type application/vnd.cyclonedx+json "$image" \
    "$evidence:application/vnd.cyclonedx+json"
done < build/image-evidence.tsv
oras attach --artifact-type application/json "ghcr.io/eoap/waterbodies@$digest" \
  build/sbom/images.lock.json:application/json build/sbom/coverage.json:application/json \
  build/baseline.json:application/json
oras discover "ghcr.io/eoap/waterbodies@$digest"
# Promotion names the already gated and evidence-associated immutable subject.
oras tag "ghcr.io/eoap/waterbodies@$digest" "$version"
test "$(oras resolve "ghcr.io/eoap/waterbodies:$version")" = "$digest"
