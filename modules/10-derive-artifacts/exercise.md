# Exercise — Derive artifacts

## 1. Generate the projections

From the repository root:

```console
task artifacts:derive
```

## 2. Compare templates and runnable inputs

- Compare `reference/expected/inputs.yaml` with `reference/inputs.yaml`.
- Identify data locations that must be supplied before a template is runnable.

## 3. Inspect metadata

- Inspect the OGC process description and OCI `$manifest` wrapper.
- Locate the PlantUML, Markdown and CodeMeta outputs.
- Trace an input from the canonical CWL to its generated representations.

## Verify your work

This task runs `scripts/derive.sh` to regenerate Markdown, PlantUML source, an input template, OGC JSON, OCI annotations and CodeMeta under `reference/expected`. It replaces generated files; it does not compare them with a baseline or execute the scientific workflow.

Run from the repository root:

```console
task artifacts:derive
```

Success means each generator finishes with exit code `0` and the expected files are present. Inspect the generated content and your Git diff to assess changes. If generation fails, use the named plugin and its diagnostics to identify which projection could not be produced.

**Expected outcome:** Actual PlantUML, Markdown, input YAML, OGC JSON, CodeMeta and OCI metadata are emitted.

Compare [the solution](solution.md). Return to [the module](README.md).
