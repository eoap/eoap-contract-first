# Run the application

The fixture is synthetic but georeferenced: 8×8 uint16 green and nir bands, one source Item and a portable catalog. It has controlled spectral populations so expected NDWI and classification are independently predictable. No large remote scene is required for CI.

Run each command in a scratch directory, then execute the complete Workflow. The runner stages input Directories and Files and collects only the contract outputs. Tests verify COG layout, 6×6 grid, NDWI values, binary classification, datetime, footprint, extension metadata and asset portability. Real scenes remain a separate scientific validation exercise; passing compact tests does not establish global classification accuracy.

## Contract questions

What are we designing? Verify tool outputs and end-to-end execution on compact data.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
