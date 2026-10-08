# Exercise — Containerize

## 1. Build the images

Start Docker and run from the repository root:

```console
task containers:build VERSION=1.0.0
```

## 2. Inspect an image

```console
docker image inspect ghcr.io/eoap/waterbodies-crop:1.0.0
docker run --rm ghcr.io/eoap/waterbodies-crop:1.0.0 waterbodies crop --help
```

- Repeat the inspection for `norm-diff`, `otsu` and `stac`.
- Compare tags with image identities. A local image ID is distinct from a registry repository digest; record a repository digest once an image has been published and inspected.

## Verify your work

This task inventories the container references in the canonical contract and runs `tests/supply_chain`. The tests cover version identities, rejection of `latest`, release preparation, OCI metadata and bundled SBOM integrity. The ORAS round-trip test can be skipped when ORAS is unavailable.

Run from the repository root:

```console
task supply-chain:check
```

Success means the inventory completes and the selected tests pass; read any skip reason. This task does not build or execute your Docker images, so retain the image inspection and help checks from step 2. For failures, inspect the named image reference or failing evidence/packaging assertion.

**Expected outcome:** All four declared dependencies have version identities; no canonical image uses latest.

Compare [the solution](solution.md). Return to [the module](README.md).
