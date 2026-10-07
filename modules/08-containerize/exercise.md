# Exercise — Containerize

Run task containers:build VERSION=1.0.0 with Docker available. Inspect each image and run docker run --rm ghcr.io/eoap/waterbodies-crop:1.0.0 waterbodies crop --help. Compare a tag with an inspected digest.

From the repository root:

```console
task supply-chain:check
```

Expected outcome: All four declared dependencies have version identities; no canonical image uses latest.

Compare [the solution](solution.md). Return to [the module](README.md).
