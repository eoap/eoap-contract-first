# Implement normalized difference

The algorithm is the upstream `(first - second) / (first + second)` using float32. Exactly two rasters are required by the scientific implementation, since CWL arrays alone do not impose cardinality. Shape, transform and CRS must match. Division by zero retains nonfinite numerical results for the downstream finite-pixel policy.

CWL binds each array item with --rasters. The outer inputBinding is empty, so cwltool emits no extra prefix. cwl2click falls back to the input id for the generated repeated option. Setting --rasters on both the array and its items emits a stray prefix and fails execution: the end-to-end runner test guards that interoperability edge case.

## Contract questions

What are we designing? Implement ordered File[] inputs and validate raster grids.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
