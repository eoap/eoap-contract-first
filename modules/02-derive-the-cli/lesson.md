# Derive the CLI

## From a terminal command to a Python function

A command-line interface (CLI) lets you run an application from a terminal. In this course, `waterbodies` is the application command, `crop` selects an operation, and options such as `--band` supply named inputs.

[Click](https://click.palletsprojects.com/en/stable/) is a Python library for building these interfaces. It reads command-line inputs, checks declared parameter types, provides `--help`, and calls the Python function that performs the operation. You do not need prior Click experience for this module.

Start by exploring the interface without processing any data:

```console
uv run waterbodies --help
uv run waterbodies crop --help
```

The first command lists available operations; the second lists the inputs accepted by `crop`. Three Click concepts explain how this works:

| Concept | Meaning in this application |
| --- | --- |
| **Group** | The top-level `waterbodies` command, which collects related operations. |
| **Command** | An operation such as `crop`, `norm-diff`, `otsu` or `stac`. |
| **Callback** | The Python function Click calls after reading and checking the operation's inputs. Here, each tool supplies an `execute` function. |

An option connects a terminal spelling to a Python parameter: `--band green` supplies `band="green"` to the crop callback. Click handles the interface; the callback performs the raster processing. Checking that a path exists does not check scientific requirements such as matching raster grids; those remain the implementation's responsibility.

## Generate the interface from CWL

**cwl2click is a Transpiler-Mate plugin.** Install it alongside `transpiler-mate-runtime` in the same tooling environment; the runtime discovers the plugin and exposes it through `transpiler-mate cwl2click`. The plugin generates a Python Click command-line interface from the CWL tool contracts.

From the repository root, `task cli:generate` runs:

```console
uv run transpiler-mate cwl2click --bundle --output reference/src/waterbodies reference/waterbodies.cwl
```

The runtime loads the CWL document, and the plugin generates imports of execute callbacks plus the Click options. Two `baseCommand` tokens create the waterbodies group and its subcommands. Hyphenated ids become snake_case Python callback names without changing public command names. The generated file is `reference/src/waterbodies/waterbodies.py`; `cli.py` only re-exports the group. The resulting `waterbodies` CLI is the application's command-line interface, while `transpiler-mate cwl2click` is the tooling command used to generate it.

`File` and `Directory` options are checked for existence. `File[]` becomes repeated `--rasters` options.

## Define the interface once

**Change the CWL contract and regenerate the CLI. Do not maintain the same interface manually in both places, and do not edit the generated file.** The contract is the source of truth; the generated CLI is a projection of it.

Maintaining CWL inputs and Python Click options separately creates two descriptions of the same public interface. Every change then depends on someone remembering to update both. A renamed option, a different default or a missing required parameter can leave a tool that works when invoked directly but fails when the CWL runner calls it. Even small differences force users and reviewers to determine which description is correct.

For example, the normalized-difference tool accepts two raster files through repeated `--rasters` options. The CWL input bindings describe that calling convention, and cwl2click generates the corresponding CLI option. Hand-editing the CLI to accept a different flag would break the connection to the workflow. Changing the contract and regenerating keeps that connection explicit and reviewable.

## Why generate the CLI?

| Benefit | What it means for this application |
| --- | --- |
| **Prevent interface drift** | Commands and options are derived from the definitions the CWL runner uses, reducing discrepancies between direct CLI use and workflow execution. |
| **Reduce repetitive maintenance** | A supported interface change is described in CWL and propagated by regeneration, without separately rewriting Click declarations for each tool. |
| **Apply consistent conventions** | The same generator maps inputs across all four tools, including path-existence checks for `File` and `Directory` and repeated options for `File[]`. |
| **Keep help aligned with the interface** | Click exposes the generated commands and options through `--help`, making the installed interface inspectable alongside the contract. |
| **Focus implementation on science** | Developers implement crop, normalized difference, classification and STAC packaging in callbacks while generation handles the CLI declarations. |
| **Make changes easier to review** | Reviewers start with the intentional contract change, then inspect its generated consequences and the corresponding implementation changes. Handwritten interface decisions stay in one place. |
| **Detect stale artifacts automatically** | Regeneration checks can reveal when the committed CLI no longer matches the contract, turning a manual synchronization task into a verifiable build step. |
| **Support repeatable builds and upgrades** | With recorded generator and plugin versions, the interface can be regenerated and compared when rebuilding a release or evaluating a tooling upgrade. |
| **Reuse the same contract elsewhere** | Documentation, diagrams and service descriptions can be derived from the same CWL, so the CLI participates in a shared description of the application. |

## Evolve and verify the generated interface

Treat CLI generation as part of maintaining the application:

1. Edit the authoritative tool definitions in `reference/waterbodies.cwl`.
2. Run `task cli:generate` to update the generated interface.
3. Update the implementation callbacks and tests where the contract change requires new behavior or arguments.
4. Run `task cli:test`, inspect the affected commands with `--help`, and verify the affected workflow behavior.

Keep custom processing logic in the implementation modules. A manual change to the generated file will be overwritten by regeneration and cannot be reproduced from the contract. If generation does not express a needed interface correctly, investigate the contract or generator support rather than maintaining a local edit to its output.

Generation does not establish scientific correctness or complete input validation. Matching raster grids, band ordering and NDWI threshold behavior still require implementation checks and meaningful tests. A breaking contract change also still needs compatibility review and appropriate versioning.

The regression check compares freshly generated Python syntax with the committed CLI. Generation adds a timestamp and traversal order can vary, so the comparison ignores timestamps and command order. This checks structural agreement without requiring byte-for-byte identical output.

## Contract questions

What are we designing? Generate one Click group from all four tool contracts.

Why does it belong in the contract? The runner and generated CLI must share one definition of commands and inputs, avoiding two manually synchronized interfaces.

What can be derived? CLI commands, options and their supported input checks, alongside documentation and other projections of the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md), compare the CLI with fresh generation, inspect help and test the observable behavior of the implementations and workflow.

[Module overview](README.md)
