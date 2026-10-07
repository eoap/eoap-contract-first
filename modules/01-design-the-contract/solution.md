# Solution — Design the contract

The canonical solution is `reference/waterbodies.cwl`. Compare your work with this repository artifact, rather than a second independently maintained interface.

The canonical graph validates, with one Workflow and four CommandLineTools.

Verification:

```console
task contract:validate
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
