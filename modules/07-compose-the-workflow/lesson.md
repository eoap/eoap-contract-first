# Compose the workflow

The Workflow reuses #crop, #norm-diff, #otsu and #stac from the same graph that generated the CLI. ScatterFeatureRequirement scatters crop over the bands input with dotproduct. Default green,nir order yields File[] for normalized difference. NDWI feeds Otsu; its binary-mask and the original source Directory feed STAC.

Steps declare `in`, `out`, `run` and optional scatter. Workflow outputs use outputSource to collect stac/stac-catalog. A workflow port is an interface; outputSource is the wiring behind it. Scatter is composition, not an implementation loop. The complete runner test proves staging, array bindings, callbacks and output collection agree.

## Contract questions

What are we designing? Connect the same tool contracts with scatter and typed dataflow.

Why does it belong in the contract? Clients and runners need a stable description of the inputs, outputs and dependencies before choosing an implementation.

What can be derived? Inspect the relevant CLI, workflow wiring and metadata projections from the same canonical CWL.

How do we verify it? Run the command in [the exercise](exercise.md) and inspect its observable result.

[Module overview](README.md)
