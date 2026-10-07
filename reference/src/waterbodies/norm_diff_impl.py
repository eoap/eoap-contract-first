"""Compute NDWI from green and near-infrared rasters on matching grids."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import rasterio

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

NDWI_BAND_COUNT = 2


def execute(*, rasters: Sequence[Path]) -> None:
    """Write float32 NDWI to ``norm_diff.tif``.

    Args:
        rasters: Exactly two files in green, near-infrared order.

    Raises:
        ValueError: If the number of rasters or their grids do not match.
    """
    if len(rasters) != NDWI_BAND_COUNT:
        raise ValueError("Exactly two rasters are required in green, nir order")
    with rasterio.open(rasters[0]) as green, rasterio.open(rasters[1]) as nir:
        if (green.shape, green.transform, green.crs) != (nir.shape, nir.transform, nir.crs):
            raise ValueError("Raster dimensions, transform and CRS must match")
        green_pixels = green.read(1).astype(np.float32)
        nir_pixels = nir.read(1).astype(np.float32)
        metadata = green.meta.copy()
    with np.errstate(divide="ignore", invalid="ignore"):
        ndwi = (green_pixels - nir_pixels) / (green_pixels + nir_pixels)
    metadata.update(driver="COG", dtype="float32", count=1, compress="LZW", blocksize=256)
    with rasterio.open("norm_diff.tif", "w", **metadata) as output:
        output.write(ndwi, 1)
