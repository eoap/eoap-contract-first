from pathlib import Path

import numpy as np
import pytest
import rasterio
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from waterbodies import crop_impl, norm_diff_impl, otsu_impl, stac_impl
from waterbodies.common import read_item
from waterbodies.validation import validate_item

WGS84_EPSG = 4326


def test_complete_scientific_chain(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source_catalog: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    for band in ("green", "nir"):
        crop_impl.execute(input_item=source_catalog, aoi="1,1,7,7", epsg="4326", band=band)
    with rasterio.open("crop_green.tif") as cropped:
        assert cropped.shape == (6, 6)
        assert cropped.crs.to_epsg() == WGS84_EPSG
        assert cropped.tags(ns="IMAGE_STRUCTURE")["LAYOUT"] == "COG"
    norm_diff_impl.execute(rasters=[Path("crop_green.tif"), Path("crop_nir.tif")])
    with rasterio.open("norm_diff.tif") as ndwi:
        np.testing.assert_array_equal(ndwi.read(1)[:, :3], -0.5)
        np.testing.assert_array_equal(ndwi.read(1)[:, 3:], 0.5)
    otsu_impl.execute(raster=Path("norm_diff.tif"))
    with rasterio.open("otsu.tif") as mask:
        np.testing.assert_array_equal(mask.read(1)[:, :3], 0)
        np.testing.assert_array_equal(mask.read(1)[:, 3:], 1)
        assert mask.nodata is None
    stac_impl.execute(input_item=source_catalog, water_body=Path("otsu.tif"))
    result = read_item(Path("catalog"))
    validate_item(result)
    assert result.id == "synthetic"
    assert result.datetime == read_item(source_catalog).datetime
    assert result.bbox == [1, 1, 7, 7]
    assert ProjectionExtension.ext(result).shape == [6, 6]
    assert RasterExtension.ext(result.assets["data"]).bands is not None
    href = result.assets["data"].get_absolute_href()
    assert href is not None and Path(href).is_file()


@pytest.mark.parametrize("aoi", ["1,2,3", "7,7,1,1", "100,100,101,101"])
def test_crop_rejects_invalid_or_disjoint_aoi(source_catalog: Path, aoi: str) -> None:
    with pytest.raises(ValueError):
        crop_impl.execute(input_item=source_catalog, aoi=aoi, epsg="4326", band="green")


def test_crop_rejects_missing_band(source_catalog: Path) -> None:
    with pytest.raises(ValueError, match="not found"):
        crop_impl.execute(input_item=source_catalog, aoi="1,1,7,7", epsg="4326", band="nir08")


def test_norm_diff_rejects_wrong_count() -> None:
    with pytest.raises(ValueError, match="Exactly two"):
        norm_diff_impl.execute(rasters=[])


def test_norm_diff_rejects_different_grids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source_catalog: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    crop_impl.execute(input_item=source_catalog, aoi="1,1,7,7", epsg="4326", band="green")
    crop_impl.execute(input_item=source_catalog, aoi="2,2,7,7", epsg="4326", band="nir")
    with pytest.raises(ValueError, match="must match"):
        norm_diff_impl.execute(rasters=[Path("crop_green.tif"), Path("crop_nir.tif")])


def test_otsu_nonfinite_pixels_are_non_water() -> None:
    mask = otsu_impl.threshold(np.array([-0.5, 0.5, np.nan, np.inf], dtype=np.float32))
    np.testing.assert_array_equal(mask, [0, 1, 0, 0])


def test_otsu_rejects_empty_finite_population() -> None:
    with pytest.raises(ValueError, match="no finite"):
        otsu_impl.threshold(np.array([np.nan, np.inf], dtype=np.float32))


def test_validation_rejects_invalid_projection(source_catalog: Path) -> None:
    item = read_item(source_catalog)
    ProjectionExtension.ext(item, add_if_missing=True).shape = [2]
    import pystac

    with pytest.raises(pystac.errors.STACValidationError):
        validate_item(item)


def test_crop_transforms_projected_aoi(
    source_catalog: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    crop_impl.execute(
        input_item=source_catalog,
        aoi="150000,150000,750000,750000",
        epsg="EPSG:3857",
        band="green",
    )
    with rasterio.open("crop_green.tif") as raster:
        assert tuple(raster.bounds) == (1, 1, 7, 7)
        assert raster.shape == (6, 6)


def test_zero_denominator_ndwi_is_nonfinite(
    source_catalog: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    for band in ("green", "nir"):
        crop_impl.execute(input_item=source_catalog, aoi="1,1,7,7", epsg="4326", band=band)
    for band in ("green", "nir"):
        with rasterio.open(f"crop_{band}.tif") as source:
            pixels = source.read(1)
            metadata = source.meta.copy()
        pixels[0, 0] = 0
        metadata.update(driver="GTiff")
        with rasterio.open(f"zero_{band}.tif", "w", **metadata) as output:
            output.write(pixels, 1)
    norm_diff_impl.execute(rasters=[Path("zero_green.tif"), Path("zero_nir.tif")])
    with rasterio.open("norm_diff.tif") as ndwi:
        assert np.isnan(ndwi.read(1)[0, 0])


def test_staged_source_remains_readable_after_relocation(
    source_catalog: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import shutil

    staged = tmp_path / "relocated-source"
    shutil.copytree(source_catalog, staged)
    monkeypatch.chdir(tmp_path)
    crop_impl.execute(input_item=staged, aoi="1,1,7,7", epsg="4326", band="green")
    assert (tmp_path / "crop_green.tif").is_file()
    item = read_item(staged)
    assert all(not Path(asset.href).is_absolute() for asset in item.get_assets().values())
