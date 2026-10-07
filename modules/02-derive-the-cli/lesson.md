# Derive the CLI

`cwl2click --bundle` reads the contracts and generates imports of execute callbacks plus the Click options. Two baseCommand tokens create the waterbodies group and its subcommands. Hyphenated ids become snake_case Python callback names without changing public command names. The generated file is `reference/src/waterbodies/waterbodies.py`; cli.py only re-exports the group.

File and Directory options are checked for existence. File[] becomes repeated --rasters options. The generator is a bootstrap projection, not an algorithm implementation. Regenerate whenever the tool interface changes; never maintain a second option list by hand. Generation adds a timestamp and traversal order can vary, so our regression check compares Python syntax rather than timestamps or command order.

## Contract questions

What are we designing? Generate one Click group from all four tool contracts.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
