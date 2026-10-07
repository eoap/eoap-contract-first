# Exercise — Implement STAC

Run uv run waterbodies stac --input-item data/fixtures/source --water-body otsu.tif from the repository root after creating the mask there, or substitute absolute paths from your scratch directory. Read catalog/synthetic/synthetic.json and follow its links. Change a projection shape to one element and rerun validation.

From the repository root:

```console
uv run pytest tests/tools/test_processing.py -k "complete or validation"
```

Expected outcome: catalog/catalog.json links to a validated Item and a portable mask asset.

Compare [the solution](solution.md). Return to [the module](README.md).
