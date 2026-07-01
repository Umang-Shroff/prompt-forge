from __future__ import annotations

import re

from models import NormalizationContext

from .config import MAX_CONSECUTIVE_BLANK_LINES
from .normalizer import Normalizer


class BlankLineNormalizer(Normalizer):
    """
    Collapse excessive blank lines.
    """

    @property
    def priority(self) -> int:
        return 60

    def normalize(
        self,
        text: str,
        context: NormalizationContext,
    ) -> str:

        max_blank = MAX_CONSECUTIVE_BLANK_LINES

        pattern = rf"\n{{{max_blank + 2},}}"

        replacement = "\n" * (max_blank + 1)

        return re.sub(
            pattern,
            replacement,
            text,
        )