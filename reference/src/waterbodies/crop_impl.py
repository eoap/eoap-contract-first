"""Crop the source band's COG using an AOI expressed in a declared CRS."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import rasterio
from pystac.extensions.eo import EOExtension
from rasterio.mask import mask
from rasterio.warp import transform_geom
from shapely.geometry import box, mapping, shape

from .common import read_item

if TYPE_CHECKING:
    from pathlib import Path

    import pystac

BBOX_COORDINATE_COUNT = 4


def _asset_href(item: pystac.Item, band: str) -> str:
    for asset in item.get_assets().values():
        if "data" not in (asset.roles or []):
            continue
        bands = EOExtension.ext(asset).bands or []
        if any(candidate.common_name == band for candidate in bands):
            href = asset.get_absolute_href()
            if href is not None:
                return href
    raise ValueError(f"Common band name {band} not found in data assets")


def execute(*, input_item: Path, aoi: str, epsg: str, band: str) -> None:
    """Write ``crop_<band>.tif`` in the working directory.

    Args:
        input_item: Staged self-contained catalog and assets.
        aoi: Bounding box or GeoJSON polygon in the supplied CRS.
        epsg: AOI CRS as an EPSG identifier or numeric code.
        band: EO common name (green, nir or nir08).

    Raises:
        ValueError: If the band, AOI, asset or raster CRS is invalid.
    """
    if band not in {"green", "nir", "nir08"}:
        raise ValueError("Band must be green, nir or nir08")
    if aoi.lstrip().startswith("{"):
        geometry = shape(json.loads(aoi))
    else:
        bounds = [float(coordinate) for coordinate in aoi.split(",")]
        if len(bounds) != BBOX_COORDINATE_COUNT or bounds[0] >= bounds[2] or bounds[1] >= bounds[3]:
            raise ValueError("AOI requires xmin,ymin,xmax,ymax with increasing bounds")
        geometry = box(*bounds)
    if geometry.geom_type not in {"Polygon", "MultiPolygon"} or not geometry.is_valid:
        raise ValueError("AOI must be a valid polygon")
    href = _asset_href(read_item(input_item), band)
    with rasterio.open(href) as source:
        if source.crs is None:
            raise ValueError("Raster must declare its CRS")
        crs = f"EPSG:{epsg}" if epsg.isdigit() else epsg
        projected = transform_geom(crs, source.crs, mapping(geometry))
        pixels, transform = mask(source, [projected], crop=True)
        metadata = source.meta.copy()
        metadata.update(
            driver="COG",
            height=pixels.shape[1],
            width=pixels.shape[2],
            transform=transform,
            compress="LZW",
            blocksize=256,
        )
        with rasterio.open(f"crop_{band}.tif", "w", **metadata) as output:
            output.write(pixels)
