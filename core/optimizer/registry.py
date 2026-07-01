from __future__ import annotations

from typing import Iterable

from .optimizer import Optimizer


class OptimizerRegistry:
    """
    Stores optimizer instances.
    """

    def __init__(self) -> None:
        self._optimizers: list[Optimizer] = []

    def register(
        self,
        optimizer: Optimizer,
    ) -> None:

        self._optimizers.append(optimizer)

    def extend(
        self,
        optimizers: Iterable[Optimizer],
    ) -> None:

        self._optimizers.extend(optimizers)

    def clear(self) -> None:

        self._optimizers.clear()

    @property
    def optimizers(
        self,
    ) -> tuple[Optimizer, ...]:

        enabled = (
            optimizer
            for optimizer in self._optimizers
            if optimizer.enabled
        )

        return tuple(
            sorted(
                enabled,
                key=lambda o: o.priority,
            )
        )