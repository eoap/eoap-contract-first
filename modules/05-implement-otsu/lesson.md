# Implement Otsu

Otsu minimizes within-class variance over the finite raster population. The Water Bodies convention is `value > threshold`, with equality classified as non-water. The implementation emits uint8 values 0 and 1, with no nodata value that could make valid non-water pixels disappear in consumers.

Nonfinite values are excluded from threshold estimation and always classified as non-water. A raster with no finite pixels fails. This is the enhancements branch behavior and improves the original code, where positive infinity could pass a comparison against a finite threshold. Homogeneous scenes may produce an all-zero mask; interpreting those outputs is a scientific responsibility.

## Contract questions

What are we designing? Classify finite NDWI and define invalid-pixel behavior.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
