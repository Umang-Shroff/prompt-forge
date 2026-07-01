from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .default_registry import create_default_registry
from .registry import DetectorRegistry


class AnalyzerStage(Stage):
    """
    Executes all registered detectors.
    """

    def __init__(
        self,
        registry: DetectorRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        for detector in self._registry.detectors:

            detector.detect(prompt)

        return prompt