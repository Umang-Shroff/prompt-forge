from __future__ import annotations

from models import NormalizationContext

from .config import NORMALIZE_UNICODE
from .normalizer import Normalizer


UNICODE_REPLACEMENTS = {
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "–": "-",
    "—": "-",
    "…": "...",
    "\u00A0": " ",
}


class UnicodeNormalizer(Normalizer):
    """
    Replace common Unicode punctuation with ASCII equivalents.
    """

    @property
    def priority(self) -> int:
        return 30

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        if not NORMALIZE_UNICODE:
            return text

        for old, new in UNICODE_REPLACEMENTS.items():
            text = text.replace(old, new)

        return text