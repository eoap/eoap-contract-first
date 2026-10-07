# Solution — Implement Otsu

The canonical solution is `reference/src/waterbodies/otsu_impl.py`. Compare your work with this repository artifact, rather than a second independently maintained interface.

otsu.tif is uint8, contains only 0/1 and marks nonfinite pixels as non-water.

Verification:

```console
uv run pytest tests/tools/test_processing.py -k otsu
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
