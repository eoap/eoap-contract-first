from pathlib import Path

ROOT = Path(__file__).parents[2]

EXPECTED_MODULE_COUNT = 14


def test_every_module_provides_a_complete_learning_step() -> None:
    modules = sorted((ROOT / "modules").iterdir())
    assert len(modules) == EXPECTED_MODULE_COUNT
    for module in modules:
        for filename in ("README.md", "lesson.md", "exercise.md", "solution.md"):
            assert (module / filename).is_file()
        lesson = (module / "lesson.md").read_text()
        assert "What are we designing?" in lesson
        assert "Why does it belong in the contract?" in lesson
        assert "What can be derived?" in lesson
        assert "How do we verify it?" in lesson
        exercise = (module / "exercise.md").read_text()
        assert "Expected outcome:" in exercise
        assert "```console" in exercise
