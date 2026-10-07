import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts.supply_chain import check_bundle, container_references, prepare_release

ROOT = Path(__file__).parents[2]

EXPECTED_TOOL_COUNT = 4


def test_canonical_images_have_release_identities() -> None:
    references = container_references(ROOT / "reference/waterbodies.cwl")
    assert len(references) == EXPECTED_TOOL_COUNT
    assert all(reference.endswith(":1.0.0") for reference in references)


def test_latest_is_rejected(tmp_path: Path) -> None:
    contract = ROOT / "reference/waterbodies.cwl"
    candidate = tmp_path / "latest.cwl"
    candidate.write_text(contract.read_text().replace("crop:1.0.0", "crop:latest"))
    with pytest.raises(ValueError, match="SemVer"):
        container_references(candidate)


def test_prepare_release_updates_metadata_and_all_images(tmp_path: Path) -> None:
    candidate = tmp_path / "release.cwl"
    prepare_release(ROOT / "reference/waterbodies.cwl", candidate, "1.2.0", None)
    assert yaml.safe_load(candidate.read_text())["s:softwareVersion"] == "1.2.0"
    assert all(image.endswith(":1.2.0") for image in container_references(candidate))


def test_actual_oci_projection_contains_selected_workflow_metadata() -> None:
    annotations = json.loads((ROOT / "reference/expected/oci/annotations.json").read_text())
    manifest = annotations["$manifest"]
    assert manifest["org.cwl.entrypoint"] == "waterbodies"
    assert manifest["org.cwl.type"] == "Workflow"
    assert manifest["org.opencontainers.image.version"] == "1.0.0"


def test_local_oras_packaging_round_trip(tmp_path: Path) -> None:
    oras = shutil.which("oras")
    if oras is None:
        pytest.skip("ORAS CLI is an external prerequisite for local packaging")
    contract = ROOT / "reference/waterbodies.cwl"
    annotations = ROOT / "reference/expected/oci/annotations.json"
    layout = tmp_path / "oci"
    subprocess.run(
        [
            "bash",
            str(ROOT / "supply-chain/oras/package.sh"),
            "1.0.0",
            str(contract),
            str(annotations),
            str(layout),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        timeout=30,
    )
    manifest = subprocess.run(
        [oras, "manifest", "fetch", "--oci-layout", f"{layout}:1.0.0"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(manifest.stdout)["artifactType"] == "application/cwl"
    restored = tmp_path / "restored"
    subprocess.run(
        [oras, "pull", "--oci-layout", f"{layout}:1.0.0", "-o", str(restored)],
        check=True,
        capture_output=True,
    )
    assert (restored / "waterbodies.cwl").read_bytes() == contract.read_bytes()


@pytest.fixture
def actual_sbom_bundle(tmp_path: Path) -> Path:
    source = ROOT / "reference/expected/sbom/local-example"
    destination = tmp_path / "sbom"
    shutil.copytree(source, destination)
    return destination


def test_actual_generated_bundle_passes_integrity_checks(actual_sbom_bundle: Path) -> None:
    check_bundle(actual_sbom_bundle / "waterbodies.cwl", actual_sbom_bundle)


def test_corrupted_image_sbom_is_rejected(actual_sbom_bundle: Path) -> None:
    image_sbom = next((actual_sbom_bundle / "images").glob("*.json"))
    image_sbom.write_text("{}")
    with pytest.raises(ValueError, match="checksum"):
        check_bundle(actual_sbom_bundle / "waterbodies.cwl", actual_sbom_bundle)


def test_missing_coverage_is_rejected(actual_sbom_bundle: Path) -> None:
    path = actual_sbom_bundle / "coverage.json"
    coverage = json.loads(path.read_text())
    coverage["tools"].pop()
    path.write_text(json.dumps(coverage))
    with pytest.raises(ValueError, match="coverage"):
        check_bundle(actual_sbom_bundle / "waterbodies.cwl", actual_sbom_bundle)


def test_unsafe_sbom_path_is_rejected(actual_sbom_bundle: Path) -> None:
    path = actual_sbom_bundle / "images.lock.json"
    lock = json.loads(path.read_text())
    lock["images"][0]["sbom"] = "../outside.json"
    path.write_text(json.dumps(lock))
    with pytest.raises(ValueError, match="inside the bundle"):
        check_bundle(actual_sbom_bundle / "waterbodies.cwl", actual_sbom_bundle)


def test_digest_pinned_contract_matches_inspected_identities(actual_sbom_bundle: Path) -> None:
    contract = actual_sbom_bundle / "waterbodies.cwl"
    document = yaml.safe_load(contract.read_text())
    lock = json.loads((actual_sbom_bundle / "images.lock.json").read_text())
    identities = {image["reference"]: image["repository_digests"][0] for image in lock["images"]}
    for process in document["$graph"]:
        if process["class"] == "CommandLineTool":
            docker = process["hints"]["DockerRequirement"]
            docker["dockerPull"] = identities[docker["dockerPull"]]
    contract.write_text(yaml.safe_dump(document))
    check_bundle(contract, actual_sbom_bundle)
