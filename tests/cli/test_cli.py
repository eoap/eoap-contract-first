from pathlib import Path

import pytest
from click.testing import CliRunner
from waterbodies.cli import waterbodies

USAGE_ERROR_EXIT_CODE = 2


@pytest.mark.parametrize("arguments", [[], ["crop"], ["norm-diff"], ["otsu"], ["stac"]])
def test_generated_help(arguments: list[str]) -> None:
    result = CliRunner().invoke(waterbodies, [*arguments, "--help"])
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.output


def test_generated_crop_callback(
    source_catalog: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(
        waterbodies,
        [
            "crop",
            "--input-item",
            str(source_catalog),
            "--aoi",
            "1,1,7,7",
            "--epsg",
            "EPSG:4326",
            "--band",
            "green",
        ],
    )
    assert result.exit_code == 0, str(result.exception)
    assert Path("crop_green.tif").is_file()


def test_paths_and_required_options_are_checked() -> None:
    result = CliRunner().invoke(waterbodies, ["otsu", "--raster", "/missing-waterbodies.tif"])
    assert result.exit_code == USAGE_ERROR_EXIT_CODE
