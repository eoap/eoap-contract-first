import ast
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
LABS = ROOT / "practice-labs"
EXPECTED_LAB_COUNT = 14
NOTEBOOK_FORMAT_VERSION = 4


def test_every_module_has_a_linked_bash_practice_lab() -> None:
    modules = tuple(sorted((ROOT / "modules").iterdir()))
    assert len(modules) == EXPECTED_LAB_COUNT
    assert {path.stem for path in LABS.glob("[0-9][0-9]-*.ipynb")} == {
        module.name for module in modules
    }
    for module in modules:
        notebook = json.loads((LABS / f"{module.name}.ipynb").read_text())
        assert notebook["metadata"]["kernelspec"]["name"] == "bash"
        assert notebook["metadata"]["language_info"]["name"] == "bash"
        for filename in ("README.md", "exercise.md"):
            assert f"../../practice-labs/{module.name}.ipynb" in (module / filename).read_text()
        markdown = "\n".join(
            "".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown"
        )
        assert "Expected outcome:" in markdown
        assert "Record your findings" in markdown


@pytest.mark.parametrize("notebook_path", tuple(sorted(LABS.glob("*.ipynb"))))
def test_notebook_cells_have_valid_syntax_and_no_saved_outputs(notebook_path: Path) -> None:
    notebook = json.loads(notebook_path.read_text())
    assert notebook["nbformat"] == NOTEBOOK_FORMAT_VERSION
    cell_ids = [cell["id"] for cell in notebook["cells"]]
    assert len(set(cell_ids)) == len(cell_ids)
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        assert cell["outputs"] == []
        assert cell["execution_count"] is None
        source = "".join(cell["source"])
        if notebook["metadata"]["kernelspec"]["language"] == "python":
            ast.parse(source)
            continue
        checked = subprocess.run(
            ["bash", "-n"], input=source, capture_output=True, text=True, check=False, timeout=10
        )
        assert checked.returncode == 0, checked.stderr
        for section in source.split("<<'PYTHON'\n")[1:]:
            ast.parse(section.split("\nPYTHON")[0])
