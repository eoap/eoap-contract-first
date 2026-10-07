# Exercise — Design the contract

Copy the crop tool into a scratch CWL document with cwlVersion v1.2. Design its typed inputs and crop output before opening crop_impl.py. Validate your scratch tool with cwltool --validate. Compare it with the canonical crop contract.

From the repository root:

```console
task contract:validate
```

Expected outcome: The canonical graph validates, with one Workflow and four CommandLineTools.

Compare [the solution](solution.md). Return to [the module](README.md).
