from __future__ import annotations

import re

from .reconstructor import Reconstructor


class SentenceReconstructor(Reconstructor):
    """
    Restores basic sentence readability after optimization.
    """

    @property
    def priority(self) -> int:
        return 10

    def reconstruct(
        self,
        text: str,
    ) -> str:

        # Collapse excessive spaces
        text = re.sub(r" {2,}", " ", text)

        # Remove spaces before punctuation
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)

        # Ensure one space after punctuation
        text = re.sub(r"([.,;:!?])([^\s])", r"\1 \2", text)

        # Collapse blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()