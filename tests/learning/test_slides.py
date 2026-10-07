"""Keep runnable instructor examples aligned with the canonical application."""

import re
import shlex
from pathlib import Path

import yaml
from click.testing import CliRunner
from cwl_loader import load_cwl_from_location
from cwl_utils.parser import CommandLineTool
from waterbodies.cli import waterbodies

ROOT = Path(__file__).parents[2]
DECK = ROOT / "slides/teacher-deck.md"


def test_slide_task_commands_exist() -> None:
    taskfile = yaml.safe_load((ROOT / "Taskfile.yaml").read_text())
    commands = re.findall(r"\btask ([a-z][a-z0-9-]*:[a-z0-9:-]+)", DECK.read_text())
    assert commands
    assert set(commands) <= set(taskfile["tasks"])


def test_slide_cli_options_match_generated_commands() -> None:
    blocks = re.findall(r"```console\n(.*?)\n```", DECK.read_text(), re.DOTALL)
    for block in blocks:
        for line in block.replace("\\\n", " ").splitlines():
            arguments = shlex.split(line)
            if arguments[:2] == ["uv", "run"]:
                arguments = arguments[2:]
            if not arguments or arguments[0] != "waterbodies":
                continue
            subcommand = arguments[1]
            help_arguments = [] if subcommand == "--help" else [subcommand]
            result = CliRunner().invoke(waterbodies, [*help_arguments, "--help"])
            assert result.exit_code == 0, result.output
            for option in arguments[2:]:
                if option.startswith("--"):
                    assert option in result.output


def test_slide_images_match_the_canonical_contract() -> None:
    contract = (ROOT / "reference/waterbodies.cwl").read_text()
    images = set(re.findall(r"ghcr\.io/eoap/waterbodies-[a-z-]+:[0-9.]+", DECK.read_text()))
    assert images
    for image in images:
        assert image in contract


def test_slide_cwl_tool_snippets_resolve() -> None:
    processes = load_cwl_from_location(str(ROOT / "reference/waterbodies.cwl"))
    assert isinstance(processes, list)
    tools = {process.id: process for process in processes if isinstance(process, CommandLineTool)}
    blocks = re.findall(r"```yaml\n(.*?)\n```", DECK.read_text(), re.DOTALL)
    for block in blocks:
        snippet = yaml.safe_load(block)
        if "id" in snippet:
            assert snippet["baseCommand"] == tools[snippet["id"]].baseCommand
        for step in (snippet.get("steps", {}) | {"crop": snippet.get("crop", {})}).values():
            if "run" in step:
                assert step["run"].removeprefix("#") in tools


def test_slide_workflow_wiring_matches_the_canonical_contract() -> None:
    contract = yaml.safe_load((ROOT / "reference/waterbodies.cwl").read_text())
    workflow = next(process for process in contract["$graph"] if process["class"] == "Workflow")
    blocks = re.findall(r"```yaml\n(.*?)\n```", DECK.read_text(), re.DOTALL)
    for block in blocks:
        snippet = yaml.safe_load(block)
        for property_name in ("steps", "outputs"):
            if property_name in snippet:
                for port_name, declaration in snippet[property_name].items():
                    assert declaration == workflow[property_name][port_name]
        if "crop" in snippet:
            assert snippet["crop"] == workflow["steps"]["crop"]
