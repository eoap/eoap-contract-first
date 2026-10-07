# Secure, promote and deploy

The capstone turns a tested contract into a versioned OCI artifact with associated evidence. Follow docs/supply-chain.md for container builds, Trivy-backed SBOM generation, checksum/coverage checks, vulnerability policy, annotation generation and local ORAS packaging. Release CI uses a protected GitHub environment; verification jobs have no registry publication permission.

cwl2sbom inventories reachable declared containers and writes workflow.cdx.json, images/*.cdx.json, images.lock.json and coverage.json. Its workflow inventory explicitly reports incomplete aggregate composition because runtime downloads and host software are outside scope. cwl2oci emits annotation metadata under $manifest. ORAS separately packages application/cwl and attaches CycloneDX evidence by digest. Neither generator signs or enforces security policy.

Promotion requires passing checks and an explicit review decision. Inventory is not a vulnerability report, evidence attachment is not trust, and a clean severity scan is not proof of security. Optional signing and provenance exercises are documented without fabricated claims. Deployment retrieves the promoted CWL artifact by digest, then posts its bytes using ZOO's verified application/cwl+yaml route. A remote staged Directory must be accessible to the server; a local fixture path is not a remote execution input.

## Contract questions

What are we designing? Promote tested immutable application artifacts and execute them through ZOO.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
