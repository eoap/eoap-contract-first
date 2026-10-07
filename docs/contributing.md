# Contributing

Design contract changes first. Regenerate the bundled CLI with task cli:generate and implement its callbacks. Preserve the real scientific chain and PySTAC extension APIs. Add meaningful behavioral tests and classify compatibility changes.

```console
task setup
task reference:test
hatch run dev:format-check
hatch run dev:lint-check
hatch run dev:typecheck
hatch run dev:security
hatch run test:test
```

Do not hand-edit generated files or schema-defined Python models. The generated CLI is excluded from style gates because it is upstream output; its complete syntax is regression-tested against upstream generation. Missing scientific dependency call annotations are isolated with mypy's untyped_calls_exclude for rasterio/skimage/shapely; application APIs remain fully annotated.

Generated snapshots can contain timestamps, anonymous schema ids and traversal order. Verify semantic output and explicit source fragments. Run task artifacts:derive after relevant metadata or wiring changes, and inspect the diff.

Release publication uses a protected environment and reviewed compatibility classification. Never publish artifacts from PR verification. Report precisely which remote/container checks were executed and which require external infrastructure.
