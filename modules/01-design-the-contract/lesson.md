# Design the contract

The public processing API belongs in CWL. A [CommandLineTool](https://www.commonwl.org/v1.2/CommandLineTool.html#CommandLineTool) declares its `id`, `baseCommand`, input types, bindings and file outputs. [Directory](https://www.commonwl.org/v1.2/CommandLineTool.html#Directory) means a staged catalog with local assets; [File](https://www.commonwl.org/v1.2/CommandLineTool.html#File) means a runner-managed raster. Strings describe the AOI, CRS and band common name. Required inputs and defaults determine whether clients may omit a value.

Read the four tools in `reference/waterbodies.cwl` without looking at Python. The crop contract tells you precisely what implementation must accept and which file it must produce. An output glob is part of the API: naming a file differently breaks collection even if the algorithm succeeds. Contract design is top-down; testing the implementation and workflow proceeds bottom-up. Contract and implementation are distinct artifacts.

## Reuse an existing type

Before defining a structured input, check the [EOAP schema reference](https://eoap.github.io/schemas/reference/). It provides named CWL types for GeoJSON, OGC bounding boxes, STAC metadata and string formats. Reusing a type lets tools agree on field names and types without maintaining separate definitions.

For an AOI expressed as a record, the OGC `BBox` type is a starting point. Following the [schema reuse guide](https://eoap.github.io/schemas/how-to/use-schema/), merge this fragment into a scratch tool's existing requirements and inputs:

```yaml
requirements:
  SchemaDefRequirement:
    types:
      - $import: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml
inputs:
  aoi:
    type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
```

`$import` loads the definitions; the input selects a named type using the same schema URL followed by `#BBox`. Read its fields and supply a matching job input:

```yaml
aoi:
  bbox: [100.0, 0.0, 101.0, 1.0]
  crs: CRS84
```

The [bounding-box example](https://eoap.github.io/schemas/ogc/bbox/) shows how bindings consume these fields. A record declaration alone does not convert them into command arguments. Our crop CLI currently accepts separate AOI and EPSG strings; adopting `BBox` would require agreeing on CRS handling, updating bindings and implementation, and reviewing workflow connections. Keep that exploration in the scratch tool. For a reproducible contract, replace `main` with a reviewed commit in both URLs, or vendor the schema and use its local path consistently.

## Define a custom type when needed

If the shared types do not describe the required concept, define it in a separate CWL schema. For example, a future tool could accept a named pair of bands. Following the [custom-type guide](https://eoap.github.io/schemas/newtypes/), create `custom.yaml` beside the scratch tool with an array of named definitions:

```yaml
- name: BandPair
  type: record
  doc: Ordered common band names for a normalized difference (first - second) / (first + second).
  fields:
    - name: first
      type: string
    - name: second
      type: string
```

Import it and select the record in the tool:

```yaml
requirements:
  SchemaDefRequirement:
    types:
      - $import: custom.yaml
inputs:
  bands:
    type: custom.yaml#BandPair
```

A matching job input is:

```yaml
bands:
  first: green
  second: nir
```

Choose field types, required values and documentation before adding bindings. Add `inputBinding` or `arguments` entries that map the fields to the command's interface. Output records can use the same type identifier, with output bindings that collect the declared structure. This example explores a different interface from the canonical workflow's band array and normalized-difference tool's raster array.

## Verify structure and meaning

Validate the complete scratch tool, then run it with a matching input document from the directory containing those files:

```console
cwltool --validate tool.cwl
cwltool tool.cwl inputs.yaml
```

The first command checks the tool definition; the second also checks job inputs and executes the command. Exercise missing required fields and wrong field types as well as valid values. Verify the resulting arguments and outputs to check that bindings preserve the intended meaning.

[CWL structural types have limits](https://eoap.github.io/schemas/explanation/custom-types/): a named record does not enforce every rule of the external standard it represents. Application checks still need to cover constraints such as valid band names, bounding-box length and coordinate semantics. The shared `URI` and `DateTime` records contain strings; their names alone do not validate those formats. Similarly, a STAC metadata record does not replace the staged `Directory` and local assets required by our crop tool.

## Contract questions

What are we designing? Design typed tool inputs and outputs before writing processing code.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
