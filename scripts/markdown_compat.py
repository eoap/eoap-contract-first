"""Run upstream cwl2markdown with its verified template filename regression repaired.

Revision 17ea06d ships *.md.jinja but requests *.md. This adapter resolves only
those filenames; rendering remains entirely in the upstream plugin.
"""

from collections.abc import Callable

import cwl2markdown.plugin as markdown_plugin
from jinja2 import Environment, PackageLoader
from transpiler_mate.runtime.cli import main


class TemplateSuffixLoader(PackageLoader):
    """Resolve the upstream plugin's .md requests to its shipped .md.jinja files."""

    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str, Callable[[], bool] | None]:
        """Load the unmodified upstream template under its actual filename."""
        name = template + ".jinja" if template.endswith(".md") else template
        return super().get_source(environment, name)


if __name__ == "__main__":
    vars(markdown_plugin)["PackageLoader"] = TemplateSuffixLoader
    main()
