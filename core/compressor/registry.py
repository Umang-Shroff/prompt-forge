from __future__ import annotations

from typing import Iterable

from engines.compression.engine import CompressionEngine


class CompressionRegistry:
    """
    Stores compression engines.
    """

    def __init__(self) -> None:
        self._engines: list[CompressionEngine] = []

    def register(self, engine: CompressionEngine) -> None:
        self._engines.append(engine)

    def extend(self, engines: Iterable[CompressionEngine]) -> None:
        self._engines.extend(engines)

    def clear(self) -> None:
        self._engines.clear()

    @property
    def engines(self) -> tuple[CompressionEngine, ...]:
        return tuple(self._engines)