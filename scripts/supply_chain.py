"""Check release identities and the integrity of real cwl2sbom evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml

EXPECTED_TOOL_COUNT = 4

SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
DIGEST = re.compile(r"[^@\s]+@sha256:[0-9a-f]{64}")


def container_references(contract: Path) -> set[str]:
    """Return versioned image references from the canonical graph.

    Raises:
        ValueError: If a tool has no image or an image has no immutable/release identity.
    """
    document = yaml.safe_load(contract.read_text())
    references: set[str] = set()
    for process in document["$graph"]:
        if process["class"] != "CommandLineTool":
            continue
        reference = process.get("hints", {}).get("DockerRequirement", {}).get("dockerPull")
        if not isinstance(reference, str):
            raise ValueError(f"Missing container for {process['id']}")
        if not DIGEST.fullmatch(reference) and not SEMVER.fullmatch(reference.rsplit(":", 1)[-1]):
            raise ValueError(f"Image must use SemVer or SHA256 digest: {reference}")
        references.add(reference)
    if len(references) != EXPECTED_TOOL_COUNT:
        raise ValueError("The reference requires four distinct processing images")
    return references


def check_bundle(contract: Path, directory: Path) -> None:
    """Verify complete coverage, image identities and image SBOM checksums.

    This verifies inventory integrity, not vulnerability policy or signatures.

    Raises:
        ValueError: If evidence is incomplete, mismatched or corrupted.
    """
    expected = container_references(contract)
    coverage = json.loads((directory / "coverage.json").read_text())
    lock = json.loads((directory / "images.lock.json").read_text())
    workflow = json.loads((directory / "workflow.cdx.json").read_text())
    covered = {tool.get("image") for tool in coverage["tools"]}
    inspected = {image["reference"] for image in lock["images"]}
    digests = {
        image["repository_digests"][0] for image in lock["images"] if image["repository_digests"]
    }
    if (
        coverage["complete"] is not True
        or len(coverage["tools"]) != EXPECTED_TOOL_COUNT
        or len(lock["images"]) != EXPECTED_TOOL_COUNT
        or any(tool["status"] != "declared" for tool in coverage["tools"])
        or any(image["platform"] != lock["platform"] for image in lock["images"])
        or covered != inspected
        or expected not in (inspected, digests)
    ):
        raise ValueError("SBOM coverage must match all four declared containers")
    if workflow["bomFormat"] != "CycloneDX":
        raise ValueError("Workflow inventory must be CycloneDX")
    for image in lock["images"]:
        relative = Path(image["sbom"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Image SBOM must stay inside the bundle")
        checksum = hashlib.sha256((directory / relative).read_bytes()).hexdigest()
        if checksum != image["sbom_sha256"]:
            raise ValueError("Image SBOM checksum does not match lock")
        if not image["repository_digests"] or not all(
            DIGEST.fullmatch(digest) for digest in image["repository_digests"]
        ):
            raise ValueError("Inspected images must report immutable identities")


def _inspected_identities(lock_path: Path) -> dict[str, str]:
    """Read the primary immutable identity for each inspected image.

    Raises:
        ValueError: If a lock reference or repository digest is invalid.
    """
    lock = json.loads(lock_path.read_text())
    identities: dict[str, str] = {}
    for image in lock["images"]:
        reference = image["reference"]
        digest = next(iter(image["repository_digests"]), None)
        if not isinstance(reference, str) or not isinstance(digest, str):
            raise ValueError("Lock must report a reference and repository digest")
        if DIGEST.fullmatch(digest) is None:
            raise ValueError("Inspected image identity must be a SHA256 repository digest")
        identities[reference] = digest
    return identities


def prepare_release(contract: Path, output: Path, version: str, lock_path: Path | None) -> None:
    """Write a release contract with coherent version tags or inspected digests.

    Args:
        contract: Source contract; never modified in place.
        output: Destination for the reviewable release CWL.
        version: Application SemVer release identity.
        lock_path: cwl2sbom lock for pinning the four already published images.

    Raises:
        ValueError: If the version or inspected image identity is invalid.
    """
    if SEMVER.fullmatch(version) is None:
        raise ValueError("VERSION must be x.y.z SemVer")
    document = yaml.safe_load(contract.read_text())
    document["s:softwareVersion"] = version
    identities = _inspected_identities(lock_path) if lock_path is not None else {}
    for process in document["$graph"]:
        if process["class"] == "CommandLineTool":
            docker = process["hints"]["DockerRequirement"]
            reference = f"ghcr.io/eoap/waterbodies-{process['id']}:{version}"
            if lock_path is not None and reference not in identities:
                raise ValueError(f"Lock has no inspected identity for {reference}")
            docker["dockerPull"] = identities[reference] if lock_path is not None else reference
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(document, sort_keys=False))


def main() -> None:
    """Run the local inventory, evidence or release preparation operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["inventory", "check", "prepare"])
    parser.add_argument("--contract", type=Path, default=Path("reference/waterbodies.cwl"))
    parser.add_argument("--bundle", type=Path, default=Path("build/sbom"))
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--output", type=Path, default=Path("build/release/waterbodies.cwl"))
    parser.add_argument("--lock", type=Path)
    options = parser.parse_args()
    if options.operation == "inventory":
        print("\n".join(sorted(container_references(options.contract))))
    elif options.operation == "check":
        check_bundle(options.contract, options.bundle)
    else:
        prepare_release(options.contract, options.output, options.version, options.lock)


if __name__ == "__main__":
    main()
