import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import rasterio
from waterbodies.common import read_item
from waterbodies.validation import validate_item

EXPECTED_WATER_PIXELS = 18

ROOT = Path(__file__).parents[2]


def test_cwl_runner_executes_the_scattered_workflow(tmp_path: Path) -> None:
    runner = shutil.which("cwltool")
    assert runner is not None
    executable = shutil.which("waterbodies")
    assert executable is not None
    completed = subprocess.run(
        [
            runner,
            "--no-container",
            "--outdir",
            str(tmp_path),
            str(ROOT / "reference/waterbodies.cwl") + "#waterbodies",
            str(ROOT / "reference/inputs.yaml"),
        ],
        capture_output=True,
        text=True,
        check=True,
        env=os.environ.copy(),
        timeout=120,
    )
    outputs = json.loads(completed.stdout)
    assert outputs["stac-catalog"]["class"] == "Directory"
    item = read_item(tmp_path / "catalog")
    validate_item(item)
    with rasterio.open(tmp_path / "catalog/synthetic/otsu.tif") as mask:
        assert mask.shape == (6, 6)
        assert np.count_nonzero(mask.read(1)) == EXPECTED_WATER_PIXELS
