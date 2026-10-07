# Contract-first Water Bodies

Design the application contract, derive interfaces, implement the real raster algorithm, compose the workflow, then package and deploy a tested release.

Start with the [learning path](learning-path.md) and [prerequisites](prerequisites.md).

The CWL contract is the authoritative description of the EO application. Implementations, interfaces, workflow composition, documentation, metadata, supply-chain evidence, packaging and deployment artifacts are derived from or traceable back to it.

A machine-readable EO application contract provides inputs and evidence for software supply-chain assurance. Security depends on inventory, scanning, policy, identity, signing and promotion working together.

```mermaid
flowchart TD
  C[CWL contract] --> CLI[Generated CLI]
  C --> W[Workflow]
  C --> M[Documentation and metadata]
  CLI --> I[Implementations]
  I --> V[Versioned containers]
  W --> V
  V --> T[Tests and compatibility assurance]
  T --> S[SBOM and image identities]
  M --> A[OCI annotations]
  S --> G[Policy and promotion gates]
  A --> G
  G --> O[Versioned EOAP OCI artifact]
  O --> R[OCI registry]
  R --> P[OGC API - Processes]
  P --> E[Execution]
```
