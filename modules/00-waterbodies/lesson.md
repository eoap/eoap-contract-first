# Understand Water Bodies

Water tends to reflect more green than near-infrared radiation. NDWI is `(green - nir) / (green + nir)`. The sign and magnitude separate our synthetic water and land populations. Otsu selects a threshold from the finite NDWI population, and pixels strictly greater than it become water. This is scene-dependent classification, not a universal guarantee of hydrological accuracy. Clouds, shadows, mixed pixels and atmospheric corrections affect real results.

The processing graph is two crop operations, one normalized difference, one Otsu classification and one STAC packaging operation. Both crops use the same AOI and retain the source raster grid. The ordered bands matter: reversing green and nir negates NDWI and changes the classification. STAC makes the output discoverable through spatial, temporal and asset metadata.

## Contract questions

What are we designing? Recognize the spectral and metadata processing graph.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
