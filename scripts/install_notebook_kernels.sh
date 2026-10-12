#!/usr/bin/env bash
# Register notebook kernels with the interpreter from the locked course environment.
set -euo pipefail
python -m bash_kernel.install "$@"
python -m ipykernel install "$@" --name contract_env --display-name 'Python (eoap-contract-first)'
