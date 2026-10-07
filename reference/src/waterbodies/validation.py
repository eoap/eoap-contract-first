"""Validate STAC with official extension schemas bundled for offline execution."""

import json
from pathlib import Path

import pystac
from pystac.validation import JsonSchemaSTACValidator


def validate_item(item: pystac.Item) -> None:
    """Validate core STAC and every declared extension with PySTAC.

    Known output extension schemas are cached locally. Other extensions retain
    PySTAC's normal schema resolution behavior.
    """
    validator = JsonSchemaSTACValidator()
    for name in ("projection", "raster", "eo"):
        schema = json.loads((Path(__file__).parent / "schemas" / f"{name}.json").read_text())
        validator.schema_cache[schema["$id"].rstrip("#")] = schema
    item.validate(validator=validator)
