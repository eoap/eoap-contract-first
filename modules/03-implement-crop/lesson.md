# Implement crop

The generated callback passes a Path for input_item and strings for AOI, CRS and band. Crop reads the first recursive STAC Item using PySTAC, selects a data asset through the EO extension common_name, resolves its relative href, transforms the AOI into the raster CRS and calls rasterio.mask. A bbox or GeoJSON Polygon/MultiPolygon is supported. Numeric EPSG codes are normalized.

The output is an LZW-compressed COG with the cropped transform and original pixel dtype. Missing bands, malformed AOIs and disjoint regions fail visibly. This reference uses staged accessible assets: automatic Planetary Computer URL signing from the enhancements branch is deliberately outside the staged Directory contract. Download or sign assets at a separate staging boundary when using authenticated remote imagery.

## Contract questions

What are we designing? Select an EO common band and crop it in its raster CRS.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
