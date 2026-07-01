from __future__ import annotations

from models import OptimizationContext

from .optimizer import Optimizer


class RepetitionOptimizer(Optimizer):
    """
    Removes repeated lines while preserving order.
    """

    @property
    def priority(self) -> int:
        return 60

    def optimize(
        self,
        text: str,
        context: OptimizationContext,
    ) -> str:

        if context.is_code:
            return text

        seen: set[str] = set()

        result: list[str] = []

        for line in text.splitlines():

            normalized = line.strip()

            if not normalized:

                result.append(line)

                continue

            key = normalized.casefold()

            if key in seen:
                continue

            seen.add(key)

            result.append(line)

        return "\n".join(result)