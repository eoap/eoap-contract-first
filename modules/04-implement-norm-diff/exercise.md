# Exercise — Implement normalized difference

## 1. Create matching crops

Run from the repository root:

```console
task fixtures:generate
uv run waterbodies crop --input-item data/fixtures/source --aoi "1,1,7,7" --epsg EPSG:4326 --band green
uv run waterbodies crop --input-item data/fixtures/source --aoi "1,1,7,7" --epsg EPSG:4326 --band nir
```

## 2. Calculate and inspect NDWI

```console
uv run waterbodies norm-diff --rasters crop_green.tif --rasters crop_nir.tif
```

- Inspect `norm_diff.tif` and compare its values with your prediction.
- Check that its grid matches both crops.

## 3. Reverse the band order

This overwrites `norm_diff.tif`; record the original values first.

```console
uv run waterbodies norm-diff --rasters crop_nir.tif --rasters crop_green.tif
```

Explain the sign change. Restore green/NIR order before continuing to the next module.

## Verify your work

The `-k "norm_diff or complete"` filter selects normalized-difference input checks and the complete scientific chain. These verify that invalid raster counts and mismatched grids are rejected, and that the default ordered bands produce the expected NDWI and mask.

Run from the repository root:

```console
uv run pytest tests/tools/test_processing.py -k "norm_diff or complete"
```

Success means the selected tests pass. They use separate fixture outputs, so also inspect your own raster from step 2. If a test fails, use its name and assertion to determine whether the problem is input validation, grid compatibility or the calculated values.

**Expected outcome:** norm_diff.tif contains float32 values -0.5 and +0.5 on the matching grid.

Compare [the solution](solution.md). Return to [the module](README.md).
