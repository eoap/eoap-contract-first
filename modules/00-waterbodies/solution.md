# Solution — Understand Water Bodies

The canonical solution is `reference/waterbodies.cwl`. Compare your work with this repository artifact, rather than a second independently maintained interface.

NDWI is -0.5 on the left, +0.5 on the right; the 6×6 crop contains 18 water pixels.

Verification:

```console
uv run pytest tests/tools/test_processing.py::test_complete_scientific_chain
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
