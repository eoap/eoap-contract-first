# Implement STAC

PySTAC owns creation, parsing, links, assets and serialization. The output keeps the input Item id and observation datetime. Its WGS84 bbox and polygon describe the cropped raster footprint. ProjectionExtension registers grid shape, transform and EPSG code; RasterExtension registers the unsigned-byte data band. The data asset has data and visual roles and the COG media type.

The catalog is self-contained: its Item links and mask asset href resolve after moving the result directory. Item ids are checked before using them as directory names. Validation checks core STAC and every declared extension. Official EO, projection and raster schemas are bundled without modification, so local CI validates offline; declared extensions are never removed to pass a check.

## Contract questions

What are we designing? Publish the water mask as validated machine-readable product metadata.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
