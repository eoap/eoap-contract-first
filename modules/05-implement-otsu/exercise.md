# Exercise — Implement Otsu

## 1. Prepare the NDWI raster

Complete the [normalized-difference exercise](../04-implement-norm-diff/exercise.md) with green/NIR order. Run the following commands from the repository root.

## 2. Classify and inspect

```console
uv run waterbodies otsu --raster norm_diff.tif
```

- Inspect the dtype and nodata setting of `otsu.tif`.
- Count each class and compare with the expected water population.
- Explain the strict greater-than threshold rule.

## 3. Explore invalid pixels

Read `test_otsu_nonfinite_pixels_are_non_water` in `tests/tools/test_processing.py`. Explain why NaN and infinity must be excluded from threshold estimation.

## Verify your work

The `-k otsu` filter selects tests for nonfinite NDWI handling: NaN and infinity become non-water, and a raster with no finite values is rejected.

Run from the repository root:

```console
uv run pytest tests/tools/test_processing.py -k otsu
```

Success means both cases pass. These tests do not inspect your manually generated mask; check its dtype, nodata and class counts in step 2. A failure identifies which invalid-pixel behavior differs from the contract.

**Expected outcome:** otsu.tif is uint8, contains only 0/1 and marks nonfinite pixels as non-water.

Compare [the solution](solution.md). Return to [the module](README.md).
