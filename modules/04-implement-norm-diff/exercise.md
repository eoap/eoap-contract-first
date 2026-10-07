# Exercise — Implement normalized difference

Run crop for both green and nir. Call uv run waterbodies norm-diff --rasters crop_green.tif --rasters crop_nir.tif. Reverse the order and compare NDWI. Explain why the output changes.

From the repository root:

```console
uv run pytest tests/tools/test_processing.py -k "norm_diff or complete"
```

Expected outcome: norm_diff.tif contains float32 values -0.5 and +0.5 on the matching grid.

Compare [the solution](solution.md). Return to [the module](README.md).
