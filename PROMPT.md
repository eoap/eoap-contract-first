# Mission

Bootstrap a complete GitHub repository for the EOAP organization that becomes the **canonical Water Bodies reference application and e-learning journey for CWL contract-first EO Application Package development**.

Working repository name:

`eoap/waterbodies-learning`

Do not create only scaffolding. Deliver a coherent, runnable first version of the repository.

The repository must teach and demonstrate the complete lifecycle:

```text
Application intent
        ↓
CWL contract
        ↓
CLI derivation
        ↓
Processing implementation
        ↓
Workflow composition
        ↓
Containerization
        ↓
Execution and testing
        ↓
Derived documentation and service artifacts
        ↓
Contract evolution and compatibility
        ↓
Research-software metadata
        ↓
Supply-chain inventory and assurance
        ↓
Versioned EOAP OCI artifact
        ↓
OCI registry
        ↓
OGC API - Processes deployment
        ↓
Execution
```

The central architectural principle is:

> **The CWL contract is the authoritative description of the EO application. Implementations, interfaces, workflow composition, documentation, metadata, supply-chain evidence, packaging and deployment artifacts are derived from or traceable back to that contract.**

The second major message is:

> **A machine-readable EO application contract enables a more secure and auditable software supply chain.**

Do not claim that CWL or Transpiler-Mate alone secures the supply chain. Clearly distinguish between:

- contract definition,
- inventory generation,
- SBOM generation,
- OCI annotations,
- container/image identity,
- vulnerability scanning,
- policy enforcement,
- artifact attachment,
- signing/attestation,
- promotion,
- deployment.

The repository should teach how these capabilities compose into a secured delivery process.

---

# 1. Inspect canonical repositories before implementation

Before writing code, inspect the current implementation and documentation of relevant repositories.

At minimum inspect:

- `eoap/mastering-app-package` including branch feature/enhancements
- `eoap/ogc-api-processes-with-zoo`
- `eoap/advanced-tooling`
- `eoap/application-package-patterns`
- `transpiler-mate/cwl2click`
- `transpiler-mate/transpiler-mate-runtime`
- `transpiler-mate/transpiler-mate-api`
- `transpiler-mate/cwl-loader`
- `transpiler-mate/cwl2markdown`
- `transpiler-mate/cwl2puml`
- `transpiler-mate/cwl2inputs`
- `transpiler-mate/cwl2ogc`
- `transpiler-mate/cwl2oci`
- `transpiler-mate/cwl2sbom`
- `transpiler-mate/cwl-baseline-plugin`

Also inspect other current EOAP/Transpiler-Mate repositories when they provide relevant patterns.

Do not infer functionality from repository names.

Inspect actual source code, tests, examples and documentation.

Record important architectural decisions and reused patterns in:

```text
docs/architecture.md
```

When this specification conflicts with the current behavior of an upstream project, prefer verified upstream behavior and document the deviation.

Do not invent unsupported Transpiler-Mate features.

---

# 2. Reference application: Water Bodies

Use the existing EOAP Water Bodies application as the scientific and processing reference.

The canonical processing chain is:

```text
                          ┌── crop(green) ──┐
STAC Item + AOI + EPSG ───┤                 ├── norm-diff ── otsu ── stac ── STAC Catalog
                          └── crop(nir) ────┘
```

Preserve the meaningful behavior of the existing EOAP Water Bodies implementation.

The four processing components are:

```text
crop
norm-diff
otsu
stac
```

Do not replace this with a toy processing chain.

Use compact fixtures for tests, but retain the real architectural and scientific behavior.

---

# 3. Contract-first development

The pedagogical direction must be:

```text
application intent
        ↓
CWL contract
        ↓
generated interface
        ↓
implementation
        ↓
composition
        ↓
execution environment
        ↓
derived artifacts
        ↓
release and assurance
        ↓
deployment
```

It must NOT primarily teach:

```text
write Python script
        ↓
build CLI
        ↓
wrap existing CLI in CWL
```

This distinction is fundamental.

Describe the methodology as:

> **top-down contract design with bottom-up implementation and verification**

Top-down:

```text
Application
    ↓
Workflow
    ↓
Tool contracts
    ↓
Implementation requirements
```

Bottom-up verification:

```text
Tool implementation
    ↓
Tool tests
    ↓
Workflow execution
    ↓
Application verification
```

---

# 4. Canonical CLI contract

The CWL contract must define one coherent CLI namespace:

```console
waterbodies --help
```

with four subcommands:

```console
waterbodies crop --help
waterbodies norm-diff --help
waterbodies otsu --help
waterbodies stac --help
```

Use the actual current bundled behavior of `transpiler-mate/cwl2click`.

The `CommandLineTool` contracts should use:

```yaml
baseCommand:
- waterbodies
- crop
```

```yaml
baseCommand:
- waterbodies
- norm-diff
```

```yaml
baseCommand:
- waterbodies
- otsu
```

```yaml
baseCommand:
- waterbodies
- stac
```

The conceptual Click hierarchy is therefore:

```text
waterbodies
├── crop
├── norm-diff
├── otsu
└── stac
```

Generate this using the verified current `cwl2click --bundle` mechanism.

Do not independently hand-design another Click contract.

The CWL remains authoritative.

---

# 5. Canonical CWL organization

The final canonical contract must live at:

```text
reference/waterbodies.cwl
```

Prefer a single `$graph` containing:

```text
Workflow #waterbodies

CommandLineTool #crop
CommandLineTool #norm-diff
CommandLineTool #otsu
CommandLineTool #stac
```

unless validation, tooling constraints or educational clarity justify another organization.

Prefer these IDs:

```text
waterbodies
crop
norm-diff
otsu
stac
```

Verify hyphenated identifiers against:

- CWL parsing,
- workflow references,
- cwl-utils,
- Transpiler-Mate,
- cwl2click,
- generated Python symbols.

If a different identifier is required by actual tooling, use the smallest justified change and document why.

---

# 6. Tool contracts

Use the existing EOAP Water Bodies application as the source for the actual semantics.

## crop

Design approximately:

```yaml
class: CommandLineTool
id: crop

baseCommand:
- waterbodies
- crop

inputs:

  item:
    type: Directory
    inputBinding:
      prefix: --input-item

  aoi:
    type: string
    inputBinding:
      prefix: --aoi

  epsg:
    type: string
    inputBinding:
      prefix: --epsg

  band:
    type: string
    inputBinding:
      prefix: --band

outputs:

  cropped:
    type: File
    outputBinding:
      glob: "*.tif"
```

Expected interface:

```console
waterbodies crop \
  --input-item <item> \
  --aoi <aoi> \
  --epsg EPSG:4326 \
  --band green
```

## norm-diff

Design a cwl2click-compatible option interface.

Prefer approximately:

```yaml
baseCommand:
- waterbodies
- norm-diff
```

with:

```text
rasters : File[]
```

Expected CLI behavior should be approximately:

```console
waterbodies norm-diff \
  --rasters green.tif \
  --rasters nir.tif
```

Output:

```text
ndwi : File
```

Preserve the actual normalized-difference behavior of the existing Water Bodies implementation.

## otsu

Use:

```yaml
baseCommand:
- waterbodies
- otsu
```

Input:

```text
raster : File
```

Expected interface:

```console
waterbodies otsu --raster norm_diff.tif
```

Output:

```text
binary-mask : File
```

Preserve the actual Otsu processing behavior.

## stac

Use:

```yaml
baseCommand:
- waterbodies
- stac
```

Inputs should include:

```text
item
water-body
```

Expected interface approximately:

```console
waterbodies stac \
  --input-item <original-item> \
  --water-body otsu.tif
```

Output:

```text
stac-catalog : Directory
```

Preserve the existing EOAP Water Bodies STAC behavior where appropriate.

---

# 7. Canonical workflow

The workflow must demonstrate composition of the same contracts used to derive the CLI.

Default bands:

```yaml
bands:
  type: string[]
  default:
  - green
  - nir
```

Use CWL scatter for crop.

Conceptually:

```yaml
steps:

  crop:
    run: "#crop"

    in:
      item: item
      aoi: aoi
      epsg: epsg
      band: bands

    scatter: band
    scatterMethod: dotproduct

    out:
    - cropped

  norm-diff:
    run: "#norm-diff"

    in:
      rasters: crop/cropped

    out:
    - ndwi

  otsu:
    run: "#otsu"

    in:
      raster: norm-diff/ndwi

    out:
    - binary-mask

  stac:
    run: "#stac"

    in:
      item: item
      water-body: otsu/binary-mask

    out:
    - stac-catalog
```

Validate actual CWL syntax instead of blindly copying this sketch.

The dataflow must remain:

```text
bands
  │
  ├── green ─→ crop ─┐
  │                  │
  └── nir ───→ crop ─┤
                     │ File[]
                     ▼
                 norm-diff
                     │
                     │ NDWI
                     ▼
                    otsu
                     │
                     │ water mask
                     ▼
original item ────→ stac
                     │
                     ▼
                STAC Catalog
```

This workflow is central to the course.

---

# 8. Repository roles

The repository has three simultaneous purposes.

## E-learning course

A newcomer should progress from understanding the algorithm to deploying a secured, versioned EO Application Package.

## Golden reference implementation

Developers should be able to inspect:

```text
reference/
```

and understand what a well-designed EOAP application looks like.

## Integration fixture

EOAP and Transpiler-Mate projects should be able to test their tooling against the canonical Water Bodies contract.

Avoid tutorial shortcuts that make the reference implementation unsuitable for integration testing.

---

# 9. Repository structure

Bootstrap approximately:

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── pyproject.toml
├── Taskfile.yaml
├── mkdocs.yml
├── .gitignore
├── .pre-commit-config.yaml
│
├── docs/
│   ├── index.md
│   ├── learning-path.md
│   ├── prerequisites.md
│   ├── architecture.md
│   ├── supply-chain.md
│   ├── deployment.md
│   ├── glossary.md
│   └── contributing.md
│
├── modules/
│   ├── 00-waterbodies/
│   ├── 01-design-the-contract/
│   ├── 02-derive-the-cli/
│   ├── 03-implement-crop/
│   ├── 04-implement-norm-diff/
│   ├── 05-implement-otsu/
│   ├── 06-implement-stac/
│   ├── 07-compose-the-workflow/
│   ├── 08-containerize/
│   ├── 09-run-the-application/
│   ├── 10-derive-artifacts/
│   ├── 11-assure-the-contract/
│   ├── 12-publish-research-software/
│   └── 13-secure-promote-deploy/
│
├── reference/
│   ├── waterbodies.cwl
│   ├── inputs.yaml
│   ├── pyproject.toml
│   │
│   ├── src/
│   │   └── waterbodies/
│   │       ├── __init__.py
│   │       ├── cli.py
│   │       ├── crop_impl.py
│   │       ├── norm_diff_impl.py
│   │       ├── otsu_impl.py
│   │       └── stac_impl.py
│   │
│   ├── containers/
│   │   ├── crop/
│   │   ├── norm-diff/
│   │   ├── otsu/
│   │   └── stac/
│   │
│   └── expected/
│       ├── docs/
│       ├── diagrams/
│       ├── ogc/
│       ├── baseline/
│       ├── sbom/
│       ├── oci/
│       └── publication/
│
├── supply-chain/
│   ├── README.md
│   ├── oras/
│   ├── policy/
│   └── examples/
│
├── data/
│   ├── README.md
│   └── fixtures/
│
├── tests/
│   ├── contract/
│   ├── cli/
│   ├── tools/
│   ├── workflow/
│   ├── supply_chain/
│   └── learning/
│
└── .github/
    └── workflows/
        ├── quality.yaml
        ├── validate-cwl.yaml
        ├── test-cli.yaml
        ├── test-workflow.yaml
        ├── supply-chain.yaml
        ├── release.yaml
        └── docs.yaml
```

Refine where justified, but preserve the conceptual separation between:

```text
modules/       progressive learning journey
reference/     canonical final implementation
supply-chain/  release/promotion mechanics
```

Do not encode lessons as Git branches.

---

# 10. Consistent module grammar

Each learning module should preferably contain:

```text
README.md
lesson.md
exercise.md
starter/
solution/
checks/
```

Use only directories that provide actual value.

Every module must clearly answer:

1. What are we designing?
2. Why does it belong in the contract?
3. What can be derived from it?
4. How do we verify it?

Each module must provide:

- learning objectives,
- prerequisites,
- conceptual explanation,
- hands-on exercise,
- reproducible verification,
- expected outcome,
- next-step link.

Examples shown in documentation must correspond to real repository artifacts.

---

# 11. Learning journey

## Module 00 — Understand Water Bodies

Teach the scientific processing chain first.

Explain:

```text
green + nir
    ↓
normalized difference / NDWI
    ↓
Otsu threshold
    ↓
binary water mask
    ↓
STAC result
```

Explain the overall processing graph.

Do not start with YAML syntax.

---

## Module 01 — Design the contract

Introduce CWL as the application contract.

Design:

```text
waterbodies crop
waterbodies norm-diff
waterbodies otsu
waterbodies stac
```

Teach:

- `CommandLineTool`,
- IDs,
- `baseCommand`,
- typed inputs,
- typed outputs,
- `inputBinding`,
- metadata,
- required vs optional inputs.

There should initially be no processing implementation.

Reinforce:

```text
contract != implementation
```

---

## Module 02 — Derive the CLI

Use actual current:

```console
transpiler-mate cwl2click --bundle ...
```

The learner must see the contract produce:

```console
waterbodies --help
```

and:

```text
Commands:
  crop
  norm-diff
  otsu
  stac
```

Then:

```console
waterbodies crop --help
waterbodies norm-diff --help
waterbodies otsu --help
waterbodies stac --help
```

Do not manually reproduce these interfaces independently of CWL.

---

## Module 03 — Implement crop

Implement behavior behind the generated `crop` interface.

Teach:

```text
CWL input
    ↓
generated Click option
    ↓
Python callback argument
    ↓
processing implementation
```

Use canonical Water Bodies behavior.

---

## Module 04 — Implement norm-diff

Implement normalized-difference processing.

Use the real Water Bodies behavior.

Teach array/multiple inputs and the relationship between:

```text
File[]
```

and repeated CLI options where supported by current cwl2click behavior.

---

## Module 05 — Implement otsu

Implement Otsu thresholding.

Input:

```text
NDWI raster
```

Output:

```text
binary water mask
```

Keep scientific behavior faithful to the reference application.

---

## Module 06 — Implement stac

Turn the processing result into the expected STAC representation.

Teach why EO processing outputs need machine-readable data/product metadata.

Use existing EOAP Water Bodies STAC patterns.

---

## Module 07 — Compose the workflow

Introduce:

- `Workflow`,
- `steps`,
- `run`,
- `in`,
- `out`,
- `source`,
- `outputSource`,
- `scatter`,
- `scatterMethod`.

Scatter `crop` across:

```text
green
nir
```

Then compose:

```text
crop → norm-diff → otsu → stac
```

Emphasize that the workflow composes the same contracts used by the CLI.

---

## Module 08 — Containerize

Introduce execution environments only after contract, implementation and composition are understood.

Build four processing images.

The learner must understand that these are not anonymous containers: they are **versioned software dependencies of the EO Application Package**.

Use Semantic Versioning.

Canonical release examples:

```text
ghcr.io/eoap/waterbodies-crop:1.0.0
ghcr.io/eoap/waterbodies-norm-diff:1.0.0
ghcr.io/eoap/waterbodies-otsu:1.0.0
ghcr.io/eoap/waterbodies-stac:1.0.0
```

Do not use `latest` in the canonical release CWL.

Explain the distinction between:

```text
human release identity
image:1.0.0
```

and:

```text
immutable execution identity
image@sha256:...
```

Where practical, demonstrate digest-pinned execution for reproducibility.

---

## Module 09 — Run the Application

Execute:

- individual tools,
- complete workflow.

Use compact local fixtures.

Do not require large remote EO datasets for basic CI.

Validate resulting raster files and STAC structures.

---

## Module 10 — Derive artifacts

Demonstrate the return on investment of contract-first design.

Starting from CWL, use current Transpiler-Mate plugins to derive only genuinely supported artifacts.

Potential projections include:

```text
CWL
 ├── cwl2click       → CLI
 ├── cwl2markdown    → documentation
 ├── cwl2puml        → diagrams
 ├── cwl2inputs      → input templates
 ├── cwl2ogc         → OGC process representation
 └── other verified projections
```

If `cwl2webgl` or other plugins are useful and currently supported, include them only after verifying their behavior.

Do not commit fabricated “generated” artifacts.

Generated examples must be reproducible from repository commands.

---

## Module 11 — Evolve and assure the contract

Create realistic:

```text
v1/
└── waterbodies.cwl

v2/
└── waterbodies.cwl
```

Introduce a realistic API change.

Examples:

- add optional input,
- modify output,
- change type,
- add command,
- change requiredness.

Use actual `cwl-baseline-plugin` behavior.

Teach:

```text
compatible?
breaking?
minimum SemVer increment?
```

The learner should understand that the CWL is a versioned public processing API.

---

## Module 12 — Publish research software

Demonstrate how the application contract can support research-software publication.

Where actual current plugins support it, derive:

- citation metadata,
- CodeMeta,
- DataCite metadata,
- RO-Crate,
- related publication artifacts.

Clearly distinguish scientific/research publication metadata from software supply-chain evidence.

Do not conflate:

```text
citation
```

with:

```text
SBOM
```

or:

```text
attestation
```

---

# 12. Module 13 — Secure, promote and deploy

This is the capstone.

The learner must take the tested application and turn it into a **versioned, distributable EO Application Package with supply-chain evidence**, then deploy it to an OGC API – Processes server.

The journey is:

```text
validated CWL
      ↓
versioned processing containers
      ↓
container identities
      ↓
SBOM generation
      ↓
OCI annotation generation
      ↓
EOAP OCI packaging
      ↓
evidence attachment / association
      ↓
security/policy gates
      ↓
promotion
      ↓
OCI registry
      ↓
OGC API - Processes deployment
      ↓
execution
```

This module must communicate:

> Deployment consumes a tested and promoted application artifact, not an arbitrary source-tree snapshot.

---

# 13. Semantic versioning and artifact identity

Treat release versioning seriously.

For an application release such as:

```text
1.2.0
```

processing containers should be tagged coherently:

```text
ghcr.io/eoap/waterbodies-crop:1.2.0
ghcr.io/eoap/waterbodies-norm-diff:1.2.0
ghcr.io/eoap/waterbodies-otsu:1.2.0
ghcr.io/eoap/waterbodies-stac:1.2.0
```

and the EOAP artifact should have a versioned identity such as:

```text
ghcr.io/eoap/waterbodies:1.2.0
```

Do not assume all component versions must always equal the EOAP version if the architecture eventually supports independent component releases.

For this reference learning journey, coherent versions are acceptable because they make the lifecycle easier to understand.

Explain the distinction between:

```text
tag = convenient version reference
digest = immutable content identity
```

Use immutable identities where reproducibility/security requires them.

---

# 14. SBOM generation

Use the actual current `transpiler-mate/cwl2sbom`.

It currently generates CycloneDX SBOM information for containers declared by a CWL workflow using Trivy.

Use an explicit workflow entrypoint and platform.

The expected output family includes, according to current behavior:

```text
workflow.cdx.json
images/*.cdx.json
images.lock.json
coverage.json
```

Teach their different purposes.

The workflow SBOM should make the relationship visible:

```text
EO Application Package
       │
       ├── workflow
       │
       ├── crop step ─────→ crop container
       ├── norm-diff ─────→ norm-diff container
       ├── otsu ──────────→ otsu container
       └── stac ──────────→ stac container
```

The image SBOMs provide the software inventory of those container images.

The lock information associates inspected image references with reported identities, platform, step associations, checksums and generator information according to actual plugin behavior.

Do not claim that `cwl2sbom`:

- pushes OCI artifacts,
- attaches referrers,
- signs artifacts,
- performs policy enforcement.

It does not.

Those are downstream responsibilities.

Explain that tags are resolved during inspection and that digest-pinned references are preferable for subsequent reproducible execution.

---

# 15. OCI annotations

Use actual current `transpiler-mate/cwl2oci`.

It generates OCI annotation metadata from normalized software metadata and the selected CWL process.

Use generated standard properties such as:

```text
org.opencontainers.image.*
```

and CWL-specific properties such as:

```text
org.cwl.*
```

where actually emitted.

The conceptual result may include information such as:

```json
{
  "org.opencontainers.image.version": "1.2.0",
  "org.cwl.entrypoint": "waterbodies",
  "org.cwl.type": "Workflow"
}
```

but use actual generated output in repository fixtures/tests.

Do not claim `cwl2oci` builds or pushes an OCI artifact.

It generates annotation metadata.

OCI packaging/publishing must be implemented separately.

---

# 16. EOAP as an OCI artifact

Package the CWL EO Application Package as an OCI-distributed artifact.

Use a current OCI client such as ORAS where appropriate.

Inspect current ecosystem conventions before selecting media types, artifact types, annotations or referrer relationships.

Do not invent private conventions unnecessarily.

The conceptual registry topology should be documented as:

```text
ghcr.io/eoap/waterbodies:1.2.0
        │
        ├── CWL Application Package
        ├── OCI annotations
        └── associated supply-chain evidence

dependencies:

ghcr.io/eoap/waterbodies-crop:1.2.0
        └── SBOM

ghcr.io/eoap/waterbodies-norm-diff:1.2.0
        └── SBOM

ghcr.io/eoap/waterbodies-otsu:1.2.0
        └── SBOM

ghcr.io/eoap/waterbodies-stac:1.2.0
        └── SBOM
```

Also consider associating the workflow-level CycloneDX SBOM with the EOAP artifact.

Use OCI referrers/attachments only according to current supported tooling and registry behavior.

Keep the packaging mechanics explicit and reproducible.

---

# 17. Supply-chain evidence

Teach the distinction between the application and evidence about the application.

Conceptually:

```text
                     EOAP
                      │
           waterbodies:1.2.0
                      │
       ┌──────────────┼───────────────┐
       │              │               │
      CWL        annotations      workflow SBOM
                                      │
                       ┌──────────────┼─────────────┐
                       │              │             │
                     crop         norm-diff       otsu ...
                       │              │             │
                     SBOM           SBOM          SBOM
```

The exact OCI graph should follow verified OCI tooling capabilities.

Do not pretend that simply attaching an SBOM makes an artifact secure.

Explain that SBOMs enable:

- inventory,
- traceability,
- vulnerability analysis,
- license analysis,
- policy decisions,
- incident response.

---

# 18. Vulnerability and policy gates

Where feasible, demonstrate downstream scanning using actual tools.

`cwl2sbom` uses Trivy to inspect images but SBOM generation and security policy are distinct concerns.

The course should demonstrate the conceptual progression:

```text
inventory
    ↓
vulnerability/license analysis
    ↓
policy evaluation
    ↓
release decision
```

Avoid arbitrary security theater.

If implementing a CI policy gate, keep it transparent and educational.

Document:

- what is checked,
- why,
- severity thresholds if used,
- exceptions,
- limitations.

Do not imply zero vulnerabilities means secure software.

---

# 19. Signing and attestations

If the surrounding EOAP ecosystem already has a preferred signing/attestation mechanism, use it.

Otherwise, signing/attestation may be demonstrated using a mainstream OCI-compatible mechanism only after inspecting current recommended practice.

Keep signing logically separate from:

```text
SBOM generation
```

and from:

```text
OCI annotation generation
```

Conceptually:

```text
artifact
   │
   ├── SBOM          what software is present?
   ├── provenance    how was it produced?
   ├── signature     who asserts this identity?
   └── policy        may this artifact be promoted?
```

Do not invent cryptographic claims.

If signing cannot be implemented safely/reproducibly in the bootstrap environment, provide a documented optional exercise rather than faking it.

---

# 20. Release and promotion pipeline

Create a release pipeline with a conceptual order similar to:

```text
validate CWL
     ↓
contract compatibility
     ↓
lint / test
     ↓
build processing containers
     ↓
tag x.y.z
     ↓
push containers
     ↓
capture immutable identities
     ↓
generate SBOMs
     ↓
security / policy checks
     ↓
generate OCI annotations
     ↓
package EOAP OCI artifact
     ↓
attach/associate evidence
     ↓
optional signing / attestation
     ↓
promote release
```

Avoid pushing real public artifacts from pull-request CI.

Separate:

```text
verification
```

from:

```text
release/promotion
```

Use GitHub Actions environments/permissions appropriately.

Keep credentials out of repository content.

---

# 21. Deployment to OGC API – Processes

The final deployment target is an OGC API – Processes server supporting EO Application Package deployment.

Inspect and follow current patterns from:

```text
eoap/ogc-api-processes-with-zoo
```

The final lesson must demonstrate the lifecycle:

```text
discover promoted EOAP
        ↓
deploy application package
        ↓
list processes
        ↓
describe waterbodies
        ↓
retrieve/inspect deployed package
        ↓
execute waterbodies
        ↓
monitor job
        ↓
retrieve result
```

Where supported by the server, demonstrate relevant resources conceptually equivalent to:

```text
/processes
/processes/{processID}
/processes/{processID}/package
/jobs/{jobID}
```

Use actual current API behavior and schemas.

Do not hard-code speculative endpoints.

The learner should finish by proving that:

```text
waterbodies
```

exists as a deployed process and can execute the canonical workflow.

---

# 22. End-to-end architectural story

The documentation should contain a prominent diagram communicating:

```text
                       DESIGN

                  waterbodies.cwl
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
         CLI          Workflow      Documentation
          │              │
          ▼              │
   Implementations       │
          │              │
          └──────┬───────┘
                 ▼
        Versioned containers
                 │
                 ▼
           Tests + assurance
                 │
        ┌────────┼─────────┐
        │        │         │
        ▼        ▼         ▼
      SBOM   OCI metadata  compatibility
        │        │         │
        └────────┼─────────┘
                 ▼
        Versioned EOAP OCI artifact
                 │
                 ▼
             OCI registry
                 │
                 ▼
        OGC API - Processes
                 │
                 ▼
              Execution
```

The course should make clear that the CWL contract connects:

- application design,
- CLI interface,
- workflow composition,
- execution environment,
- software inventory,
- release identity,
- documentation,
- interoperability,
- distribution,
- deployment.

---

# 23. Python package

The canonical implementation should live under:

```text
reference/src/waterbodies/
```

with approximately:

```text
__init__.py
cli.py
crop_impl.py
norm_diff_impl.py
otsu_impl.py
stac_impl.py
```

Use modern Python packaging.

Require Python 3.10+ unless verified dependencies justify a different minimum.

Avoid duplicating parameter declarations already present in CWL.

The generated/derived Click interface must remain consistent with the CWL contract.

---

# 24. Testing strategy

Implement multiple layers.

## Contract tests

Verify that:

- canonical CWL parses,
- selected workflow resolves,
- four tools exist,
- expected types exist,
- expected command hierarchy exists,
- workflow connections are correct,
- Docker/container declarations are covered.

## CLI tests

Verify:

```console
waterbodies --help
waterbodies crop --help
waterbodies norm-diff --help
waterbodies otsu --help
waterbodies stac --help
```

Verify representative invocations.

Establish that CLI shape comes from the CWL contract.

## Tool tests

Test:

- crop,
- norm-diff,
- otsu,
- stac

independently.

## Workflow tests

Run compact end-to-end fixture.

Verify:

- crop outputs,
- NDWI,
- water mask,
- STAC result.

## Supply-chain tests

Where practical verify:

- no canonical image uses `latest`,
- version tags follow SemVer,
- all executable workflow container declarations are inventoried,
- expected SBOM files are generated,
- coverage is acceptable,
- OCI annotation output contains required fields,
- packaging scripts are deterministic/reproducible where possible.

## Learning tests

Ensure commands and solution artifacts used in lessons do not silently rot.

---

# 25. Taskfile UX

Create a root `Taskfile.yaml`.

Make it the primary learner/developer interface.

Provide commands along the lines of:

```console
task setup
task quality
task test

task contract:validate

task cli:generate
task cli:test

task workflow:run
task workflow:test

task artifacts:derive

task sbom:generate
task sbom:check

task oci:annotations
task oci:package
task oci:inspect

task supply-chain:check

task docs:serve
task docs:build

task reference:test
```

For operations requiring registry credentials, clearly distinguish local/dry-run behavior from authenticated publication.

Consider:

```console
task release:prepare VERSION=1.2.0
```

and an explicitly protected:

```console
task release:publish VERSION=1.2.0
```

if appropriate.

Module-specific tasks may include:

```console
task lesson:01:check
task lesson:02:generate
task lesson:07:run
task lesson:10:derive
task lesson:13:package
```

Do not create a huge opaque Taskfile.

Tasks should delegate to understandable commands/scripts.

---

# 26. Documentation site

Use MkDocs following current EOAP/Transpiler-Mate conventions.

Suggested navigation:

```text
Home
Learning Path
Prerequisites
Architecture

Modules
  00 - Understand Water Bodies
  01 - Design the Contract
  02 - Derive the CLI
  03 - Implement Crop
  04 - Implement Normalized Difference
  05 - Implement Otsu
  06 - Implement STAC
  07 - Compose the Workflow
  08 - Containerize
  09 - Run the Application
  10 - Derive Artifacts
  11 - Evolve and Assure the Contract
  12 - Publish Research Software
  13 - Secure, Promote and Deploy

Reference
  Canonical CWL
  CLI
  Python Implementation
  Workflow
  Containers
  Generated Artifacts
  OCI Artifact
  SBOMs

Concepts
  Contract-First Development
  Application Packaging
  Semantic Versioning
  OCI Distribution
  Software Supply Chain
  Reproducibility
  OGC API - Processes

Contributing
Glossary
```

Favor executable examples, diagrams and observable results over excessive prose.

---

# 27. README

The root README should immediately communicate:

> **Build an Earth Observation Application Package from its CWL contract.**
>
> Water Bodies is the canonical EOAP reference application for learning contract-first processing design, implementation, workflow composition, software supply-chain assurance, packaging, distribution and deployment.

Show:

```text
                    waterbodies.cwl
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
         CLI            Workflow        Metadata
          │                │                │
          ▼                ▼                ▼
   implementation     containers      documentation
                           │
                           ▼
                     SBOM + identity
                           │
                           ▼
                     EOAP OCI artifact
                           │
                           ▼
                       registry
                           │
                           ▼
                  OGC API - Processes
```

Provide a short start:

```console
git clone ...
cd ...
task setup
task reference:test
```

and an obvious link to Module 00.

---

# 28. CI

Implement GitHub Actions covering:

## quality

- formatting,
- linting,
- tests,
- type checking where useful.

## validate-cwl

Validate:

- canonical contract,
- relevant module solutions.

## test-cli

Generate/use contract-derived CLI and test help surfaces.

## test-workflow

Execute compact reference workflow.

## supply-chain

On appropriate events:

- verify SemVer image references,
- verify no `latest`,
- generate/test SBOM bundle where feasible,
- verify inventory coverage,
- test OCI annotation generation,
- test local OCI packaging mechanics where feasible.

Do not require privileged publication in normal PR CI.

## release

On explicit release/tag workflow:

- determine version,
- verify compatibility/release requirements,
- build containers,
- publish versioned containers,
- collect immutable identities,
- generate SBOMs,
- perform configured checks,
- generate OCI annotations,
- package EOAP,
- publish EOAP OCI artifact,
- associate evidence,
- optionally sign/attest if implemented,
- verify published artifact.

Use least-privilege GitHub permissions.

## docs

Build MkDocs in strict mode.

---

# 29. Dependency discipline

Prefer existing EOAP and Transpiler-Mate components.

Do not reimplement capabilities already supplied by:

- cwl-loader,
- cwl-utils,
- transpiler-mate-runtime,
- cwl2click,
- cwl2sbom,
- cwl2oci,
- other relevant plugins.

Keep heavy optional tooling separate where practical.

Document external prerequisites such as:

- Trivy,
- ORAS,
- container tooling,
- CWL runner.

Provide version constraints where reproducibility benefits from them.

---

# 30. Quality conventions

Inspect recent EOAP and Transpiler-Mate repositories and follow current conventions where appropriate.

Prefer:

- Apache-2.0,
- modern `pyproject.toml`,
- Hatch if consistent with current ecosystem,
- Ruff,
- mypy where useful,
- pytest,
- Taskfile,
- pre-commit,
- MkDocs,
- Diátaxis-inspired documentation,
- Keep a Changelog conventions,
- Semantic Versioning.

Do not cargo-cult configuration.

The repository should remain understandable to learners.

---

# 31. Security language

Use precise language.

Prefer:

> enables a secured software supply chain

or:

> provides machine-readable inputs and evidence for software supply-chain assurance

over:

> CWL secures the supply chain

Explain that:

```text
CWL
 ↓
declares software relationships
 ↓
inventory tooling
 ↓
SBOM / identities / metadata
 ↓
security tooling + policy
 ↓
promotion decision
```

Security is an ecosystem property, not a single plugin output.

---

# 32. Important constraints

## One source of truth

Do not manually maintain multiple independent definitions of the same public interface.

CWL is authoritative.

## No fake generated artifacts

If documentation says something was generated, make it reproducibly generated.

## No `latest` in canonical releases

Use Semantic Versioning.

## Prefer immutable identity for reproducibility

Teach digest references and their purpose.

## Preserve the real Water Bodies workflow

Keep:

```text
crop(green/nir)
→ norm-diff
→ otsu
→ stac
```

## Keep supply-chain concepts distinct

Do not conflate:

- SBOM,
- vulnerability report,
- signature,
- provenance,
- OCI annotation,
- release metadata.

## Keep deployment as the ultimate outcome

The course does not end at creating an OCI artifact.

The promoted application must conceptually reach:

```text
OGC API - Processes
```

and execute.

---

# 33. Implementation order

Work in this order.

## Phase 1 — Research

Inspect upstream EOAP and Transpiler-Mate repositories.

Document verified assumptions.

## Phase 2 — Repository skeleton

Create:

- package structure,
- modules,
- docs,
- tests,
- Taskfile,
- CI skeleton.

## Phase 3 — Canonical CWL contract

Implement:

```text
reference/waterbodies.cwl
```

Validate it before implementing processing code.

## Phase 4 — CLI derivation

Generate/bootstrap using actual cwl2click bundled behavior.

Verify:

```text
waterbodies
├── crop
├── norm-diff
├── otsu
└── stac
```

## Phase 5 — Processing implementation

Port/refactor canonical Water Bodies behavior.

## Phase 6 — Workflow execution

Build compact fixtures and execute complete workflow.

## Phase 7 — Containers

Build four versioned processing images.

## Phase 8 — Learning modules

Construct lessons around the working reference implementation.

## Phase 9 — Derived artifacts

Integrate verified Transpiler-Mate projections.

## Phase 10 — Contract evolution

Create v1/v2 compatibility lesson.

## Phase 11 — Research publication

Integrate relevant research-software metadata projections.

## Phase 12 — Supply-chain inventory

Integrate `cwl2sbom`, Trivy and associated checks.

## Phase 13 — OCI packaging

Integrate `cwl2oci` annotation generation and actual OCI packaging/publishing mechanics separately.

## Phase 14 — Promotion

Implement/document release gates, evidence association and optional signing/attestation.

## Phase 15 — OGC API deployment

Connect the promoted Application Package to the EOAP OGC API – Processes deployment workflow.

## Phase 16 — Documentation and CI polish

Ensure the entire learning journey is reproducible.

---

# 34. Definition of done

The repository bootstrap is complete when a fresh clone can execute:

```console
task setup
task reference:test
```

and all core local checks succeed.

The canonical CWL validates.

The contract-derived CLI exposes:

```console
waterbodies crop --help
waterbodies norm-diff --help
waterbodies otsu --help
waterbodies stac --help
```

All four processing components pass tests.

The complete CWL Workflow executes against compact fixtures.

The workflow produces a valid Water Bodies STAC result.

The canonical container declarations use versioned references rather than `latest`.

The repository can generate the expected SBOM bundle using actual `cwl2sbom`.

The repository can generate actual OCI annotations using `cwl2oci`.

The EOAP can be packaged locally as an OCI artifact using documented tooling.

The release pipeline contains a clear path for publishing:

```text
waterbodies:x.y.z
```

and its processing container dependencies.

Supply-chain evidence can be associated with the appropriate OCI artifacts using verified tooling.

The repository clearly distinguishes tags from immutable digests.

The final module demonstrates or precisely documents deployment of the promoted EO Application Package to an OGC API – Processes implementation.

The deployed Water Bodies process can be:

- discovered,
- described,
- associated with its Application Package,
- executed,
- monitored,
- and its result retrieved.

MkDocs builds in strict mode.

Every learning module has a runnable path.

CI verifies the contract, CLI, processing components, workflow, documentation and feasible supply-chain checks.

---

# 35. Final learner takeaway

The completed learning journey should leave the learner able to explain:

```text
I designed an EO application as a CWL contract.

That contract defined its processing interfaces and composition.

I derived a Python CLI from it.

I implemented and tested the processing components.

I packaged those components as versioned containers.

The CWL identified the software composing my application.

I generated software inventory and SBOM evidence from that application.

I versioned and packaged the EO Application Package as an OCI artifact.

I promoted a known application artifact rather than an arbitrary source snapshot.

I deployed that Application Package to an OGC API - Processes server.

I executed the same application I designed at the beginning.
```

That narrative is the primary success criterion for the repository.

---

# 36. Execution behavior for Codex

Do not stop after producing a plan.

Inspect the referenced repositories and implement the repository.

Do not fill the repository with placeholder files merely to match the proposed tree.

Prefer working vertical slices.

When an upstream dependency prevents full implementation:

1. verify the limitation against current source/documentation,
2. implement everything possible,
3. document the exact limitation,
4. create a narrowly scoped TODO if necessary,
5. do not fake generated output or successful execution.

Do not silently change the architectural thesis to make implementation easier.

When choosing between a tutorial shortcut and a production-quality reference pattern, prefer the pattern that allows `reference/` to remain a credible EOAP golden implementation while keeping the learning modules approachable.

At completion, report:

- architecture implemented,
- final repository tree,
- canonical CWL structure,
- CLI generated from it,
- Water Bodies workflow behavior,
- test status,
- container/versioning strategy,
- SBOM outputs,
- OCI packaging strategy,
- supply-chain controls implemented,
- OGC API – Processes deployment path,
- setup/test/docs commands,
- deviations from this specification and why,
- unresolved limitations,
- recommended next improvements.

The resulting repository should credibly be describable as:

> **The EOAP canonical Water Bodies reference application and e-learning journey: from CWL contract design to a versioned, supply-chain-aware OCI Application Package deployed and executed through OGC API – Processes.**
