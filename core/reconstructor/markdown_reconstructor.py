from __future__ import annotations

import re

from .reconstructor import Reconstructor


class MarkdownReconstructor(Reconstructor):
    """
    Normalizes common Markdown formatting.
    """

    @property
    def priority(self) -> int:
        return 30

    def reconstruct(
        self,
        text: str,
    ) -> str:

        lines: list[str] = []

        for line in text.splitlines():

            # Normalize headings
            line = re.sub(
                r"^(#{1,6})(\S)",
                r"\1 \2",
                line,
            )

            # Normalize blockquotes
            line = re.sub(
                r"^>\s*",
                "> ",
                line,
            )

            # Normalize horizontal rules
            if re.fullmatch(
                r"[-*_]{3,}",
                line.strip(),
            ):
                line = "---"

            lines.append(line)

        return "\n".join(lines)