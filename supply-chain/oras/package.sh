#!/usr/bin/env bash
# Package a reviewed release locally; no authentication or publication.
set -euo pipefail
version=${1:-1.0.0}
contract=${2:-reference/waterbodies.cwl}
annotations=${3:-reference/expected/oci/annotations.json}
layout=${4:-build/oci}
mkdir -p build/package
cp "$contract" build/package/waterbodies.cwl
cp "$annotations" build/package/annotations.json
# ORAS's implicit creation timestamp would otherwise change the artifact digest.
export WATERBODIES_PACKAGE_VERSION="$version"
python - <<'PY'
import json
import os
import yaml
from pathlib import Path
path = Path('build/package/annotations.json')
value = json.loads(path.read_text())
contract = yaml.safe_load(Path('build/package/waterbodies.cwl').read_text())
version = os.environ['WATERBODIES_PACKAGE_VERSION']
if (value['$manifest']['org.opencontainers.image.version'] != version
        or contract['s:softwareVersion'] != version):
    raise ValueError('Package tag, CWL version and generated annotation version must match')
value['$manifest']['org.opencontainers.image.created'] = '2026-10-07T00:00:00Z'
path.write_text(json.dumps(value, sort_keys=True))
PY
layout=$(realpath -m "$layout")
cd build/package
oras push --oci-layout "$layout:$version" --artifact-type application/cwl \
  --annotation-file annotations.json waterbodies.cwl:application/cwl
oras manifest fetch --oci-layout "$layout:$version"
