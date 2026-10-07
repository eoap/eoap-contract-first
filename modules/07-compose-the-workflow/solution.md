# Solution — Compose the workflow

The canonical solution is `reference/waterbodies.cwl`. Compare your work with this repository artifact, rather than a second independently maintained interface.

The runner executes five tool jobs (two crops) and collects the final STAC Directory.

Verification:

```console
task workflow:test
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
