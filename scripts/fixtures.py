"""Generate compact, georeferenced synthetic spectral data using PySTAC."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pystac
import rasterio
from pystac.extensions.eo import Band, EOExtension
from rasterio.transform import from_origin
from waterbodies.validation import validate_item


def create_fixture(directory: Path) -> None:
    """Write an 8 by 8 staged catalog with separable land and water pixels."""
    directory.mkdir(parents=True, exist_ok=True)
    catalog = pystac.Catalog(id="source", description="Synthetic Water Bodies fixture")
    item = pystac.Item(
        id="synthetic",
        geometry={"type": "Polygon", "coordinates": [[[0, 0], [8, 0], [8, 8], [0, 8], [0, 0]]]},
        bbox=[0, 0, 8, 8],
        datetime=datetime(2024, 1, 1, tzinfo=UTC),
        properties={},
    )
    catalog.add_item(item)
    for name, left, right in [("green", 100, 300), ("nir", 300, 100)]:
        pixels = np.full((8, 8), left, dtype=np.uint16)
        pixels[:, 4:] = right
        path = directory / f"{name}.tif"
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=8,
            width=8,
            count=1,
            dtype="uint16",
            crs="EPSG:4326",
            transform=from_origin(0, 8, 1, 1),
        ) as output:
            output.write(pixels, 1)
        asset = pystac.Asset(
            href=str(path.resolve()), media_type=pystac.MediaType.GEOTIFF, roles=["data"]
        )
        item.add_asset(name, asset)
        EOExtension.ext(asset, add_if_missing=True).bands = [
            Band.create(name=name, common_name=name)
        ]
    catalog.normalize_hrefs(str(directory.resolve()))
    catalog.make_all_asset_hrefs_relative()
    validate_item(item)
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)


if __name__ == "__main__":
    create_fixture(Path("data/fixtures/source"))
