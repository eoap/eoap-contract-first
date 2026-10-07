# Supply-chain assurance and promotion

CWL declares software relationships. Inventory tooling exposes them; security tooling and policy decide whether a tested artifact may be promoted. The contract enables a secured software supply chain but does not secure it by itself.

| Capability | Tool or boundary | What it establishes |
| --- | --- | --- |
| Contract | CWL + cwltool | Typed processing interface and reachable steps. |
| Image build | Docker | Executable environments with release tags. |
| Inventory | cwl2sbom + Trivy | Declared container dependencies and image contents. |
| Identity | images.lock.json | Inspected repository digests and platform. |
| Vulnerabilities | Trivy sbom | Known vulnerabilities against a current database. |
| Policy | supply-chain/policy/scan.sh | Reject known HIGH/CRITICAL findings. |
| Annotations | cwl2oci | Software metadata and selected CWL process identity. |
| Packaging | ORAS | OCI-distributed application/cwl artifact. |
| Evidence association | ORAS attach | Digest-addressed CycloneDX referrers. |
| Signature/provenance | Optional signing exercise | Separate identity and build assertions. |
| Promotion | Protected GitHub environment | Explicit release authorization after gates. |
| Deployment | ZOO API | Installation and execution of pulled promoted CWL. |

## Local preparation

```console
task reference:test
task release:prepare VERSION=1.0.0
task containers:build VERSION=1.0.0
task sbom:generate CONTRACT=build/release/waterbodies.cwl PLATFORM=linux/amd64
task sbom:check CONTRACT=build/release/waterbodies.cwl
```

The verified `cwl2sbom` forces Trivy's `--image-src remote`: images must exist in an accessible registry, not only the local Docker cache. Push to a temporary local registry for an integration exercise, or use the protected release pipeline for GHCR. Real repository digests require registry inspection. No illustrative image references are silently replaced with unrelated images. The output directory must not exist: choose another `SBOM=build/sbom-new` for a repeat run.

The bundle contains workflow.cdx.json (workflow/tool/image relationships), images/*.cdx.json (image contents), images.lock.json (reference, repository digests, platform, checksums, generator versions and step associations) and coverage.json (reachable tool coverage and limitations). Coverage complete means every reachable declared tool is covered; it does not mean every runtime dependency is covered. The workflow SBOM marks its aggregate composition incomplete intentionally.

```console
uv run python scripts/supply_chain.py check --contract build/release/waterbodies.cwl --bundle build/sbom
bash supply-chain/policy/scan.sh build/sbom
```

The educational vulnerability policy rejects HIGH or CRITICAL findings, including unfixed vulnerabilities. It makes no license-policy claim and has no hidden exceptions. An exception needs a separately reviewed policy change with rationale and expiry; do not hide findings with an automatic ignore. Database availability and freshness affect results. A passing scan does not prove security.

## Immutable execution and application packaging

After the versioned images have been pushed and inspected:

```console
uv run python scripts/supply_chain.py prepare --version 1.0.0 --lock build/sbom/images.lock.json
uv run cwltool --validate build/release/waterbodies.cwl#waterbodies
uv run transpiler-mate cwl2oci --output build/annotations.json build/release/waterbodies.cwl#waterbodies
uv run bash supply-chain/oras/package.sh 1.0.0 build/release/waterbodies.cwl build/annotations.json
oras manifest fetch --oci-layout build/oci:1.0.0
oras pull --oci-layout build/oci:1.0.0 -o build/restored
```

This is local packaging, with no authenticated push. ORAS receives the actual generated `$manifest` annotation wrapper. The application/cwl media type follows EOAP advanced-tooling conventions. The script supplies a fixed example creation timestamp so identical contract and metadata produce the same local manifest digest; release builds should supply their declared release time consistently if that field is changed.

The OCI manifest refers to the CWL, which declares four immutable image dependencies. The SBOM bundle describes the inspected versioned references and their digests. The release verifies that the exact pinned digest set matches the lock before promotion.

## Registry evidence graph

```text
waterbodies:1.0.0 → EOAP manifest digest
    ├── waterbodies.cwl (application/cwl)
    ├── generated OCI annotations
    └── workflow CycloneDX SBOM referrer

waterbodies-crop@sha256:...      → image CycloneDX referrer
waterbodies-norm-diff@sha256:... → image CycloneDX referrer
waterbodies-otsu@sha256:...      → image CycloneDX referrer
waterbodies-stac@sha256:...      → image CycloneDX referrer
```

The ellipses are diagram placeholders, not usable digests. `supply-chain/oras/publish.sh` copies the local OCI layout and attaches real evidence to resolved immutable subjects using ORAS. The workflow bundle lock and coverage are also associated with the application in protected release CI. Referrer discoverability depends on the registry's OCI support; verify `oras discover` and retrieve the attached evidence rather than assuming attachment succeeds everywhere.

## Release boundary

The release workflow is manually dispatched with version, previous promoted CWL location and explicit reviewed compatibility classification. It runs all local checks, compares the contract, builds and publishes four versioned images, captures immutable identities through cwl2sbom, verifies coverage and checksums, scans image inventories, writes digest-pinned release CWL, generates annotations, packages, associates evidence, then publishes the promotion tag. Staging uses a candidate tag; the final version tag is created only after evidence gates.

Configure a GitHub environment named `release` with required reviewers. Its job alone receives packages:write. PR workflows have contents:read and perform no publication. A manual `task release:publish` requires `WATERBODIES_PUBLISH=approved` after reviewing the same gates; it does not itself build or upload the image dependencies.

## Optional signing exercise

This bootstrap does not fabricate signatures or claim to establish provenance. A team can add Sigstore Cosign signing and attestations after selecting an issuer/identity trust policy and verifying its current official CLI for its installed version. Sign immutable EOAP and container subjects; verify both signature identity and artifact digest before promotion. A signature answers who asserts an identity; provenance answers how an artifact was built; the SBOM answers what was inventoried. Each is independently checked. Do not treat any one as a substitute for the others.
