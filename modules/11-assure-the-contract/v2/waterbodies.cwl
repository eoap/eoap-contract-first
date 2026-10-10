cwlVersion: v1.2
$namespaces:
  s: https://schema.org/
s:name: Water Bodies
s:description: Detect water using green and near-infrared reflectance, NDWI and Otsu.
s:dateCreated: "2026-10-07"
s:softwareVersion: "2.0.0"
s:license: https://spdx.org/licenses/Apache-2.0
s:softwareHelp:
  s:url: https://github.com/eoap/waterbodies-learning
s:publisher:
  s:class: s:Organization
  s:name: EOAP
s:author:
  s:class: s:Person
  s:givenName: Fabrice
  s:familyName: Brito
  s:email: fabrice.brito@terradue.com
  s:affiliation:
    s:class: s:Organization
    s:name: Terradue
$graph:
- id: waterbodies
  class: Workflow
  label: Water Bodies
  doc: Detect water from a staged STAC Item using NDWI and Otsu.
  requirements:
    ScatterFeatureRequirement: {}
  inputs:
    item: Directory
    aoi: string
    epsg: string
    bands:
      type: string[]
      default: [green, nir]
  outputs:
    stac-catalog:
      type: Directory
      outputSource: stac/stac-catalog
  steps:
    crop:
      run: '#crop'
      in: {item: item, aoi: aoi, epsg: epsg, band: bands}
      scatter: band
      scatterMethod: dotproduct
      out: [cropped]
    norm-diff:
      run: '#norm-diff'
      in: {rasters: crop/cropped}
      out: [ndwi]
    otsu:
      run: '#otsu'
      in: {raster: norm-diff/ndwi}
      out: [binary-mask]
    stac:
      run: '#stac'
      in: {item: item, water-body: otsu/binary-mask}
      out: [stac-catalog]
- id: crop
  class: CommandLineTool
  label: Crop
  doc: Crop the data asset selected by EO common band name to a bounding box or polygon.
  baseCommand: [waterbodies, crop]
  hints:
    DockerRequirement: {dockerPull: 'ghcr.io/eoap/waterbodies-crop:1.0.0'}
  inputs:
    item:
      type: Directory
      doc: Staged self-contained STAC catalog containing the source Item and bands.
      inputBinding: {prefix: --input-item}
    aoi:
      type: string
      doc: xmin,ymin,xmax,ymax or GeoJSON polygon in the supplied CRS.
      inputBinding: {prefix: --aoi}
    epsg:
      type: string
      doc: AOI coordinate reference system, for example EPSG:4326.
      inputBinding: {prefix: --epsg}
    band:
      type: string
      doc: EO common band name; green or nir for NDWI.
      inputBinding: {prefix: --band}
  outputs:
    cropped:
      type: File
      outputBinding: {glob: 'crop_*.tif'}
- id: norm-diff
  class: CommandLineTool
  label: Normalized difference
  doc: Calculate (green - nir) / (green + nir) on matching raster grids.
  baseCommand: [waterbodies, norm-diff]
  hints:
    DockerRequirement: {dockerPull: 'ghcr.io/eoap/waterbodies-norm-diff:1.0.0'}
  inputs:
    rasters:
      type:
        type: array
        items: File
        inputBinding: {prefix: --rasters}
      doc: Exactly two rasters in green, nir order.
      inputBinding: {}
  outputs:
    ndwi:
      type: File
      outputBinding: {glob: norm_diff.tif}
- id: otsu
  class: CommandLineTool
  label: Otsu
  doc: Threshold finite NDWI pixels; nonfinite pixels are non-water.
  baseCommand: [waterbodies, otsu]
  hints:
    DockerRequirement: {dockerPull: 'ghcr.io/eoap/waterbodies-otsu:1.0.0'}
  inputs:
    raster:
      type: File
      inputBinding: {prefix: --raster}
  outputs:
    binary-mask:
      type: File
      outputBinding: {glob: otsu.tif}
- id: stac
  class: CommandLineTool
  label: STAC
  doc: Package the water mask as a validated self-contained STAC catalog.
  baseCommand: [waterbodies, stac]
  hints:
    DockerRequirement: {dockerPull: 'ghcr.io/eoap/waterbodies-stac:1.0.0'}
  inputs:
    item:
      type: Directory
      inputBinding: {prefix: --input-item}
    water-body:
      type: File
      inputBinding: {prefix: --water-body}
  outputs:
    stac-catalog:
      type: Directory
      outputBinding: {glob: catalog}
