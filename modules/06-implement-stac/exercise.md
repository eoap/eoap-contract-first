# Exercise — Implement STAC

## 1. Prepare the mask

Complete the [Otsu exercise](../05-implement-otsu/exercise.md). Keep `otsu.tif` and the staged source catalog available in the repository root.

## 2. Package and inspect

```console
uv run waterbodies stac --input-item data/fixtures/source --water-body otsu.tif
```

- Read `catalog/synthetic/synthetic.json` and follow its links.
- Locate the mask asset and confirm its relative path resolves.
- Compare source identity and acquisition time with the result.

## 3. Check validation

Read `test_validation_rejects_invalid_projection` in `tests/tools/test_processing.py`. It changes the projection shape to one element through the PySTAC extension API and checks that validation rejects it.

## Verify your work

The `-k "complete or validation"` filter selects the complete scientific-chain test and the invalid-projection validation test. They check that the packaged Item validates, preserves source identity and time, describes the cropped product and resolves its mask asset; malformed projection metadata must be rejected.

Run from the repository root:

```console
uv run pytest tests/tools/test_processing.py -k "complete or validation"
```

Success means both tests pass. They use their own output catalogs; inspect your catalog separately in step 2. If a test fails, distinguish the STAC validation error from an assertion about metadata or asset paths.

**Expected outcome:** catalog/catalog.json links to a validated Item and a portable mask asset.

Compare [the solution](solution.md). Return to [the module](README.md).
