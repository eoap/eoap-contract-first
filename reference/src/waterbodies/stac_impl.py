"""Package the classified raster with spatial, temporal and raster STAC metadata."""

from __future__ import annotations

import shutil
from pathlib import Path

import pystac
import rasterio
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import DataType, RasterBand, RasterExtension
from rasterio.warp import transform_bounds

from .common import read_item
from .validation import validate_item


def execute(*, input_item: Path, water_body: Path) -> None:
    """Write and validate a self-contained STAC catalog under ``catalog/``.

    Preserve the source Item identity and datetime. Derive the footprint from
    the mask grid and register projection and raster metadata via PySTAC.

    Raises:
        ValueError: If the Item id is unsafe or the raster has no EPSG CRS.
        pystac.errors.STACValidationError: If the output fails STAC validation.
    """
    source_item = read_item(input_item)
    if Path(source_item.id).name != source_item.id or source_item.id in {"", ".", ".."}:
        raise ValueError("STAC Item id must be a single directory name")
    directory = Path("catalog") / source_item.id
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / "otsu.tif"
    shutil.copyfile(water_body, destination)
    with rasterio.open(destination) as raster:
        if raster.crs is None or raster.crs.to_epsg() is None:
            raise ValueError("Water mask must declare an EPSG CRS")
        bounds = list(transform_bounds(raster.crs, "EPSG:4326", *raster.bounds))
        west, south, east, north = bounds
        geometry = {
            "type": "Polygon",
            "coordinates": [
                [[west, south], [east, south], [east, north], [west, north], [west, south]]
            ],
        }
        result = pystac.Item(
            id=source_item.id,
            geometry=geometry,
            bbox=bounds,
            datetime=source_item.datetime,
            properties={},
        )
        projection = ProjectionExtension.ext(result, add_if_missing=True)
        projection.apply(
            epsg=raster.crs.to_epsg(),
            shape=[raster.height, raster.width],
            transform=list(raster.transform)[:6],
        )
    asset = pystac.Asset(
        href="otsu.tif",
        media_type=pystac.MediaType.COG,
        roles=["data", "visual"],
        title="Binary water mask (0 non-water, 1 water)",
    )
    result.add_asset("data", asset)
    RasterExtension.ext(asset, add_if_missing=True).bands = [
        RasterBand.create(data_type=DataType.UINT8)
    ]
    catalog = pystac.Catalog(id="catalog", description="water-bodies")
    catalog.add_item(result)
    catalog.normalize_hrefs(str(Path("catalog").resolve()))
    validate_item(result)
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
