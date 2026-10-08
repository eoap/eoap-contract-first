# Prerequisites

This course combines Python development, CWL workflows, container packaging and release tooling. You do not need to install everything before starting. Begin with the core environment, then add the external tools when you reach the relevant exercises.

A **CLI** is a command-line interface: a program invoked from a terminal. **PATH** is the list of directories your shell searches for those programs. A **virtual environment** keeps a project's Python interpreter and packages separate from other projects. The commands below use `uv run` to select this project's environment without requiring you to activate it manually.

## Choose the environment you need

| Activity | Prerequisites |
| --- | --- |
| Read the lessons | A web browser. |
| Generate the CLI and metadata, run the scientific workflow locally, and run Python checks | Git, Python 3.12–3.14, uv, Task v3, Bash and the packages installed by `task setup`. |
| Build or run the four component images | The core environment plus a working Docker engine. |
| Package and inspect a local OCI artifact | The core environment plus the ORAS CLI. No registry publication account is needed for a local layout. |
| Generate fresh image inventories and enforce vulnerability policy | Trivy, accessible registry images, network/database access as needed, and Docker for the local registry exercise. |
| Publish releases | Registry credentials and permissions, reviewed release evidence and the configured release workflow. |
| Deploy and execute remotely | A configured ZOO API and execution backend, accessible staged data, available images and any required authentication. |
| Build the instructor slides | Node.js, npm and the locally installed Marp CLI; a supported browser for PDF export. |

Use a terminal with Bash and Unix-style utilities. Linux is the reference environment used by CI. On Windows, a Linux environment through [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) is a practical way to follow these commands; install and run the course tools inside that environment. The scripts are not written as PowerShell commands.

On macOS, use Bash for the supplied scripts and check utility compatibility: the packaging script uses `realpath -m`, which may require GNU Coreutils. Container and SBOM examples target `linux/amd64`; on a different processor architecture, check your container engine's platform support rather than assuming a native build matches that target.

## Install the core tools

Choose the installation instructions for your operating system from the official links. The tables distinguish tools installed on your machine from packages installed automatically into the project.

| Tool | Purpose and course requirement | Official overview, documentation and installation |
| --- | --- | --- |
| **Python** | Runs the application and Python tools. The project accepts 3.12–3.14; start with 3.12 to match CI. | [Home](https://www.python.org/) · [Documentation](https://docs.python.org/3/) · [Downloads](https://www.python.org/downloads/) · [Install through uv](https://docs.astral.sh/uv/guides/install-python/) |
| **Git** | Retrieves this repository and the Git-based Python dependencies. | [Home](https://git-scm.com/) · [Documentation](https://git-scm.com/doc) · [Installation](https://git-scm.com/install/) |
| **uv** | Installs the locked Python environment and runs its commands. | [Documentation](https://docs.astral.sh/uv/) · [README](https://github.com/astral-sh/uv) · [Installation](https://docs.astral.sh/uv/getting-started/installation/) |
| **Task v3** | Runs named recipes from `Taskfile.yaml`, such as `task workflow:run`. This is Go Task, not Taskwarrior or a Python package named task. | [Home](https://taskfile.dev/) · [README](https://github.com/go-task/task) · [Installation](https://taskfile.dev/docs/installation) |
| **Bash** | Executes the repository's shell scripts. Usually available in a Linux environment; install with the operating system's package manager if absent. | [Home and downloads](https://www.gnu.org/software/bash/) · [Manual](https://www.gnu.org/software/bash/manual/) |
| **GNU Coreutils** | Supplies utilities used by shell scripts, including the GNU-compatible `realpath -m` needed for local packaging. | [Home and downloads](https://www.gnu.org/software/coreutils/) · [Manual](https://www.gnu.org/software/coreutils/manual/) |

Check the commands after installation, opening a new terminal if the installer changed PATH:

```console
git --version
uv --version
task --version
bash --version
```

uv can install the chosen Python version without replacing the operating system's Python:

```console
uv python install 3.12
```

See [uv's Python installation guide](https://docs.astral.sh/uv/guides/install-python/) for platform details. You do not need a global command named `python` for every exercise; use `uv run python` once the project environment exists.

## Get the repository and install its Python environment

Clone the course repository and enter its root directory:

```console
git clone https://github.com/eoap/eoap-contract-first.git
cd eoap-contract-first
```

The **repository root** is the directory containing `Taskfile.yaml`, `pyproject.toml` and `uv.lock`. Unless a lesson says otherwise, run its commands from there. Use a Git checkout that preserves symbolic links: `docs/modules` points to the lessons under `modules`.

Set the interpreter for this shell session and install the project:

```bash
export UV_PYTHON=3.12
task setup
```

`task setup` executes:

```console
uv sync --locked --extra tooling --extra dev
```

`uv.lock` records resolved dependencies, including the selected Git revisions. `--locked` checks that this record agrees with the project configuration. The `tooling` and `dev` extras select the generation, testing and documentation packages. The reference application is installed from the local `reference/` directory.

Initial setup needs access to Python package downloads and GitHub. It may also download Python if needed. A network error during installation is different from a workflow failure. Once the environment is prepared, the basic scientific exercise uses local synthetic rasters and bundled STAC validation schemas rather than a remote satellite scene.

For this checkout, use the locked environment rather than independently upgrading individual tools. The upstream installation links below explain the tools, but are not a request to replace the course's dependency selection.

## Know the Python tools installed by setup

These tools are supplied by `task setup`; separate global installations are unnecessary for the normal Task-based exercises.

| Tool | Role | Official documentation, README and installation reference |
| --- | --- | --- |
| **cwltool** | Validates CWL and runs the workflow. | [Documentation](https://cwltool.readthedocs.io/) · [README and installation](https://github.com/common-workflow-language/cwltool#install) |
| **Ruff** | Checks Python formatting and lint rules. | [Documentation](https://docs.astral.sh/ruff/) · [README](https://github.com/astral-sh/ruff) · [Installation](https://docs.astral.sh/ruff/installation/) |
| **mypy** | Checks Python type annotations and their use. | [Home](https://mypy-lang.org/) · [README](https://github.com/python/mypy) · [Getting started/install](https://mypy.readthedocs.io/en/stable/getting_started.html) |
| **Bandit** | Checks Python source for selected security issues. It is separate from container vulnerability scanning. | [Documentation](https://bandit.readthedocs.io/) · [README](https://github.com/PyCQA/bandit) · [Installation](https://bandit.readthedocs.io/en/latest/start.html) |
| **pytest** | Runs behavioral and regression tests. | [Documentation](https://docs.pytest.org/) · [README](https://github.com/pytest-dev/pytest) · [Installation](https://docs.pytest.org/en/stable/getting-started.html) |
| **pytest-cov** | Adds coverage reporting to pytest. | [Documentation and installation](https://pytest-cov.readthedocs.io/) · [README](https://github.com/pytest-dev/pytest-cov) |
| **MkDocs** | Builds and serves the documentation site. | [Home](https://www.mkdocs.org/) · [README](https://github.com/mkdocs/mkdocs) · [Installation](https://www.mkdocs.org/user-guide/installation/) |
| **Material for MkDocs** | Provides the documentation theme. | [Home](https://squidfunk.github.io/mkdocs-material/) · [README](https://github.com/squidfunk/mkdocs-material) · [Installation](https://squidfunk.github.io/mkdocs-material/getting-started/) |

### Transpiler-Mate runtime and plugins

The **runtime** provides the `transpiler-mate` CLI. Each installed plugin contributes a subcommand. The runtime and plugins must share an environment so discovery works. In this course, setup installs them together; they can also be used in a separate tooling environment without becoming dependencies of the scientific application.

Start with the [Transpiler-Mate project overview](https://github.com/transpiler-mate/) and the [runtime README and setup instructions](https://github.com/transpiler-mate/transpiler-mate-runtime). The following links identify every plugin used by this repository; PyPI pages provide published-package installation references, while `task setup` selects the repository's locked versions.

| Package | Command and purpose | Project/README | Installation reference |
| --- | --- | --- | --- |
| `transpiler-mate-runtime` | `transpiler-mate`: loads CWL and runs plugins. | [Runtime](https://github.com/transpiler-mate/transpiler-mate-runtime) | [PyPI](https://pypi.org/project/transpiler-mate-runtime/) |
| `cwl2click` | `transpiler-mate cwl2click`: generates the application CLI. | [README](https://github.com/transpiler-mate/cwl2click) | [PyPI](https://pypi.org/project/cwl2click/) |
| `cwl2markdown` | `transpiler-mate cwl2markdown`: generates Markdown documentation; the course task applies its compatibility adapter. | [README](https://github.com/transpiler-mate/cwl2markdown) | [PyPI](https://pypi.org/project/cwl2markdown/) |
| `cwl2puml` | `transpiler-mate cwl2puml`: generates PlantUML diagram source. | [README](https://github.com/transpiler-mate/cwl2puml) | [PyPI](https://pypi.org/project/cwl2puml/) |
| `cwl2inputs` | `transpiler-mate cwl2inputs`: generates input YAML templates. | [README](https://github.com/transpiler-mate/cwl2inputs) | [PyPI](https://pypi.org/project/cwl2inputs/) |
| `cwl2ogc` | `transpiler-mate cwl2ogc`: generates OGC process descriptions. | [README](https://github.com/transpiler-mate/cwl2ogc) | [PyPI](https://pypi.org/project/cwl2ogc/) |
| `cwl2oci` | `transpiler-mate cwl2oci`: generates OCI annotations. | [README](https://github.com/transpiler-mate/cwl2oci) | [PyPI](https://pypi.org/project/cwl2oci/) |
| `cwl2sbom` | `transpiler-mate cwl2sbom`: inventories declared containers using external Trivy. | [README](https://github.com/transpiler-mate/cwl2sbom) | [PyPI](https://pypi.org/project/cwl2sbom/) |
| `cwl-baseline-plugin` | `transpiler-mate baseline`: compares contracts and version compatibility. | [README](https://github.com/transpiler-mate/cwl-baseline-plugin) | [PyPI](https://pypi.org/project/cwl-baseline-plugin/) |
| `cwl2codemeta` | `transpiler-mate cwl2codemeta`: exports software metadata. | [README](https://github.com/transpiler-mate/cwl2codemeta) | [PyPI](https://pypi.org/project/cwl2codemeta/) |

Supporting API and loading modules are installed as dependencies; attendees do not need separate commands for them. Check discovery with:

```console
uv run transpiler-mate --help
uv run transpiler-mate cwl2click --help
```

### Scientific and data libraries

Setup also installs these application libraries. They are Python imports rather than tools you need to launch separately. The full resolved dependency list is in `uv.lock`.

| Library | Purpose | Official documentation / README / installation reference |
| --- | --- | --- |
| **Click** | Implements the generated command-line interface. | [Documentation](https://click.palletsprojects.com/) · [README](https://github.com/pallets/click) · [PyPI](https://pypi.org/project/click/) |
| **NumPy** | Performs numerical operations on pixel arrays. | [Home and install guide](https://numpy.org/install/) · [README](https://github.com/numpy/numpy) |
| **Rasterio** | Reads and writes georeferenced rasters. | [Documentation](https://rasterio.readthedocs.io/) · [README](https://github.com/rasterio/rasterio) · [Installation](https://rasterio.readthedocs.io/en/stable/installation.html) |
| **scikit-image** | Supplies Otsu thresholding. | [Home and installation](https://scikit-image.org/docs/stable/user_guide/install.html) · [README](https://github.com/scikit-image/scikit-image) |
| **pyproj** | Transforms coordinates between reference systems. | [Documentation and installation](https://pyproj4.github.io/pyproj/stable/installation.html) · [README](https://github.com/pyproj4/pyproj) |
| **Shapely** | Handles geometric shapes used for AOIs. | [Documentation](https://shapely.readthedocs.io/) · [README/install](https://github.com/shapely/shapely) |
| **PySTAC, Terradue fork** | Creates, reads and validates STAC objects and extensions. | [Fork README/install](https://github.com/Terradue/pystac/tree/t2_extensions) · [PySTAC documentation](https://pystac.readthedocs.io/) |
| **PyYAML** | Reads and writes YAML in repository tooling. | [Documentation/install](https://pyyaml.org/wiki/PyYAMLDocumentation) · [README](https://github.com/yaml/pyyaml) |

The required PySTAC dependency is `pystac[validation] @ git+https://github.com/Terradue/pystac.git@t2_extensions`. Let setup install it; substituting the upstream PyPI package would change the dependency required by this project.

If a raster library cannot install on your platform, read its installation diagnostics and official platform requirements. A source build may need native libraries and build tools. Do not assume the Python version range guarantees prebuilt packages for every operating system and processor combination.

### Hatch and build tooling

**Hatch** manages builds and the alternative development/test environments configured in `pyproject.toml`. **Hatchling** is the Python build backend used to create the packages. The normal `task setup` and `uv run` path does not require a globally installed Hatch CLI; the Docker builder installs its own Hatch.

For contributors running `hatch run dev:check` or building directly with Hatch, install it separately: [Hatch home](https://hatch.pypa.io/) · [README](https://github.com/pypa/hatch) · [installation](https://hatch.pypa.io/latest/install/) · [Hatchling package](https://pypi.org/project/hatchling/). Its environments are separate from uv's environment and may require their own initial downloads.

Both Python projects read their application version from `reference/src/waterbodies/__about__.py`; do not confuse that application version with the versions of the build tools.

## Verify the core setup before proceeding

Run these commands from the repository root:

```console
uv run python --version
uv run waterbodies --help
uv run cwltool --version
uv run transpiler-mate --help
task fixtures:generate
task reference:test
task workflow:run
```

Expect Python in the supported range, CLI help listing `crop`, `norm-diff`, `otsu` and `stac`, and a successful workflow producing `build/result/catalog`. The synthetic example should yield a 6×6 mask with 18 water pixels; [Run the application](modules/09-run-the-application/lesson.md) explains how to inspect it.

`task reference:test` checks the contracts, Python quality gates, tests, supply-chain conventions and documentation build. The ORAS round-trip test is skipped if the external ORAS CLI is absent. Passing the core checks therefore does not establish that OCI packaging or remote deployment has been exercised.

To preview the documentation, run `task docs:serve`, open the local address printed by MkDocs and stop the server with Ctrl+C. `task docs:build` builds the site without starting a server.

## Add container, inventory and publication tools

These executables are not installed by `task setup`.

| Tool | When and why you need it | Official overview, README and installation |
| --- | --- | --- |
| **Docker Engine / Docker Desktop** | Builds component images and runs the container workflow or temporary registry. You need a running engine, not just the `docker` client. | [Home](https://www.docker.com/) · [CLI README](https://github.com/docker/cli) · [Engine installation](https://docs.docker.com/engine/install/) · [Desktop setup](https://docs.docker.com/desktop/) |
| **ORAS CLI 1.3.1** | Packages, inspects, transfers and attaches evidence to OCI artifacts. This is the course release-workflow version. | [Home](https://oras.land/) · [README](https://github.com/oras-project/oras) · [Installation](https://oras.land/docs/installation/) · [1.3.1 release](https://github.com/oras-project/oras/releases/tag/v1.3.1) |
| **Trivy 0.75.0** | Inventories images and scans image SBOMs against vulnerability information. This is the course release-workflow version. | [Home](https://trivy.dev/) · [README](https://github.com/aquasecurity/trivy) · [Installation](https://trivy.dev/docs/latest/getting-started/installation/) · [0.75.0 release](https://github.com/aquasecurity/trivy/releases/tag/v0.75.0) |
| **curl** | Sends the HTTP requests in deployment examples. Use a version supporting `--fail-with-body`. | [Home](https://curl.se/) · [README](https://github.com/curl/curl) · [Downloads](https://curl.se/download.html) |
| **Sigstore Cosign** | Optional signing exercise only; not required by the implemented release pipeline. | [Home](https://www.sigstore.dev/) · [README](https://github.com/sigstore/cosign) · [Installation](https://docs.sigstore.dev/cosign/system_config/installation/) |

Install ORAS from its official binary distribution or documented package-manager method. The Python package named `oras` is not a substitute for the ORAS executable used by this repository.

Verify the tools you intend to use:

```console
docker version
docker info
oras version
trivy --version
curl --version
```

`docker version` should report both client and server information. A connection error usually means the engine is stopped, inaccessible or configured differently from your terminal. Follow Docker's platform-specific setup rather than assuming installing the client started the engine.

Before inventory generation, ensure the images exist in a registry Trivy can access. The inspected plugin requests remote image inspection, so local Docker images alone are insufficient. Vulnerability assessment also needs Trivy's databases available and appropriately updated. Choose a new SBOM output directory for each generation run.

Registry publication requires an account or service identity with write permission; inspection and image retrieval may require read credentials. The core local workflow needs neither a GitHub login nor registry publication privileges. For actual releases, configure the GitHub `release` environment and reviewers as described in [Supply-chain assurance](supply-chain.md).

## Prepare a remote processing service only when needed

**ZOO-Project** provides the service used in the deployment exercise. Installing a command-line client does not create that service: the API, execution backend, storage and authentication must be prepared by you or the course provider.

- ZOO: [project home](https://zoo-project.org/) · [source/README](https://github.com/ZOO-Project/ZOO-Project) · [installation documentation](https://zoo-project.github.io/docs/install/index.html).
- Course-specific environment: [EOAP ZOO course and setup README](https://github.com/eoap/ogc-api-processes-with-zoo) · [tutorial site](https://eoap.github.io/ogc-api-processes-with-zoo/).
- Registry publication: [GitHub Container Registry documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

Before attempting deployment, obtain the actual API base URL, authentication method, accepted input-staging convention and backend storage location. The backend must be able to retrieve the selected component images and read the complete staged STAC directory.

A directory on your laptop is not automatically available to the server. A URL for one Item JSON is not equivalent to the workflow's self-contained Directory input. Transfer the catalog, linked Item and raster assets using the backend's supported mechanism, then follow [Deployment](deployment.md). The repository's placeholder execution request is not runnable until those details are supplied.

A particular backend may require additional infrastructure. Follow that environment's setup guide; Kubernetes or a separate workflow engine is not a universal prerequisite for the local course exercises.

## Optional diagram rendering and instructor slides

The artifact-generation task produces PlantUML source with image conversion disabled. It does not require a separate Java-based renderer merely to generate `.puml` files. To render them yourself, follow [PlantUML's quick start](https://plantuml.com/starting), [project README](https://github.com/plantuml/plantuml) and [downloads](https://plantuml.com/download). That guide explains the Java and any diagram-specific rendering dependencies. Mermaid diagrams in these lessons are handled by the documentation presentation; no Mermaid CLI is required for `task docs:build`.

Slide authoring is a separate optional toolchain:

| Tool | Purpose and installation path | Official links |
| --- | --- | --- |
| **Node.js** | Runs the slide-generation tooling. Use a supported LTS release compatible with the locked dependencies. | [Home](https://nodejs.org/) · [README](https://github.com/nodejs/node) · [Downloads/install](https://nodejs.org/en/download) |
| **npm** | Installs the versions in `slides/package-lock.json`. | [Documentation](https://docs.npmjs.com/) · [README](https://github.com/npm/cli) · [Node.js/npm installation](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm/) |
| **Marp CLI 4.5.1** | Converts the instructor Markdown deck; installed locally by `task slides:setup`. | [Home](https://marp.app/) · [README/install](https://github.com/marp-team/marp-cli#installation) |
| **A browser supported by Marp** | Required for PDF export: Chrome, Edge or Firefox. Install one supported choice, not all three. | [Marp browser guidance](https://github.com/marp-team/marp-cli) · [Chrome download](https://www.google.com/chrome/) · [Edge download](https://www.microsoft.com/edge/download) · [Firefox download](https://www.mozilla.org/firefox/new/) |

Check `node --version` and `npm --version`, then use:

```console
task slides:setup
task slides:html
task slides:pdf
```

The setup task runs `npm ci` against the lockfile rather than installing a global Marp version. See the [instructor README](https://github.com/eoap/eoap-contract-first/blob/main/slides/README.md) for preview commands, browser configuration and the documented dependency-audit limitations. Slides are not required to complete the scientific exercises.

## Diagnose setup problems at the right layer

| Symptom | First thing to check |
| --- | --- |
| `command not found` for Git, uv, Task or an external CLI | Installation and PATH in the same terminal where you run the exercise. |
| `waterbodies` or a Python tool is missing | Run `task setup` from the repository root, then invoke it with `uv run`. |
| A Transpiler-Mate plugin is missing | Confirm the tooling extra was installed and the runtime is using that same environment. |
| Python version rejected | Check `uv run python --version` and select a supported interpreter. |
| Dependency download fails | Network, GitHub/package-index access and any organization-specific proxy configuration. |
| Docker cannot connect | Engine status, access permissions and the active Docker context. |
| Image inspection fails although the image was built | Registry availability, credentials, image reference and selected platform. |
| SBOM generation refuses its output path | Choose a fresh output directory; the plugin does not overwrite an existing bundle. |
| Remote execution cannot read inputs | Backend staging and storage access, not the presence of local files on your workstation. |

Once the core checks pass, continue with the [learning path](learning-path.md). Add the optional tools when the selected exercise requires them, and verify each layer before moving on to the next.
