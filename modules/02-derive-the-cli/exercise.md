# Exercise — Derive the CLI

## 1. Generate the CLI

Run from the repository root:

```console
task cli:generate
```

Inspect the callback imports in `reference/src/waterbodies/waterbodies.py`.

## 2. Explore the command help

Run each help command and compare the options with the CWL inputs:

```console
uv run waterbodies --help
uv run waterbodies crop --help
uv run waterbodies norm-diff --help
uv run waterbodies otsu --help
uv run waterbodies stac --help
```

- Trace `--input-item` through the generated callback to the implementation parameter.
- Identify required options and defaults.

## Verify your work

This task runs pytest over `tests/cli` and `tests/contract`. It checks command help, required options, path checks, the crop callback and the correspondence between the committed generated CLI and the CWL contract.

Run from the repository root:

```console
task cli:test
```

Success means the selected tests pass and the task exits with code `0`. For a failure, read the failing test name and assertion: they distinguish a CLI behavior problem from drift between generated Python and the contract.

**Expected outcome:** Help lists crop, norm-diff, otsu and stac, with options derived from CWL.

Compare [the solution](solution.md). Return to [the module](README.md).
