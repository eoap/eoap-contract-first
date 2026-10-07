# Derive artifacts

The installed runtime discovers plugins through their entry points. Explicit source fragments select #waterbodies for diagrams, documentation, input templates, OGC descriptions and OCI metadata. scripts/derive.sh records each actual invocation; reference/expected contains outputs generated during bootstrap, not invented approximations.

The current cwl2markdown revision has a filename regression: it requests index.md but ships index.md.jinja. scripts/markdown_compat.py maps requested .md filenames to upstream .md.jinja files, then runs the original runtime and plugin. The upstream output filename is waterbodies.md.jinja even though its content is already rendered Markdown. This is documented rather than presented as a supported plugin option. Plugin timestamps and blank-node traversal can make byte-for-byte output differ.

## Contract questions

What are we designing? Generate genuine projections from the selected contract.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
