# Water Bodies application

The installable reference application implements the contract in waterbodies.cwl.
Its bundled CLI is generated with cwl2click; processing callbacks use PySTAC and rasterio.

For the complete learning and verification environment, run task setup and task reference:test from the repository root.

Build this application wheel with `hatch build -t wheel` in this directory. Install it and run `waterbodies --help`. Container builds use the root build context and resolve dependency wheels in their builder stage.
