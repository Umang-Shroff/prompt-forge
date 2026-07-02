from __future__ import annotations

from .reconstructor import Reconstructor


class CodeBlockReconstructor(Reconstructor):
    """
    Normalizes fenced code blocks.
    """

    @property
    def priority(self) -> int:
        return 40

    def reconstruct(
        self,
        text: str,
    ) -> str:

        lines = text.splitlines()

        result: list[str] = []

        inside_block = False

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("```"):

                if result and result[-1] != "":
                    result.append("")

                result.append(stripped)

                inside_block = not inside_block

                continue

            if inside_block:

                result.append(line.rstrip())

            else:

                result.append(line.rstrip())

        return "\n".join(result)