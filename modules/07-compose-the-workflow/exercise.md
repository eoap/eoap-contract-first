# Exercise — Compose the workflow

## 1. Trace the graph

Open `reference/waterbodies.cwl`.

- Draw every source-to-input edge in the `Workflow`.
- Identify the scattered crop step and the ordered raster input to normalized difference.

## 2. Run the workflow

From the repository root:

```console
task workflow:run
```

- Find both crop executions in the runner log.
- Check green/NIR order in the normalized-difference invocation.
- Locate the collected STAC `Directory`.

## Verify your work

This task runs `tests/workflow`. The integration test executes the canonical scattered workflow with `cwltool --no-container` in a temporary output directory, validates the resulting STAC Item and checks a 6×6 mask with 18 water pixels.

Run from the repository root:

```console
task workflow:test
```

Success means the workflow test passes. It uses the locally installed tools, so it does not verify Docker execution. A failure may indicate a runner/tool error, invalid STAC metadata or an unexpected raster result; inspect the reported subprocess output or assertion.

**Expected outcome:** The runner executes five tool jobs (two crops) and collects the final STAC `Directory`.

Compare [the solution](solution.md). Return to [the module](README.md).
