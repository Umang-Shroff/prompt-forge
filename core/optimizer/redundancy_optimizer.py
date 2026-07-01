from __future__ import annotations

import re

from models import OptimizationContext

from .optimizer import Optimizer
from .patterns import REDUNDANT_WORD_PATTERN


class RedundancyOptimizer(Optimizer):
    """
    Removes immediately repeated words.
    """

    @property
    def priority(self) -> int:
        return 50

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_code:
            return text

        return re.sub(
            REDUNDANT_WORD_PATTERN,
            r"\1",
            text,
            flags=re.IGNORECASE,
        )