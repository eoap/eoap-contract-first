# Notebook practice labs

Run the course commands inside notebooks, with the explanation and result in the same place. Each module has a Bash notebook following the persistent-shell approach used by the Mastering Application Packages course. Python heredocs inspect rasters and STAC objects while the notebook remains on its Bash kernel.

## Open a lab in the dev-platform workspace

The course runs through `dev-platform-eoap/eoap-contract-first` on **Minikube or a Kubernetes cluster**, using **`eoepca/pde-code-server:amd64`**. This image already has the Bash kernel installed. Workspace startup installs the locked course packages; students do not install kernels or run environment setup.

1. Open this course checkout in the workspace editor.
2. Open a notebook below and select **Bash** in the kernel picker.
3. Run cells in order with **Shift+Enter**, predicting results before executing commands.
4. Stop at unexpected errors. Read the cell output, correct the cause and rerun the cell. Restarting the kernel clears its variables; rerun the workspace cell after a restart.

Use the image's existing **Bash** kernel. Each lab activates the course `.venv` inside that shell, so its commands use the course packages even though the kernel comes from the container image. If the kernel or course environment is unavailable, the instructor checks platform provisioning.

A Kubernetes workspace runs the local scientific tools inside its editor pod. That does not imply it has a Docker engine or that its checkout is shared with Calrissian tool pods. The local path works without a container engine. Integration cells describe the extra service, input and storage preparation they require.

## Follow the modules

| Module | Executable lab | What you practise |
| --- | --- | --- |
| 00 | [Understand Water Bodies](00-waterbodies.ipynb) | Predict reflectance, view NDWI/masks and validate the product. |
| 01 | [Design the contract](01-design-the-contract.ipynb) | Edit and validate scratch CWL interfaces. |
| 02 | [Derive the CLI](02-derive-the-cli.ipynb) | Generate Click commands and check required options. |
| 03 | [Implement crop](03-implement-crop.ipynb) | Inspect COG grids and reject disjoint AOIs. |
| 04 | [Implement normalized difference](04-implement-norm-diff.ipynb) | Reverse bands and reject unequal grids. |
| 05 | [Implement Otsu](05-implement-otsu.ipynb) | Count classes and explore nonfinite pixels. |
| 06 | [Implement STAC](06-implement-stac.ipynb) | Inspect PySTAC extensions and exercise validation. |
| 07 | [Compose the workflow](07-compose-the-workflow.ipynb) | Trace scatter, run the graph and inspect its output. |
| 08 | [Containerize](08-containerize.ipynb) | Inspect image declarations and optionally build/run images. |
| 09 | [Run the application](09-run-the-application.ipynb) | Validate relocated products and optionally run Calrissian. |
| 10 | [Derive artifacts](10-derive-artifacts.ipynb) | Generate and compare genuine contract projections. |
| 11 | [Evolve and assure the contract](11-assure-the-contract.ipynb) | Observe a failing compatibility gate and record a review. |
| 12 | [Publish research software](12-publish-research-software.ipynb) | Compare CodeMeta with CWL and citation metadata. |
| 13 | [Secure, promote and deploy](13-secure-promote-deploy.ipynb) | Inspect evidence, package locally and use configured live services. |

Module 00 also retains its [Python exploration notebook](../modules/00-waterbodies/waterbodies.ipynb) for additional graphical experiments.

## Keep an execution record

All labs write under `.notebook-runs/<module>/`, which Git ignores. No lab deletes another module's results. Rerunning processing cells replaces that lab's existing files; fresh CWL workflow runs, SBOM bundles and Calrissian runs get their own directories. Add Markdown cells to record predictions, observations and the contract declaration that explains them. Keep secrets out of notebook cells and saved outputs.

The default local activity and marked integrations have separate completion criteria. An integration cell that prints **skipped** has not verified Docker, Kubernetes, registry scanning or deployment. The notebooks do not fabricate published images, digests or successful remote jobs. Complete those sections using the instructor-provided services when they form part of your course session.

## Provision and verify the course environment

These are **instructor/startup commands**; students use the notebook interface above.

```console
task notebooks:check
```

For dev-platform startup, synchronize the course packages with `uv sync --locked --extra tooling --extra dev --extra notebook`. Keep the image's preinstalled Bash kernelspec. Register `Python (eoap-contract-first)` separately only for the supplementary Python exploration notebook.

`task notebooks:setup` and [setup.ipynb](setup.ipynb) are optional helpers for a separate local JupyterLab or VS Code installation. They register course-backed kernels there; they are not part of student setup in the dev-platform workspace.

The check task installs temporary kernels under `.notebook-runs/jupyter`, executes every numbered lab with its real Bash kernel and saves executed copies under `.notebook-runs/executed`. It disables container builds, fresh registry scans, Kubernetes execution and live ZOO deployment. ORAS packaging runs when the CLI is available. It leaves source notebooks without stored execution outputs.

For a local JupyterLab session, the instructor can launch the notebook index with:

```console
task notebooks:setup
uv run --extra tooling --extra dev --extra notebook jupyter lab practice-labs
```

See [prerequisites](https://github.com/eoap/eoap-contract-first/blob/main/docs/prerequisites.md), [the learning path](https://github.com/eoap/eoap-contract-first/blob/main/docs/learning-path.md), [supply-chain preparation](https://github.com/eoap/eoap-contract-first/blob/main/docs/supply-chain.md) and [deployment staging](https://github.com/eoap/eoap-contract-first/blob/main/docs/deployment.md) for the configured integration environments.
