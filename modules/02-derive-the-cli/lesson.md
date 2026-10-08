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

The runtime loads the CWL document, and the plugin generates imports of execute callbacks plus the Click option declarations. Two `baseCommand` tokens create the waterbodies group and its subcommands. Hyphenated ids become snake_case Python callback names without changing public command names. The generated file is `reference/src/waterbodies/waterbodies.py`; `cli.py` only re-exports the group. The resulting `waterbodies` CLI is the application's command-line interface, while `transpiler-mate cwl2click` is the tooling command used to generate it.

`File` and `Directory` options are checked for existence. `File[]` becomes repeated `--rasters` options, one per raster. The generator is a bootstrap projection, not an algorithm implementation. Regenerate whenever the tool interface changes; never maintain a second option list by hand. Generation adds a timestamp and traversal order can vary, so our regression check compares Python syntax rather than timestamps or command order.
## Contract questions

What are we designing? Generate one Click group from all four tool contracts.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
