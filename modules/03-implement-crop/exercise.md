# Exercise — Implement crop

Run the crop command below in a scratch directory after substituting an absolute path to data/fixtures/source. Compare output bounds, transform and pixel size with the original green.tif. Try an AOI outside the fixture.

From the repository root:

```console
uv run pytest tests/tools/test_processing.py -k crop
```

Expected outcome: crop_green.tif is a 6×6 COG spanning 1,1,7,7.

Compare [the solution](solution.md). Return to [the module](README.md).
