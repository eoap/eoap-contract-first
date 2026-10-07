# Water Bodies learning

**Build an Earth Observation Application Package from its CWL contract.**

Water Bodies is the EOAP reference application for learning contract-first processing design, implementation, workflow composition, software supply-chain assurance, packaging, distribution and deployment.

```text
waterbodies.cwl → generated CLI → implementations
      │                │              │
      ├── workflow ────┴── versioned containers
      └── metadata ────────────┐
                     tests + assurance
                             │
                     SBOM + immutable identity
                             │
                     EOAP OCI artifact → registry
                             │
                     OGC API - Processes → execution
```

Use **top-down contract design with bottom-up implementation and verification**.
The scientific chain remains crop(green/nir) → normalized difference → Otsu → STAC.

Install Python 3.12–3.14, Git, uv and Task. Then:

```console
git clone https://github.com/eoap/waterbodies-learning.git
cd waterbodies-learning
task setup
task reference:test
task workflow:run
```

The working directory may have another checkout name; run all tasks from its root.
Start at [Module 00](modules/00-waterbodies/README.md), then follow the [learning path](docs/learning-path.md).

`modules/` is the progressive course; `reference/` is the canonical implementation;
`supply-chain/` contains explicit release and promotion mechanics. The application wheel is built from `reference/pyproject.toml` and owns `reference/src/waterbodies`. The root project supplies the course contract, tooling and quality configuration, and resolves the application checkout through uv.

Core local checks and workflow execution need no Docker or registry credentials.
ORAS 1.3.1 and Trivy 0.75.0 are external tools for the capstone; Docker is needed
for image builds. The example GHCR names are intended release destinations, not
claims that these images have already been published. Live deployment requires
a configured ZOO server and server-accessible staged input data.

See [architecture and verified upstream deviations](docs/architecture.md),
[supply-chain assurance](docs/supply-chain.md), [deployment](docs/deployment.md)
and [contributing](docs/contributing.md).

The [teacher-facing Marp deck](slides/README.md) provides presenter notes, live demos and reproducible HTML/PDF exports for the complete course.
