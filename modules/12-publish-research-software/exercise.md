# Exercise — Publish research software

Inspect `s: metadata` in the canonical CWL and the generated CodeMeta file. Run

```console
task artifacts:derive
```

Compare `softwareVersion` with `CITATION.cff` and explain which release fields require editorial synchronization.

From the repository root:

```console
task artifacts:derive
```

Expected outcome: A real CodeMeta projection records the research software independently of SBOM evidence.

Compare [the solution](solution.md). Return to [the module](README.md).
