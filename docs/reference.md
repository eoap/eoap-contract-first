# Canonical reference

| Artifact | Repository location | Verify or regenerate |
| --- | --- | --- |
| CWL graph | reference/waterbodies.cwl | task contract:validate |
| CLI | reference/src/waterbodies/waterbodies.py | task cli:generate; task cli:test |
| Python callbacks | reference/src/waterbodies/*_impl.py | task test |
| Workflow input | reference/inputs.yaml | task workflow:run |
| Containers | reference/containers/*/Dockerfile | task containers:build |
| Projections | reference/expected | task artifacts:derive |
| Compatibility | reference/expected/baseline/report.json | task baseline:check |
| Local OCI artifact | build/oci | task oci:package; task oci:inspect |
| Real SBOM bundle | build/sbom | task sbom:generate; task sbom:check |

A real historical localhost SBOM bundle is committed under reference/expected/sbom/local-example and is integrity-tested. Regenerate its output family with task supply-chain:integration after building the four images. Its image digests and package inventory are genuine; its temporary registry names are not promoted release references. No fabricated signature, digest or successful remote job is supplied.

The scientific tools emit crop_<band>.tif, norm_diff.tif, otsu.tif and catalog/. Run commands in scratch directories to keep outputs separate. Use `uv run waterbodies <subcommand> --help` for the generated contract options.
