from __future__ import annotations

import re

from .reconstructor import Reconstructor


class ListReconstructor(Reconstructor):
    """
    Normalizes markdown and numbered lists.
    """

    @property
    def priority(self) -> int:
        return 20

    def reconstruct(
        self,
        text: str,
    ) -> str:

        lines = []

        for line in text.splitlines():

            line = re.sub(
                r"^\s*[-*+]\s*",
                "- ",
                line,
            )

            line = re.sub(
                r"^\s*(\d+)[.)]\s*",
                r"\1. ",
                line,
            )

            lines.append(
                line.rstrip(),
            )

        return "\n".join(lines)