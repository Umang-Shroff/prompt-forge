from __future__ import annotations

from PromptOptimizer.core.normalizer import normalizer
from core.stage import Stage

from models import PromptData
from models import NormalizationContext
from .default_registry import create_default_registry
from .registry import NormalizerRegistry


class NormalizerStage(Stage):
    """
    Executes all registered normalizers.
    """

    def __init__(
        self,
        registry: NormalizerRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        text = prompt.current_prompt

        context = NormalizationContext(
            mode=prompt.mode,
            analysis=prompt.analysis,
        )

        for normalizer in self._registry.normalizers:

            previous = text
        
            text = normalizer.normalize(
                text,
                context,
            )
        
            if text != previous:
            
                prompt.normalization.mark_applied(
                    normalizer.name,
                )
        
            else:
            
                prompt.normalization.mark_skipped(
                    normalizer.name,
                )

        prompt.current_prompt = text

        return prompt