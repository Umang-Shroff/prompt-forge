from __future__ import annotations

from typing import Iterable

from .detector import ChunkImportanceDetector


class ImportanceRegistry:

    def __init__(
        self,
    ) -> None:

        self._detectors: list[
            ChunkImportanceDetector
        ] = []

    def register(
        self,
        detector: ChunkImportanceDetector,
    ) -> None:

        self._detectors.append(
            detector,
        )

    def extend(
        self,
        detectors: Iterable[
            ChunkImportanceDetector
        ],
    ) -> None:

        self._detectors.extend(
            detectors,
        )

    @property
    def detectors(
        self,
    ) -> tuple[
        ChunkImportanceDetector,
        ...
    ]:

        return tuple(
            self._detectors,
        )