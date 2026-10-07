# Exercise — Derive the CLI

Run task cli:generate. Inspect the generated imports, then run waterbodies --help and all four subcommand help commands using uv run. Trace --input-item to the callback argument input_item.

From the repository root:

```console
task cli:test
```

Expected outcome: Help lists crop, norm-diff, otsu and stac, with options derived from CWL.

Compare [the solution](solution.md). Return to [the module](README.md).
