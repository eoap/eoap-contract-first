# Architecture and upstream evidence

Research performed against actual source, tests, examples and documentation on 2026-10-07. Release references below were checked on 2026-10-08: prefer an available PyPI version, otherwise the latest Git tag, rather than a commit hash. These release references are distinct from the historical projection revisions recorded in [upstream-lock.json](upstream-lock.json) and the verification record below.

## Application library and upstream references

The EOAP repositories provide examples and architectural guidance, rather than Python dependencies. PySTAC is an application dependency and must use the Terradue fork with validation support. That fork has no Git tags; retain `pystac[validation] @ git+https://github.com/Terradue/pystac.git@t2_extensions` rather than substituting the upstream PyPI package.

| Repository | Release or source reference | Role |
| --- | --- | --- |
| [advanced-tooling](https://github.com/eoap/advanced-tooling) | Git tag [v0.1.2](https://github.com/eoap/advanced-tooling/tree/v0.1.2) | OCI artifact and supply-chain guidance |
| [application-package-patterns](https://github.com/eoap/application-package-patterns) | Git tag [1.1.0](https://github.com/eoap/application-package-patterns/tree/1.1.0) | Staging and workflow composition examples |
| [mastering-app-package](https://github.com/eoap/mastering-app-package) | Git tag [1.1.1](https://github.com/eoap/mastering-app-package/tree/1.1.1) | Water Bodies source examples |
| [mastering-enhancements](https://github.com/eoap/mastering-app-package/tree/feature/enhancements) | `feature/enhancements` branch; no separate release | Enhancement implementations and crop tests |
| [ogc-api-processes-with-zoo](https://github.com/eoap/ogc-api-processes-with-zoo) | Git tag [0.1.1](https://github.com/eoap/ogc-api-processes-with-zoo/tree/0.1.1) | Deployment and execution guidance |
| [pystac (Terradue fork)](https://github.com/Terradue/pystac) | [t2_extensions](https://github.com/Terradue/pystac/tree/t2_extensions) branch; no tags | STAC objects, extension APIs and validation |

## Standalone CLI tooling

Transpiler-Mate and its plugins can run as CLI tools in a separate tooling environment; they do not need to be included in any `pyproject.toml`. Install the runtime and the required plugins into the same environment so `transpiler-mate` can discover them. Supporting modules are installed as runtime dependencies; attendees interact with the runtime CLI and its plugins. The repository currently declares a `tooling` extra for its own generation and verification workflow; that is a repository convenience, not an application packaging requirement.

| Tooling package | PyPI version | Role |
| --- | --- | --- |
| [transpiler-mate-runtime](https://github.com/transpiler-mate/transpiler-mate-runtime) | [1.3.0](https://pypi.org/project/transpiler-mate-runtime/1.3.0/) | `transpiler-mate` CLI and plugin discovery |
| [transpiler-mate-api](https://github.com/transpiler-mate/transpiler-mate-api) | [1.0.1](https://pypi.org/project/transpiler-mate-api/1.0.1/) | Shared plugin API dependency |
| [cwl-baseline-plugin](https://github.com/transpiler-mate/cwl-baseline-plugin) | [0.1.1](https://pypi.org/project/cwl-baseline-plugin/0.1.1/) | Baseline comparison plugin |
| [cwl2click](https://github.com/transpiler-mate/cwl2click) | [0.10.1](https://pypi.org/project/cwl2click/0.10.1/) | Click CLI generation plugin |
| [cwl2codemeta](https://github.com/transpiler-mate/cwl2codemeta) | [0.1.1](https://pypi.org/project/cwl2codemeta/0.1.1/) | CodeMeta generation plugin |
| [cwl2inputs](https://github.com/transpiler-mate/cwl2inputs) | [0.1.1](https://pypi.org/project/cwl2inputs/0.1.1/) | Input template generation plugin |
| [cwl2markdown](https://github.com/transpiler-mate/cwl2markdown) | [0.2.1](https://pypi.org/project/cwl2markdown/0.2.1/) | Markdown documentation plugin |
| [cwl2oci](https://github.com/transpiler-mate/cwl2oci) | [0.1.1](https://pypi.org/project/cwl2oci/0.1.1/) | OCI annotation generation plugin |
| [cwl2ogc](https://github.com/transpiler-mate/cwl2ogc) | [0.22.2](https://pypi.org/project/cwl2ogc/0.22.2/) | OGC process description plugin |
| [cwl2puml](https://github.com/transpiler-mate/cwl2puml) | [0.49.1](https://pypi.org/project/cwl2puml/0.49.1/) | PlantUML generation plugin |
| [cwl2sbom](https://github.com/transpiler-mate/cwl2sbom) | [0.1.1](https://pypi.org/project/cwl2sbom/0.1.1/) | Software inventory generation plugin |

## Design decisions

The canonical `$graph` contains #waterbodies and four tools. Its generated interface is one waterbodies group. The runtime resolves the workflow and its tool references, while cwl2click generates the command-line interface. The complete cwltool execution verifies workflow references and repeated raster-file options.

The Water Bodies source is `mastering-app-package/water-bodies/command-line-tools/*/app.py`, plus `feature/enhancements` implementations and crop tests under the same component tree. Preserve EO common-band selection, AOI transformation, COG writes, `(green-nir)/(green+nir)`, Otsu strict greater-than, and the original Item identity/time in a self-contained result catalog. Enhancements supply grid checking, AOI polygons, finite-value classification and safe Item paths.

The source input is a staged Directory with catalog.json, Item JSON and local bands. Crop and STAC use PySTAC. Projection and Raster extension accessors replace the older rio-stac serialization path; metadata expresses the same cropped-grid product semantics. Geometry is built as an input value to a PySTAC Item, never as a handwritten STAC Item representation. We bundle official EO v1.1.0, projection v2.0.0 and raster v1.1.0 schemas and use PySTAC validation unchanged. Schema `$id` values identify the original sources. Schema files are upstream artifacts, not generated Python models.

## Tool purposes and upstream guidance

### Standalone CLI tooling

#### Transpiler-Mate runtime

`transpiler-mate-runtime` provides the `transpiler-mate` command. It loads the selected CWL process, resolves references to workflow steps and tools, and prepares the software metadata for the installed plugins. Attendees use this common entry point to generate different artifacts from the same contract. Run `transpiler-mate --help` to discover installed plugins and `transpiler-mate <plugin> --help` for their options.

The purpose-based groups below follow the [Transpiler-Mate project tables](https://github.com/transpiler-mate/), covering the plugins listed in our tooling table. Repository-specific verification notes refer to the source revisions inspected on 2026-10-07; they do not establish verification of every release listed above.

#### Software generation

- **cwl2click** generates a Python Click command-line interface from CWL tool definitions. In Water Bodies, it keeps the command names and input options aligned with the contract while the application supplies the scientific operations. The generated interface is checked against fresh generation and exercised through the workflow runner, including multiple raster-file inputs.
- **cwl2inputs** creates YAML input templates for a selected process. Attendees fill in the actual data locations and parameter values before running the workflow.
- **cwl2oci** produces OCI annotations describing the software and CWL process. These annotations accompany the package when ORAS publishes it; artifact assembly and publication are separate pipeline steps.

#### Documentation generation

- **cwl2markdown** turns the CWL contract and software metadata into readable workflow documentation. The inspected version requires a repository compatibility adapter for documentation generation; this is a historical verification note, not a requirement established for every published version.
- **cwl2puml** creates PlantUML workflow diagrams to help readers understand the processing steps and their connections. This course generates diagram source without relying on an external rendering service.

#### Format conversion

**cwl2ogc** generates an OGC API – Processes description of the workflow's inputs and outputs. This provides the service-facing contract; deployment and execution are handled by the processing service described below.

#### FAIR research software metadata

**cwl2codemeta** exports embedded software metadata as CodeMeta JSON-LD, helping others discover and describe the workflow. CodeMeta 3.0 generation is verified in this repository. The repository's `CITATION.cff` is maintained separately; citation generation, DataCite exports and RO-Crate packaging are outside this course's verified tooling scope.

#### Analysis and reporting

**cwl-baseline-plugin** compares CWL releases and reports compatibility changes with a minimum semantic-version increment. Reviewers use the report alongside their assessment of changes to scientific behavior. In this course, removing the EPSG default is reviewed as a major change, and release CI requires an independent review classification. The inspected version can also report differences caused by automatically assigned array-schema names, so findings need review.

#### Software supply-chain inspection

**cwl2sbom** inventories the containers referenced by the selected workflow, including reachable tools. With Trivy and an explicit target platform, it produces workflow and image inventories, image identities and coverage evidence. Undeclared runtime software remains outside that inventory, and the inspected workflow composition is marked `incomplete`. Vulnerability policy checks, signing and publication belong to subsequent pipeline steps.

### Application library and upstream references

**PySTAC** provides STAC Item creation, asset and link management, extension metadata and validation for the scientific application. The Terradue fork is the application library used here; the projection and raster extensions describe the cropped products, and output Items are validated with their declared schemas.

**mastering-app-package** supplies the Water Bodies processing example, with additional validation and crop behavior drawn from its enhancements branch. These sources establish the scientific behavior preserved by the contract-first implementation described above.

**application-package-patterns** guides explicit data staging and workflow composition. The scientific tools receive a staged directory containing the catalog and local assets; staging remote data is a separate responsibility.

**advanced-tooling** guides CWL packaging as OCI artifacts and the use of separate ORAS attachments. This course uses the CycloneDX media type for the generated software inventories.

**ogc-api-processes-with-zoo** guides process deployment, discovery, execution, job monitoring and result retrieval. The deployment flow pulls the promoted OCI artifact and submits its CWL bytes to `POST /processes?w=...` with `application/cwl+yaml`; the workflow's generated process description supports the service interface.

## Boundaries

The application is an installable Hatch project under reference/, with a dynamic version in src/waterbodies/__about__.py. The root learning project depends on that versioned application, resolves it locally through tool.uv.sources and a Hatch pre-install hook that installs the application editably before the course, and owns the repository quality gates. Its wheel includes the canonical CWL; it does not duplicate the application Python namespace. Packaging follows company/pyproject.toml. The four component containers share the reference package in this first release. Following company/Dockerfile, they build application/dependency wheels on Rocky Linux 10.2 minimal and install them offline into a runtime virtual environment as neo (UID/GID 2000). Git, GCC and Hatch remain in the builder; runtime checks dependencies and CLI help, removes pip and wheel archives, and supplies a help CMD without a conflicting ENTRYPOINT. Their dependency versions are pinned during release preparation by real inspected digests, not fabricated identities.

Scientific limitations: this is the established Water Bodies classifier, not cloud screening or a calibrated global water product. Authenticated cloud URL signing remains a staging concern. Core tests establish grid arithmetic, threshold semantics and portable metadata on compact fixtures; large real-scene evaluation is separate.

Supply-chain checks establish declared-image coverage and integrity, then a transparent HIGH/CRITICAL vulnerability gate. They cannot prove that software is secure or account for all runtime downloads. Protected promotion and optional verified signatures/provenance add distinct assertions.

## Bootstrap verification record

The local install and reference checks passed. The scientific chain executed both with the installed generated CLI and with all four built Docker images. The result Item validated against core STAC, projection and raster extension schemas. Container execution exposed absolute fixture hrefs; fixture generation now calls PySTAC's make_all_asset_hrefs_relative after normalizing the catalog, and this is regression-tested with a relocated source Directory.

The actual cwl2sbom/Trivy remote path was tested through a disposable localhost registry with all four real images and linux/amd64. The committed historical bundle has complete declared-image coverage and verified checksums. It is not promoted-release evidence. ORAS packaging and pull round-trip succeeded.

The educational HIGH/CRITICAL policy rejected the image on 2026-10-07: the first scanned component reported 62 HIGH and 2 CRITICAL findings. This is an observed failure of the promotion gate, not a successful security release. No exceptions, severity reductions or fabricated scan evidence were added. Resolve the dependency/base-image findings and regenerate all evidence before production promotion; later vulnerability databases may report different results. Public GHCR publication and live ZOO deployment were not performed in this workspace.

## Company packaging alignment

Packaging and containers now follow the supplied company templates. Both Hatch projects use dynamic versions and Python 3.12–3.14. The application wheel is independently buildable from reference/; the root course wheel owns the canonical contract and development tooling. uv resolves the application editably, while Hatch uses a pre-install hook and explicit local dependency override because its project installation does not consume tool.uv.sources.

All four Rocky Linux 10.2 multi-stage images built and the complete container workflow succeeded. Runtime inspection confirmed UID 2000 and pip absent. The rebuilt crop image was scanned with Trivy 0.75.0 and the current cached database on 2026-10-07; that scan reported no vulnerabilities. This result does not assert general security or replace release evidence. The 62 HIGH/2 CRITICAL findings above belong to the earlier Debian build preserved in the historical SBOM example. Generate new inventories and enforce promotion policy against the rebuilt immutable image identities before publishing a release.
