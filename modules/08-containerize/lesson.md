# Containerize

Four Dockerfiles build the canonical implementation into named component images. They share the reference application wheel and follow the company Rocky Linux multi-stage template: build all wheels in a builder, install offline into a non-root runtime virtual environment, check dependencies and CLI help, then remove pip. Their CWL DockerRequirement hints declare ghcr.io/eoap/waterbodies-{component}:1.0.0. A local no-container run uses the installed Python package; normal container execution uses those image references.

SemVer tags identify releases but registries may allow retagging. A SHA256 digest identifies immutable content. Release CI inspects published versioned containers with cwl2sbom and rewrites release CWL to reported digests. Container CMD is a help default; there is no conflicting ENTRYPOINT because CWL supplies waterbodies and its subcommand. Future independent component releases need not match the application version.

## Contract questions

What are we designing? Represent execution environments as versioned dependencies.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
