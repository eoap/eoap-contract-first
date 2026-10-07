# Solution — Secure, promote and deploy

The canonical solution is `reference/waterbodies.cwl`. Compare your work with this repository artifact, rather than a second independently maintained interface.

Local package inspection succeeds. A configured ZOO environment can execute the promoted package; deployment requires an accessible staged input and server credentials.

Verification:

```console
task supply-chain:check
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
