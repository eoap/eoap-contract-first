# Exercise — Design the contract

## 1. Design a scratch tool

- Copy the crop `CommandLineTool` from `reference/waterbodies.cwl` into `build/scratch-crop.cwl`.
- Set `cwlVersion` to `v1.2` and retain the required declarations.
- Design typed inputs and the cropped `File` output before opening `crop_impl.py`.

## 2. Validate and compare

Validate your scratch document from the repository root:

```console
uv run cwltool --validate build/scratch-crop.cwl
```

Compare its required inputs, defaults, bindings and output glob with the canonical crop contract.

## Verify your work

Validate the repository contracts with `cwltool --validate`: the canonical `reference/waterbodies.cwl#waterbodies` workflow and the v1/v2 examples from module 11. This checks CWL declarations and references without running the processing tools. It does not validate your scratch document; use the separate command in step 2 for that.

Run from the repository root:

```console
task contract:validate
```

Success means all three documents validate and the task exits with code `0`. If validation fails, use the document location and error message to identify the declaration or reference that needs correction.

**Expected outcome:** The canonical graph validates, with one `Workflow` and four `CommandLineTool` definitions.

Compare [the solution](solution.md). Return to [the module](README.md).
