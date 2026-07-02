from __future__ import annotations

import re

from models import OptimizationContext

from .optimizer import Optimizer
from .optimizer_type import OptimizerType


class RepetitionOptimizer(Optimizer):
    """
    Removes repeated lines while preserving order.
    """

    @property
    def optimizer_type(
        self,
    ) -> OptimizerType:
        return OptimizerType.REPETITION

    @property
    def priority(self) -> int:
        return 60

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if (
            context.is_structured
            or context.contains_code
        ):
            return text

        if self.is_protected(
            text,
            context,
        ):
            return text

        seen: set[str] = set()

        result: list[str] = []

        for line in text.splitlines():

            normalized = line.strip()

            if not normalized:
                result.append(line)
                continue

            key = re.sub(
                r"\s+",
                " ",
                normalized.casefold(),
            )

            if key in seen:

                if context.is_conservative:
                    result.append(line)

                continue

            seen.add(key)

            result.append(line)

        optimized = "\n".join(result)

        if context.needs_aggressive_optimization:

            optimized = re.sub(
                r"\n{3,}",
                "\n\n",
                optimized,
            )

        return optimized.strip()