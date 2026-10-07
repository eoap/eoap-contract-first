# Actual inventory example

`local-example/` is an unmodified cwl2sbom/Trivy bundle generated on 2026-10-07 by inspecting the four built Water Bodies 1.0.0 images through a temporary localhost registry. The included waterbodies.cwl records the exact inspected references. Those localhost names are a historical fixture, not an accessible promoted release. No image digests or inventories were fabricated.

It contains workflow.cdx.json, images/*.cdx.json, images.lock.json and coverage.json. The workflow inventory's composition remains incomplete according to upstream semantics; declared tool coverage is complete. Its image SBOMs carry actual Trivy package inventories. They are not vulnerability reports, signatures or promotion approvals.

Reproduce this family of real outputs using `task containers:build VERSION=1.0.0` followed by `task supply-chain:integration`. scripts/local_supply_chain.sh starts an ephemeral localhost registry, pushes the built images locally, runs the actual plugin with explicit linux/amd64 and removes the registry. Rebuilt digests, timestamps and assigned registry ports can differ. It never pushes to GHCR.

Use `task sbom:generate` for a fresh bundle against published canonical release dependencies. Never reuse this historical localhost example as release evidence. The example image scan exposed HIGH/CRITICAL base-image vulnerabilities, and our promotion policy rejects those findings without suppression.
