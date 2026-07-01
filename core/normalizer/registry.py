from __future__ import annotations

from typing import Iterable

from .normalizer import Normalizer


class NormalizerRegistry:
    """
    Stores normalizer instances.
    """

    def __init__(self) -> None:
        self._normalizers: list[Normalizer] = []

    def register(
        self,
        normalizer: Normalizer,
    ) -> None:

        self._normalizers.append(normalizer)

    def extend(
        self,
        normalizers: Iterable[Normalizer],
    ) -> None:

        self._normalizers.extend(normalizers)

    def clear(self) -> None:

        self._normalizers.clear()

    @property
    def normalizers(
        self,
    ) -> tuple[Normalizer, ...]:

        enabled = (
            normalizer
            for normalizer in self._normalizers
            if normalizer.enabled
        )

        return tuple(
            sorted(
                enabled,
                key=lambda n: n.priority,
            )
        )