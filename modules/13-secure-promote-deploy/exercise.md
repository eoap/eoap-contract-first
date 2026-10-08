# Exercise — Secure, promote and deploy

## 1. Prepare the environment

Run commands from the repository root.

- Install ORAS for local OCI packaging.
- For real SBOM generation, install Trivy and make the declared versioned container images available in an accessible registry.
- For deployment, configure ZOO and its execution backend, server authentication and backend-accessible staged inputs. See the [deployment guide](../../deployment.md).

## 2. Package and inspect locally

```console
task oci:package
```

```console
task oci:inspect
```

Record the inspected artifact digest. Local packaging does not publish or promote the artifact.

## 3. Generate and check real evidence

Follow the [supply-chain preparation guide](../../supply-chain.md#local-preparation) to prepare the release contract and publish its declared container dependencies before running:

```console
task sbom:generate CONTRACT=build/release/waterbodies.cwl PLATFORM=linux/amd64
```

The default `build/sbom` output directory must not already exist; use a fresh `SBOM` path for repeat runs and pass it consistently to subsequent checks.

```console
task sbom:check CONTRACT=build/release/waterbodies.cwl
```

```console
bash supply-chain/policy/scan.sh build/sbom
```

Inspect coverage, image identities and policy findings before proceeding through the documented promotion process.

## 4. Deploy and execute the promoted package

Follow the [deployment guide](../../deployment.md) using an actual promoted digest and your configured server.

- Pull the artifact by digest and verify its package and evidence.
- Deploy, discover and describe the process, then inspect its installed package.
- Stage the complete input catalog where the backend can read it.
- Execute, monitor the returned job and retrieve its results.
- Validate the output catalog through PySTAC.

## 5. Record completion

Record the promoted artifact digest, deployed process identifier, returned package identity, successful job ID and validated output location. Keep server credentials out of the record.

## Verify your work

This task inventories the canonical container declarations and runs the local supply-chain tests. These cover release identities, OCI metadata, optional ORAS round-trip packaging and the integrity of bundled SBOM evidence. It does not run the live vulnerability-policy scan or deploy to ZOO.

Run from the repository root:

```console
task supply-chain:check
```

Success means inventory and tests pass; an ORAS skip means packaging was not exercised by that test. Independently retain the policy results and successful deployment record from steps 3–5. A failed test identifies a local reference, packaging or evidence-integrity problem; live job failures require the server diagnostics and staging-access checks in the deployment guide.

**Expected outcome:** Local package inspection succeeds. A configured ZOO environment can execute the promoted package; deployment requires an accessible staged input and server credentials.

Compare [the solution](solution.md). Return to [the module](README.md).
