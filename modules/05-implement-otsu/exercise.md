# Exercise — Implement Otsu

Run

```console
uv run waterbodies otsu --raster norm_diff.tif
```

Inspect `dtype`, `nodata` and the class histogram. Read the test using NaN and infinity and explain why a finite mask is necessary.

From the repository root:

```console
uv run pytest tests/tools/test_processing.py -k otsu
```

Expected outcome: `otsu.tif` is `uint8`, contains only 0/1 and marks nonfinite pixels as non-water.

Compare [the solution](solution.md). Return to [the module](README.md).
