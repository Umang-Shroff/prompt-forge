from __future__ import annotations

from typing import Iterable

from .detector import Detector


class DetectorRegistry:
    """
    Stores detector instances.

    AnalyzerStage executes them in priority order.
    """

    def __init__(self) -> None:

        self._detectors: list[Detector] = []

    def register(self, detector: Detector) -> None:

        self._detectors.append(detector)

    def extend(
        self,
        detectors: Iterable[Detector],
    ) -> None:

        self._detectors.extend(detectors)

    def clear(self) -> None:

        self._detectors.clear()

    @property
    def detectors(self) -> tuple[Detector, ...]:

        enabled = (
            detector
            for detector in self._detectors
            if detector.enabled
        )

        return tuple(
            sorted(
                enabled,
                key=lambda detector: detector.priority,
            )
        )