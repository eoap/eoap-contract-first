#!/usr/bin/env bash
set -euo pipefail
contract=${1:-reference/waterbodies.cwl}
output=${2:-reference/expected}
mkdir -p "$output"/{docs,diagrams,ogc,oci,publication,baseline}
python scripts/markdown_compat.py cwl2markdown --output "$output/docs" "$contract#waterbodies"
transpiler-mate cwl2puml --output "$output/diagrams" --diagrams component --no-convert-image "$contract#waterbodies"
transpiler-mate cwl2inputs --output "$output/inputs.yaml" "$contract#waterbodies"
transpiler-mate cwl2ogc --output "$output/ogc/processes.json" "$contract#waterbodies"
transpiler-mate cwl2oci --output "$output/oci/annotations.json" "$contract#waterbodies"
transpiler-mate cwl2codemeta --code-repository https://github.com/eoap/waterbodies-learning.git --output "$output/publication/codemeta.json" "$contract#waterbodies"
