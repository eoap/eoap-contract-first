# Exercise — Understand Water Bodies

Open the [guided notebook](waterbodies.ipynb) to explore the spectral bands, predict NDWI, crop the scene and inspect the water mask and its STAC metadata.

From the repository root, install the notebook environment and launch JupyterLab:

```console
uv sync --extra notebook
uv run --extra notebook jupyter lab docs/modules/00-waterbodies/waterbodies.ipynb
```

In JupyterLab, use the Python 3 kernel and run cells in order with **Shift+Enter**. In VS Code, open the same notebook and select the repository `.venv/bin/python` interpreter.

The activity uses local synthetic data and writes results into a fresh run directory under `.notebook-runs/`. Predict before running each stage, compare your predictions with the plots, then experiment with the AOI and band order. Restart the kernel and run all cells to repeat the activity from scratch.

**Expected outcome:** You can explain the observed NDWI values and water-pixel count, inspect the packaged STAC result, and describe how changing the AOI or band order affects classification.

Explain why band order and matching raster grids matter to the workflow contract. Compare [the solution](solution.md) after completing the activity. Return to [the module](README.md).
