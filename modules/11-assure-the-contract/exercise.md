# Exercise — Evolve and assure the contract

## 1. Compare the versions

From the repository root, create the report output directory:

```console
mkdir -p build
uv run transpiler-mate baseline modules/11-assure-the-contract/v2/waterbodies.cwl --previous modules/11-assure-the-contract/v1/waterbodies.cwl --output build/baseline.json
```

Inspect the report and identify `input.omission_removed`.

## 2. Observe the unresolved review

This command is expected to fail until the compatibility change has been reviewed:

```console
uv run transpiler-mate baseline modules/11-assure-the-contract/v2/waterbodies.cwl --previous modules/11-assure-the-contract/v1/waterbodies.cwl --output build/baseline.json --check
```

Explain why removing a default affects existing callers.

## 3. Record the known review

The verification task below records the explicit major-change review for this example.

## Verify your work

This task compares the module 11 v1 and v2 contracts with the baseline plugin, records `--review-bump major` and applies `--check`. It writes the reviewed report to `reference/expected/baseline/report.json`, replacing that generated file.

Run from the repository root:

```console
task baseline:check
```

Success means the compatibility gate accepts the explicit major-change review. Inspect the report for the change and version requirement; if the gate fails, read the unresolved review or compatibility diagnostics rather than removing the check.

**Expected outcome:** The actual report requires at least 2.0.0 and records the explicit review decision.

Compare [the solution](solution.md). Return to [the module](README.md).
