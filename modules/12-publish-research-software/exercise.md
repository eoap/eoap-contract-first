# Exercise — Publish research software

## 1. Inspect the source metadata

Open `reference/waterbodies.cwl` and identify its `s:` software metadata. Note the release version and research-software identity.

## 2. Generate CodeMeta

From the repository root:

```console
task artifacts:derive
```

## 3. Compare release metadata

- Inspect the generated CodeMeta file under `reference/expected`.
- Compare `softwareVersion` with `CITATION.cff`.
- Explain which release fields need editorial synchronization and how CodeMeta differs from SBOM evidence.

## Verify your work

This task runs `scripts/derive.sh`, regenerating all contract projections, including `reference/expected/publication/codemeta.json`. It replaces generated files. It does not synchronize `CITATION.cff` or publish a release.

Run from the repository root:

```console
task artifacts:derive
```

Success means all generators complete and the CodeMeta file is present. Compare its software identity and version with the CWL and `CITATION.cff` yourself. If a generator fails, read its plugin diagnostics; if metadata differs, identify the source field that needs editorial correction.

**Expected outcome:** A real CodeMeta projection records the research software independently of SBOM evidence.

Compare [the solution](solution.md). Return to [the module](README.md).
