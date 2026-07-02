from __future__ import annotations

from typing import Iterable

from .detector import IntentDetector


class IntentRegistry:
    """
    Stores registered intent detectors.
    """

    def __init__(self) -> None:

        self._detectors: list[IntentDetector] = []

    def register(
        self,
        detector: IntentDetector,
    ) -> None:

        self._detectors.append(detector)

    def extend(
        self,
        detectors: Iterable[IntentDetector],
    ) -> None:

        self._detectors.extend(detectors)

    def clear(self) -> None:

        self._detectors.clear()

    @property
    def detectors(
        self,
    ) -> tuple[IntentDetector, ...]:

        return tuple(self._detectors)