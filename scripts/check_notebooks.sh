#!/usr/bin/env bash
# Execute local practice labs with kernels belonging to this course environment.
set -euo pipefail
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$root"
prefix="$root/.notebook-runs/jupyter"
bash scripts/install_notebook_kernels.sh --prefix "$prefix"
export JUPYTER_PATH="$prefix/share/jupyter${JUPYTER_PATH:+:$JUPYTER_PATH}"
export LAB_RUN_CONTAINERS=0
export LAB_RUN_REGISTRY=0
export LAB_RUN_KUBERNETES=0
export LAB_RUN_DEPLOYMENT=0
mkdir -p .notebook-runs/executed
for notebook in practice-labs/[0-9][0-9]-*.ipynb; do
    jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=180 \
        --output-dir .notebook-runs/executed "$notebook"
done
