from __future__ import annotations

from typing import Iterable

from .strategy import IntentOptimizationStrategy


class StrategyRegistry:

    def __init__(self) -> None:

        self._strategies: list[IntentOptimizationStrategy] = []

    def register(
        self,
        strategy: IntentOptimizationStrategy,
    ) -> None:

        self._strategies.append(strategy)

    def extend(
        self,
        strategies: Iterable[IntentOptimizationStrategy],
    ) -> None:

        self._strategies.extend(strategies)

    @property
    def strategies(
        self,
    ) -> tuple[IntentOptimizationStrategy, ...]:

        return tuple(self._strategies)