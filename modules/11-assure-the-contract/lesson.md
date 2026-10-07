# Evolve and assure the contract

v1 has a default AOI CRS; v2 removes that default and therefore requires callers to supply epsg. This is a breaking omission change and needs a major increment from 1.0.0 to 2.0.0. The actual baseline plugin compares normalized process interfaces, environment and behavior and records findings.

Removing a default also needs behavioral review. Generated array blank-node names can add review findings even when an array is unchanged. Run baseline without --check first, inspect all findings, then explicitly classify this known lesson change with --review-bump major. The task contains that lesson-specific reviewed classification; production release review remains an explicit input to protected release CI, not an automatic major approval.

## Contract questions

What are we designing? Classify a public input change and its minimum SemVer release.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
