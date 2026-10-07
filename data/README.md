# Compact fixture

`fixtures/source` contains synthetic uint16 green/nir 8×8 GeoTIFFs and a PySTAC catalog. Coordinates are EPSG:4326, pixel size is one degree, observation time is 2024-01-01T00:00:00Z. This is synthetic educational data, not observed Earth imagery.

Regenerate with `task fixtures:generate`. The left half has green=100,nir=300; the right half has green=300,nir=100. AOI 1,1,7,7 yields 36 pixels with 18 water pixels. Raster values are reflectance-like controlled inputs, with no claim of radiometric realism. Fixture creation and output use PySTAC and extension validation.
