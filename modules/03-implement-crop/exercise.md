# Exercise — Implement crop

## 1. Prepare local data

Run these commands from the repository root. Outputs are written there; rerunning processing commands replaces their output files.

```console
task fixtures:generate
```

## 2. Crop and inspect

```console
uv run waterbodies crop --input-item data/fixtures/source --aoi "1,1,7,7" --epsg EPSG:4326 --band green
```

- Compare bounds, transform and pixel size with `data/fixtures/source/green.tif`.
- Confirm the output is a 6×6 COG.

## 3. Try a disjoint AOI

Predict the failure before running:

```console
uv run waterbodies crop --input-item data/fixtures/source --aoi "100,100,101,101" --epsg EPSG:4326 --band green
```

Explain why rejecting the request is preferable to returning an unrelated raster.

## Verify your work

Run the crop-related tests in `tests/tools/test_processing.py`. The `-k crop` filter selects tests for invalid or disjoint AOIs, missing bands and coordinate transformation.

Run from the repository root:

```console
uv run pytest tests/tools/test_processing.py -k crop
```

Success means the selected tests pass. The tests create their own data and do not inspect your manually generated `crop_green.tif`; check its dimensions and bounds in step 2. If a test fails, compare the reported AOI or band case with the expected behavior.

**Expected outcome:** crop_green.tif is a 6×6 COG spanning 1,1,7,7.

Compare [the solution](solution.md). Return to [the module](README.md).
