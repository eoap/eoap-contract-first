# Exercise — Understand Water Bodies

Open `scripts/fixtures.py`. Identify the green/nir values for each half of the image. Predict NDWI and the number of water pixels after cropping to 1,1,7,7.

From the repository root:

```console
uv run pytest tests/tools/test_processing.py::test_complete_scientific_chain
```

Expected outcome: NDWI is -0.5 on the left, +0.5 on the right; the 6×6 crop contains 18 water pixels.

Compare [the solution](solution.md). Return to [the module](README.md).
