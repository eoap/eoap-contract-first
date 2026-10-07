import ast
import io
from pathlib import Path

from cwl2click import to_click
from cwl_loader import load_cwl_from_location
from cwl_utils.parser import CommandLineTool, Workflow
from waterbodies.cli import waterbodies

CONTRACT = Path(__file__).parents[2] / "reference/waterbodies.cwl"


def test_contract_resolves_tools_and_scatter() -> None:
    processes = load_cwl_from_location(str(CONTRACT))
    assert isinstance(processes, list)
    workflows = [process for process in processes if isinstance(process, Workflow)]
    tools = [process for process in processes if isinstance(process, CommandLineTool)]
    assert {tool.id for tool in tools} == {"crop", "norm-diff", "otsu", "stac"}
    assert len(workflows) == 1
    assert workflows[0].steps[0].scatter == "crop/band"
    assert {tool.id: tool.baseCommand for tool in tools} == {
        name: ["waterbodies", name] for name in ("crop", "norm-diff", "otsu", "stac")
    }


def test_cli_is_the_upstream_generated_interface() -> None:
    processes = load_cwl_from_location(str(CONTRACT))
    assert isinstance(processes, list)
    tools = [process for process in processes if isinstance(process, CommandLineTool)]
    stream = io.StringIO()
    to_click(tools, "waterbodies", stream, bundle=True)
    committed = CONTRACT.parent / "src/waterbodies/waterbodies.py"

    # Upstream embeds a timestamp and emits tools in loader traversal order.
    # Compare all generated Python statements without depending on that order.
    generated_nodes = sorted(ast.dump(node) for node in ast.parse(stream.getvalue()).body)
    committed_nodes = sorted(ast.dump(node) for node in ast.parse(committed.read_text()).body)
    assert generated_nodes == committed_nodes
    assert set(waterbodies.commands) == {"crop", "norm-diff", "otsu", "stac"}
