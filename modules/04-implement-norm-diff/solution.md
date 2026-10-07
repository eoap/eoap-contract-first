# Solution — Implement normalized difference

The canonical solution is `reference/src/waterbodies/norm_diff_impl.py`. Compare your work with this repository artifact, rather than a second independently maintained interface.

norm_diff.tif contains float32 values -0.5 and +0.5 on the matching grid.

Verification:

```console
uv run pytest tests/tools/test_processing.py -k "norm_diff or complete"
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
