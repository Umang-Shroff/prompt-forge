from __future__ import annotations

from models import NormalizationContext

from .config import REMOVE_TRAILING_WHITESPACE
from .normalizer import Normalizer


class TrailingSpaceNormalizer(Normalizer):
    """
    Removes trailing whitespace from every line.
    """

    @property
    def priority(self) -> int:
        return 20

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        if not REMOVE_TRAILING_WHITESPACE:
            return text

        return "\n".join(
            line.rstrip()
            for line in text.splitlines()
        )