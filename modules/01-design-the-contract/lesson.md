# Design the contract

The public processing API belongs in CWL. A CommandLineTool declares its id, `baseCommand`, input types, bindings and file outputs. Directory means a staged catalog with local assets; File means a runner-managed raster. Strings describe the AOI, CRS and band common name. Required inputs and defaults determine whether clients may omit a value.

Read the four tools in `reference/waterbodies.cwl` without looking at Python. The crop contract tells you precisely what implementation must accept and which file it must produce. An output glob is part of the API: naming a file differently breaks collection even if the algorithm succeeds. Contract design is top-down; testing the implementation and workflow proceeds bottom-up. Contract and implementation are distinct artifacts.

## Contract questions

What are we designing? Design typed tool inputs and outputs before writing processing code.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
