"""Classify finite NDWI pixels with the upstream Otsu water threshold."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt
import rasterio
from skimage.filters import threshold_otsu

if TYPE_CHECKING:
    from pathlib import Path


def threshold(pixels: npt.NDArray[np.float32]) -> npt.NDArray[np.uint8]:
    """Return a binary mask; nonfinite pixels are non-water.

    Raises:
        ValueError: If no finite pixels are available for thresholding.
    """
    finite = np.isfinite(pixels)
    if not finite.any():
        raise ValueError("Raster has no finite values for Otsu thresholding")
    cutoff = float(threshold_otsu(pixels[finite]))
    return np.asarray(finite & (pixels > cutoff), dtype=np.uint8)


def execute(*, raster: Path) -> None:
    """Write the uint8 water mask to ``otsu.tif`` in the working directory."""
    with rasterio.open(raster) as source:
        pixels = source.read(1).astype(np.float32)
        metadata = source.meta.copy()
    water_mask = threshold(pixels)
    metadata.update(
        driver="COG",
        dtype="uint8",
        count=1,
        nodata=None,
        compress="LZW",
        blocksize=256,
    )
    with rasterio.open("otsu.tif", "w", **metadata) as output:
        output.write(water_mask, 1)
