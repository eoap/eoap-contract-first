# Exercise — Run the application

## 1. Verify and run

From the repository root:

```console
task reference:test
task workflow:run
```

## 2. Inspect the result

- Locate the catalog in `build/result/catalog`.
- Open its mask with Rasterio and count nonzero pixels; expect 18 for the default fixture.
- Read the catalog through PySTAC and validate the Item and declared extensions.

## 3. Check portability

Copy the complete result catalog to another directory. Use PySTAC to resolve the asset href and confirm that the local raster is readable without referring to the original result directory.

## Verify your work

This task runs the workflow integration test with `cwltool --no-container`, using its own temporary output directory. It checks the output `Directory`, validates the STAC Item and confirms a 6×6 raster with 18 water pixels.

Run from the repository root:

```console
task workflow:test
```

Success means the test passes. It does not inspect `build/result/catalog` or the relocated copy from your activity; verify those separately in steps 2–3. If it fails, inspect the runner diagnostics, STAC validation message or raster assertion.

**Expected outcome:** A complete local execution produces a validated self-contained Water Bodies catalog.

Compare [the solution](solution.md). Return to [the module](README.md).
