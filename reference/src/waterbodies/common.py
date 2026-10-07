"""Read staged STAC inputs shared by crop and output packaging."""

from pathlib import Path

import pystac


def read_item(directory: Path) -> pystac.Item:
    """Read the first recursive Item from a staged catalog.

    Raises:
        ValueError: If the staged document does not contain an Item.
    """
    document = pystac.read_file(str(directory / "catalog.json"))
    if isinstance(document, pystac.Item):
        return document
    if isinstance(document, pystac.Catalog):
        item = next(document.get_items(recursive=True), None)
        if item is not None:
            return item
    raise ValueError("Input must contain a STAC Item")
