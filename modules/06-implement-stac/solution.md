# Solution — Implement STAC

The canonical solution is `reference/src/waterbodies/stac_impl.py`. Compare your work with this repository artifact, rather than a second independently maintained interface.

catalog/catalog.json links to a validated Item and a portable mask asset.

Verification:

```console
uv run pytest tests/tools/test_processing.py -k "complete or validation"
```

Explain how the result follows from the contract and compare any failure with the tool tests under `tests/`.

[Return to the exercise](exercise.md)
