from __future__ import annotations

from models import NormalizationContext

from .config import NORMALIZE_NEWLINES
from .normalizer import Normalizer


class NewlineNormalizer(Normalizer):
    """
    Normalize newline characters to LF.
    """

    @property
    def priority(self) -> int:
        return 10

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        if not NORMALIZE_NEWLINES:
            return text

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        return text