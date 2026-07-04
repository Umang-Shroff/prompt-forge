from __future__ import annotations

from core.stage import Stage

from models import PromptData

from .default_registry import create_default_registry
from .registry import DetectorRegistry
from core.region_classifier import RegionClassifier


class AnalyzerStage(Stage):
    """
    Executes all registered detectors.
    """

    def __init__(
        self,
        registry: DetectorRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()
        self._classifier = RegionClassifier()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        for detector in self._registry.detectors:

            detector.detect(prompt)
        
        prompt.regions = self._classifier.classify(
            prompt.current_prompt,
        )
        
        return prompt