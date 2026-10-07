# Prerequisites

Use Python 3.12–3.14, Git, uv and Task v3, matching the company packaging conventions. Python 3.12 is used in CI; the Rocky Linux container uses its supported python3 package. Both projects read their release version from reference/src/waterbodies/__about__.py.

`task setup` runs `uv sync --locked --extra tooling --extra dev`; uv.lock pins all resolved packages and the Terradue PySTAC t2_extensions revision. Initial setup needs internet access. Basic tests use staged synthetic rasters and bundled official STAC schemas, so workflow execution needs no remote EO scene.

```console
task setup
uv run waterbodies --help
task reference:test
```

Optional capstone tools: Docker, ORAS CLI 1.3.1 and Trivy 0.75.0. The Python package named oras is not the ORAS CLI. Install official command binaries and confirm `oras version` and `trivy --version`. SBOM generation requires access to all declared images and the Trivy database; output must be a new directory.

A ZOO deployment also needs its execution backend, staged catalog storage accessible to that backend, and authentication supplied according to the server's configuration. The local Directory fixture does not imply remote upload support.
