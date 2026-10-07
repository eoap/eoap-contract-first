from pathlib import Path

import pytest


@pytest.fixture
def source_catalog() -> Path:
    return Path(__file__).parents[1] / "data/fixtures/source"
