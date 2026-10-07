# Publish research software

Schema.org metadata in the CWL identifies the application, version, license, author, publisher and help location. The verified cwl2codemeta plugin converts normalized metadata into CodeMeta 3.0 JSON-LD and can associate the source repository and development links. The output is in reference/expected/publication/codemeta.json.

CITATION.cff is repository citation metadata maintained as release editorial metadata; it is not claimed to be plugin-generated. This bootstrap verifies CodeMeta, not DataCite, RO-Crate or an unverified citation plugin. Publication metadata supports scholarly credit and discovery. An SBOM describes software inventory, a signature asserts artifact identity, and provenance describes a build. None substitutes for citation metadata.

## Contract questions

What are we designing? Distinguish citation and CodeMeta from security evidence.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
