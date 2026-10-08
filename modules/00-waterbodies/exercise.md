# Exercise — Understand Water Bodies

## 1. Open the notebook

Open the [guided notebook](waterbodies.ipynb) to explore the spectral bands, predict NDWI, crop the scene and inspect the water mask and its STAC metadata.

From the repository root, install the notebook environment and launch JupyterLab:

```console
uv sync --extra notebook
uv run --extra notebook jupyter lab docs/modules/00-waterbodies/waterbodies.ipynb
```

## 2. Run the guided activity

In JupyterLab, use the Python 3 kernel and run cells in order with **Shift+Enter**. In VS Code, open the same notebook and select the repository `.venv/bin/python` interpreter.

The activity uses local synthetic data and writes results under `.notebook-runs/`.

- Predict before running each stage.
- Compare your predictions with the plots.
- Experiment with the AOI and band order.
- Restart the kernel and run all cells to repeat the activity from scratch.

## 3. Verify and explain your results

The notebook prints the observed NDWI values and water-pixel count, validates the packaged STAC Item, and deliberately demonstrates rejection of unequal grids. For the default AOI and green/NIR order, check for NDWI values of −0.5 and +0.5, 18 water pixels, and the message `STAC validation passed`. The caught grid-validation error in the experiment is expected.

If a cell fails unexpectedly, read its error and confirm that preceding cells ran in order with the repository Python environment. Restart the kernel and rerun with the default parameters to distinguish setup problems from an experiment you changed.

**Expected outcome:** You can explain the observed NDWI values and water-pixel count, inspect the packaged STAC result, and describe how changing the AOI or band order affects classification.

Explain why band order and matching raster grids matter to the workflow contract. Compare [the solution](solution.md) after completing the activity. Return to [the module](README.md).
