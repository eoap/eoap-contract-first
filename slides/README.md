# Water Bodies instructor deck

[teacher-deck.md](teacher-deck.md) is the source of truth: 65 slides across 13 sections, eight demos and six interaction points. It covers contract-first design, Water Bodies science, tool contracts, CLI derivation, implementation, composition, containers/execution, derived artifacts, evolution, supply chain, OCI, OGC deployment, and recap. The pacing slide recommends 215 minutes including a break, with an adapted two-session plan. Presenter material is teacher-facing; the module exercises remain the learner handouts.

## Build and present

Install Node.js 22 LTS (or a compatible Node >=18), npm and Task. Marp CLI 4.5.1 is a local development dependency; commit package-lock.json and use `npm ci`. No global npm installation is needed. PDF/image exports additionally require Chrome, Edge or Firefox. Course demos also need the prerequisites in [the course guide](../docs/prerequisites.md).

Run from the repository root:

```console
task slides:setup
task slides:check
task slides:preview
task slides:html
task slides:pdf
task slides:notes
```

Preview serves `http://localhost:8080`; open `teacher-deck.md` from its index. Stop with Ctrl-C. HTML/PDF/notes exports go to `build/slides/`. The HTML contains the SVG assets inline and supports Marp's presenter view; the PDF includes presenter-note annotations and outlines. Keep teacher exports private if notes contain delivery-specific information. The PDF browser can be selected with `CHROME_PATH=/absolute/path/to/chrome task slides:pdf`. Marp's CLI also supports `--browser-path` if using the direct commands below.

Equivalent CLI commands, from `slides/` after `npm ci`:

```console
npx --no-install marp --server --watch . --theme-set themes/eoap.css
npx --no-install marp teacher-deck.md --theme-set themes/eoap.css -o ../build/slides/teacher-deck.html
npx --no-install marp teacher-deck.md --theme-set themes/eoap.css --allow-local-files --pdf --pdf-notes --pdf-outlines -o ../build/slides/teacher-deck.pdf
```

Create `../build/slides` before direct exports. Only allow local files for this trusted repository deck. Syntax follows the [Marp CLI documentation](https://github.com/marp-team/marp-cli/blob/main/README.md); normal HTML comments are [Marpit presenter notes](https://marpit.marp.app/usage?id=presenter-notes). `<!-- _class: demo -->` is a local slide directive, not a presenter note. Use normal comments for teaching goals, misconceptions, questions, expected responses, transitions and exact live commands. Keep lengthy explanations in notes rather than projected text.

## Visual system and assets

[themes/eoap.css](themes/eoap.css) declares `@theme eoap` and imports Marp's default theme. The build registers it using `--theme-set`. Edit its colors, spacing and typography directly. The 16:9 theme uses navy/teal high-contrast surfaces, 48px headings, 30px body text and 25px code; divider/title slides are dark, demo slides teal and interaction slides amber. Diagram and table styles retain projected readability. No arbitrary HTML or Mermaid plugin is required.

[assets/architecture.svg](assets/architecture.svg) is an original code-native conceptual diagram created for this repository under its Apache-2.0 license. It summarizes contracts, execution, evidence and deployment, rather than claiming to be generated CWL dataflow. The other diagrams are readable Markdown text. The actual generated workflow diagram source is demonstrated through `task artifacts:derive` in `reference/expected/diagrams/`; this avoids an external rendering service or a competing manual scientific graph. No stock imagery or external fonts are used.

## Synchronization and rehearsal

Use `reference/waterbodies.cwl` for tool IDs, bindings, scatter order, output types, image names and version. Use `Taskfile.yaml` for demo commands, `reference/src/waterbodies/*_impl.py` for behavior and `supply-chain/oras/` for packaging/referrer mechanics. The slides deliberately use the actual **1.0.0**, rather than a hypothetical 1.2.0. After contract changes, regenerate projections, update the relevant slide examples and notes, and run `task slides:check`. Tests validate shown Task commands, scientific CLI options against the installed generated CLI, canonical image/version references, and CWL snippets against resolved models. Re-export and visually inspect after changing typography or content.

The deck follows the pinned tooling source evidence in [architecture.md](../docs/architecture.md). Generation is local: cwl2sbom produces inventories; cwl2oci produces annotations; ORAS separately packages and distributes. An inventory is neither a vulnerability report nor a signature. Version tags are mutable. Coverage refers to declared tools, not all possible runtime software. Signing/provenance and license policy are separate discussion topics, not implemented course capabilities.

Before class, run `task setup`, `task reference:test`, `task workflow:run` and `task containers:build`. Pre-generate slow evidence. DEMO 6 uses real local images, a disposable registry and `task supply-chain:integration`, writing `build/sbom-local`. That directory must be new; remove only reviewed disposable output or call `uv run bash scripts/local_supply_chain.sh build/sbom-local-next` for another run. Do not rerun against an existing directory. The committed historical Debian inventory is an inspection fallback, not release evidence for the newer Rocky images. DEMO 7 uses a local OCI layout and does not publish.

## Prepare the remote deployment demo

Remote execution requires a running configured ZOO API/backend, authenticated access where required, a reviewed promoted artifact digest, available component images, and backend-accessible staged inputs. This deck provides commands and instructor preparation, not a fabricated successful live job. The routes and CWL deployment behavior follow [EOAP's ZOO deployment tutorial](https://eoap.github.io/ogc-api-processes-with-zoo/deploy-application/) and [its resource table](https://eoap.github.io/ogc-api-processes-with-zoo/describe-process/). The package endpoint and deployment selector are server-specific extensions; OCI references are pulled before posting CWL bytes.

Configure these values in the instructor terminal, replacing the placeholders:

```bash
export API='http://localhost:8080/ogc-api'
export EOAP_REF='ghcr.io/eoap/waterbodies@sha256:REPLACE_WITH_PROMOTED_DIGEST'
export PROCESS_ID='waterbodies'
task slides:deployment-demo MODE=deploy
task slides:deployment-demo MODE=inspect
```

The helper requires a full sha256 digest for deployment and pulls into a fresh directory. Inspect referrers and verify the reviewed release evidence/trust policy before running it; `oras discover` alone does not verify trust. Confirm the returned process ID, adjusting PROCESS_ID if necessary. Configure authentication through the environment's established client mechanism; do not commit credentials. The helper's plain curl commands assume an API reachable with that mechanism.

Stage all of `data/fixtures/source` with relative links preserved on storage the backend can access. Consult the deployed input schema and backend's Directory staging convention. Prepare `build/execute.json` from [the documented example](../supply-chain/examples/execute.json), replacing its placeholder location with an actually staged Directory; an Item JSON URL or local learner path is insufficient. Some backends require an explicit stage-in wrapper: use the environment's verified wrapper. Then:

```bash
task slides:deployment-demo MODE=execute
# Read build/slides/deployment/job.headers and job.json; follow the returned links.
export JOB_ID='REPLACE_WITH_RETURNED_JOB_ID'
task slides:deployment-demo MODE=monitor
```

Follow status until completion and retrieve the returned result href. Validate the output Item/extensions with PySTAC. For the compact fixture, verify 6×6 pixels and 18 water pixels. Record promoted digest, installed package identity, process ID, successful job ID and result validation. See [deployment.md](../docs/deployment.md) for the full staging boundary.

Customize the instructor/event identity, API URL, authentication, storage location, process/job identifiers and promoted release identity before delivery. Never run `release:publish` as an unannounced demo; it is a protected publication step with its own release authorization and policy gates.

## Build dependency audit limitation

The build uses the current Marp CLI 4.5.1, with a locked compatible override to `@xmldom/xmldom` 0.9.12 to address XML-parser advisories. On 2026-10-07, `npm audit` still reports eight high and two low affected packages in the Marp dependency tree, including inherited findings. The remaining direct advisory origins are basic-ftp, extract-zip and KaTeX. Automatic compatible fixes do not resolve them; npm's forced suggestion would downgrade Marp to an obsolete release. No audit findings were suppressed. This is an unresolved upstream build-tool security limitation, separate from the passing Python quality gates and the demonstrated HTML/PDF exports. Run `npm --prefix slides audit` when updating the pinned toolchain; review the [FTP advisory](https://github.com/advisories/GHSA-c475-qrg2-pj4r), [archive advisory](https://github.com/advisories/GHSA-jmr9-qjv8-65gv) and [KaTeX advisory](https://github.com/advisories/GHSA-238p-pmpm-9mq7). The export pipeline uses the locally installed browser and trusted repository source, but this does not clear those findings.
