# Solution — Implement crop

The canonical solution is `reference/src/waterbodies/crop_impl.py`. Compare your work with this repository artifact, rather than a second independently maintained interface.

crop_green.tif is a 6×6 COG spanning 1,1,7,7.

Verification:

```console
uv run pytest tests/tools/test_processing.py -k crop
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
