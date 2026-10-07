# Deploy a promoted application through ZOO

Deployment consumes a tested, promoted artifact. The verified reference is [EOAP's ZOO course](https://github.com/eoap/ogc-api-processes-with-zoo), specifically deploy-application.md, app-package.md, execute-monitor-process.md and its OpenAPI resource. Start that server and execution backend following its instructions. The examples below use its API route structure; set the actual tenant/API base URL.

ZOO's documented deployment supports CWL bytes or an HTTP application-package reference. This bootstrap does not assume it accepts OCI references directly. Pull the promoted artifact by digest first:

```bash
export EOAP_REF='ghcr.io/eoap/waterbodies@sha256:REPLACE_WITH_PROMOTED_DIGEST'
oras discover "$EOAP_REF"
oras pull "$EOAP_REF" -o build/promoted
export API='http://localhost:8080/ogc-api'
curl --fail-with-body -X POST "$API/processes?w=waterbodies" \
  -H 'Accept: application/json' -H 'Content-Type: application/cwl+yaml' \
  --data-binary @build/promoted/waterbodies.cwl
```

Replace the placeholder with an inspected, verified digest. Confirm its annotations, referrers and policy evidence before deployment. The server-specific `w` selector follows the ZOO tutorial; a different implementation may use another process selection mechanism. Keep authentication in your environment/client configuration according to the deployed server, not in committed commands.

Discover, describe and inspect the installed package:

```bash
curl --fail-with-body "$API/processes"
curl --fail-with-body "$API/processes/waterbodies"
curl --fail-with-body "$API/processes/waterbodies/package"
```

Verify the returned identifier and follow links in responses if the server assigns a different id. Compare the retrieved package's scientific tool contracts and immutable image declarations with the promoted CWL. Service description generation with cwl2ogc is separate from installation and does not itself deploy anything.

## Supply an executable input

The canonical workflow requires a staged STAC **Directory**. A JSON Item URL is not interchangeable with that Directory. Upload/prepare the catalog.json, linked Item JSON and both band rasters on storage accessible to the ZOO execution backend, using that environment's established staging mechanism. For the compact fixture, transfer the entire `data/fixtures/source` directory. Preserve all relative links. Confirm that the backend can read it and materialize it as a CWL Directory.

Inspect the deployed process description for the accepted Directory representation. `reference/expected/ogc/processes.json` is generated from the canonical contract and describes its ports. ZOO backend adapters differ in how they stage complex Directory values; there is no universal upload endpoint assumed here. Supply a backend-accessible Directory `location`, not the learner's local path. Some installations require a separate stage-in wrapper like the EOAP application-package-patterns examples; in that case deploy the environment's verified stage-in wrapper around #waterbodies rather than changing the scientific tool interfaces.

Prepare `build/execute.json` using the advertised process input schemas and the verified backend's Directory staging convention. A CWL-native backend representation is illustrated in `supply-chain/examples/execute.json`; replace its placeholder. This example is an execution request, not a claim that every ZOO backend accepts that Directory encoding. The file is intentionally not a runnable remote request until storage and staging are configured.

```bash
curl --fail-with-body -D build/job.headers \
  -X POST "$API/processes/waterbodies/execution" \
  -H 'Content-Type: application/json' -H 'Prefer: respond-async' \
  --data-binary @build/execute.json
```

Capture the job id/status location from the response. Follow the returned status link, or the verified ZOO resources:

```bash
export JOB_ID='REPLACE_WITH_RETURNED_JOB_ID'
curl --fail-with-body "$API/jobs/$JOB_ID"
curl --fail-with-body "$API/jobs/$JOB_ID/results"
```

Wait for successful completion; failed jobs require inspecting the server's diagnostics and staging access. Retrieve the result href returned by the service. Parse the output catalog through PySTAC and validate the Item and declared extensions. For the transferred compact fixture, confirm 6×6 pixels and 18 water pixels.

The completion record is the promoted artifact digest, deployed process id, returned package identity, successful job id and validated output catalog. This repository does not include a fabricated live job result: execution needs a running configured server, published container identities and backend-accessible inputs.
