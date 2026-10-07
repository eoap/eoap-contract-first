# Exercise — Run the application

Run task reference:test and task workflow:run. Inspect build/result/catalog. Use rasterio to count nonzero pixels and verify the expected 18. Move the catalog to a different directory and confirm its local asset links resolve.

From the repository root:

```console
task workflow:test
```

Expected outcome: A complete local execution produces a validated self-contained Water Bodies catalog.

Compare [the solution](solution.md). Return to [the module](README.md).
