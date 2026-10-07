# Exercise — Evolve and assure the contract

Run uv run transpiler-mate baseline modules/11-assure-the-contract/v2/waterbodies.cwl --previous modules/11-assure-the-contract/v1/waterbodies.cwl --output build/baseline.json. Identify input.omission_removed. Add --check and observe the unresolved review failure. Complete the known major review with task baseline:check.

From the repository root:

```console
task baseline:check
```

Expected outcome: The actual report requires at least 2.0.0 and records the explicit review decision.

Compare [the solution](solution.md). Return to [the module](README.md).
