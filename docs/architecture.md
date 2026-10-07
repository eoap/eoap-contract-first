# Architecture and upstream evidence

Research performed against actual source, tests, examples and documentation on 2026-10-07. Tooling Git dependencies are pinned in pyproject.toml and uv.lock; docs/upstream-lock.json records projection revisions. The source anchors below make the choices reviewable.

| Repository | Inspected revision |
| --- | --- |
| [advanced-tooling](https://github.com/eoap/advanced-tooling/tree/bc3aef3cf43fca5fe961e6c6825fe1ed38294d80) | `bc3aef3cf43fca5fe961e6c6825fe1ed38294d80` |
| [application-package-patterns](https://github.com/eoap/application-package-patterns/tree/9c07fade21a06f718111ae853a154a680a82ebf0) | `9c07fade21a06f718111ae853a154a680a82ebf0` |
| [cwl-baseline-plugin](https://github.com/transpiler-mate/cwl-baseline-plugin/tree/63d5c7697bbb6e66d5687f4ef88eb36ccc155e7e) | `63d5c7697bbb6e66d5687f4ef88eb36ccc155e7e` |
| [cwl-loader](https://github.com/transpiler-mate/cwl-loader/tree/a51369615c16443b46bf7f63d1971d4acb389174) | `a51369615c16443b46bf7f63d1971d4acb389174` |
| [cwl2click](https://github.com/transpiler-mate/cwl2click/tree/43ddfd6a785c41ce9c62e28d52b7143aa654f5c3) | `43ddfd6a785c41ce9c62e28d52b7143aa654f5c3` |
| [cwl2codemeta](https://github.com/transpiler-mate/cwl2codemeta/tree/49ff46d301d90e347861ed4d29bad838526abb57) | `49ff46d301d90e347861ed4d29bad838526abb57` |
| [cwl2inputs](https://github.com/transpiler-mate/cwl2inputs/tree/f417674eb87374b39c9b7f4d5dd6cdfc8e098597) | `f417674eb87374b39c9b7f4d5dd6cdfc8e098597` |
| [cwl2markdown](https://github.com/transpiler-mate/cwl2markdown/tree/17ea06d1eae4452a2e17c8b6c104dc5624122c44) | `17ea06d1eae4452a2e17c8b6c104dc5624122c44` |
| [cwl2oci](https://github.com/transpiler-mate/cwl2oci/tree/ea662e629435e7d7f556674af071a905d605bf62) | `ea662e629435e7d7f556674af071a905d605bf62` |
| [cwl2ogc](https://github.com/transpiler-mate/cwl2ogc/tree/2ae57d69f835e39d02ecaf851bc3da9ea7cb061f) | `2ae57d69f835e39d02ecaf851bc3da9ea7cb061f` |
| [cwl2puml](https://github.com/transpiler-mate/cwl2puml/tree/3bc0efd5efdc450e58a3a60c9e5451a6dafe187f) | `3bc0efd5efdc450e58a3a60c9e5451a6dafe187f` |
| [cwl2sbom](https://github.com/transpiler-mate/cwl2sbom/tree/fc707a129947508eebd1b26c46e4bee63c06a4bd) | `fc707a129947508eebd1b26c46e4bee63c06a4bd` |
| [mastering-app-package](https://github.com/eoap/mastering-app-package/tree/3811d5e69b6645fdcb0f5d293ce8cb2242ebd92b) | `3811d5e69b6645fdcb0f5d293ce8cb2242ebd92b` |
| [mastering-enhancements](https://github.com/eoap/mastering-app-package/tree/12ecedd44525b6c745b211b88431d7de3b8a474e) | `12ecedd44525b6c745b211b88431d7de3b8a474e` |
| [ogc-api-processes-with-zoo](https://github.com/eoap/ogc-api-processes-with-zoo/tree/ddfaa45b2986bf6f5a0e0d88719322544a06772c) | `ddfaa45b2986bf6f5a0e0d88719322544a06772c` |
| [pystac](https://github.com/Terradue/pystac/tree/5941d0c361d409d35e0aeb36f6ae05b03008de71) | `5941d0c361d409d35e0aeb36f6ae05b03008de71` |
| [transpiler-mate-api](https://github.com/transpiler-mate/transpiler-mate-api/tree/850c966e4a0d9b18a94d28508fc63c189b55280c) | `850c966e4a0d9b18a94d28508fc63c189b55280c` |
| [transpiler-mate-runtime](https://github.com/transpiler-mate/transpiler-mate-runtime/tree/c55100e21d9e009f5ac67147794225547666f7cd) | `c55100e21d9e009f5ac67147794225547666f7cd` |

## Design decisions

The canonical `$graph` contains #waterbodies and four tools. Its generated interface is one waterbodies group. Hyphenated ids resolve in cwl-utils/cwl-loader, cwl2click converts Python symbols to snake_case, and the complete cwltool execution proves workflow references and repeated File[] options work.

The Water Bodies source is `mastering-app-package/water-bodies/command-line-tools/*/app.py`, plus `feature/enhancements` implementations and crop tests under the same component tree. Preserve EO common-band selection, AOI transformation, COG writes, `(green-nir)/(green+nir)`, Otsu strict greater-than, and the original Item identity/time in a self-contained result catalog. Enhancements supply grid checking, AOI polygons, finite-value classification and safe Item paths.

The source input is a staged Directory with catalog.json, Item JSON and local bands. Crop and STAC use PySTAC. Projection and Raster extension accessors replace the older rio-stac serialization path; metadata expresses the same cropped-grid product semantics. Geometry is built as an input value to a PySTAC Item, never as a handwritten STAC Item representation. We bundle official EO v1.1.0, projection v2.0.0 and raster v1.1.0 schemas and use PySTAC validation unchanged. Schema `$id` values identify the original sources. Schema files are upstream artifacts, not generated Python models.

## Verified APIs and deviations

- `cwl2click/src/cwl2click/plugin.py` writes a bundled module using the source stem and imports `{id}_impl.execute`. Its shipped Jinja template defines the group and options. Generated files remain unmodified; formatting/linting excludes only the generated artifact, whose structure is checked against fresh upstream generation.
- File[] needs an empty outer inputBinding plus per-item --rasters binding. Setting both prefixes repeats a stray array-level option. This is covered by an actual runner test.
- `cwl-loader` dereferences graph steps and returns typed cwl-utils process objects. No duplicate CWL models are handwritten. Generated statement order and timestamps vary; tests compare parsed Python statements.
- Runtime context resolution and `transpiler-mate-api` normalize Schema.org software metadata and expose plugin execution contexts. We use their plugin discovery and options directly.
- Current cwl2markdown 17ea06d ships `.md.jinja` files while requesting `.md`. The previous official 0.2.0 release renders correctly but pins API 1.0.0, conflicting with current runtime's API >=1.0.1 requirement. The narrow filename adapter in scripts/markdown_compat.py preserves all upstream rendering, with mutually compatible current versions. Actual output is waterbodies.md.jinja.
- cwl2puml emits PlantUML without an external rendering service; cwl2inputs generates templates that still need real locations; cwl2ogc emits a process description, not a deployment service.
- cwl2oci emits a JSON `$manifest` wrapper consumed by ORAS --annotation-file. It builds no artifact and performs no publication.
- cwl2sbom's discovery follows reachable tools, Trivy resolves images for an explicit platform, and generation writes workflow/image inventories plus lock and coverage evidence. Its workflow composition remains `incomplete` because undeclared runtime software is outside scope. It does not enforce vulnerability policy, sign, attach or publish.
- Baseline compares every normalized process and requires review for behavioral changes. Anonymous array schema names currently differ between loads and can create review findings. The known EPSG-default removal example is explicitly reviewed as major; release CI requires an independently supplied review classification.
- cwl2codemeta is verified and generates CodeMeta 3.0. CITATION.cff is editorial repository metadata. No unverified DataCite, RO-Crate or citation-generation functionality is claimed.
- advanced-tooling/docs/oci-artifacts.md establishes application/cwl and separate ORAS attachments; we use CycloneDX's media type instead of its SPDX example because cwl2sbom emits CycloneDX.
- application-package-patterns demonstrates explicit staging and workflow composition. We keep staging outside the scientific tools, and do not confuse a staged Directory with a remote URL.
- ogc-api-processes-with-zoo/docs/deploy-application.md verifies POST /processes?w=... with application/cwl+yaml. Its index, execute-monitor-process and package tutorials verify discovery, descriptions, execution, job status/results and package retrieval. No automatic OCI deploy endpoint is assumed: pull the promoted artifact first and deploy its bytes.

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
