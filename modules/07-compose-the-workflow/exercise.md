# Exercise — Compose the workflow

Draw every source-to-input edge in reference/waterbodies.cwl. Run task workflow:run. Find both crop executions in the runner log and check their order in the normalized difference invocation.

From the repository root:

```console
task workflow:test
```

Expected outcome: The runner executes five tool jobs (two crops) and collects the final STAC Directory.

Compare [the solution](solution.md). Return to [the module](README.md).
