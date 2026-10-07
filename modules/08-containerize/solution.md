# Solution — Containerize

The canonical solution is `reference/waterbodies.cwl`. Compare your work with this repository artifact, rather than a second independently maintained interface.

All four declared dependencies have version identities; no canonical image uses latest.

Verification:

```console
task supply-chain:check
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
