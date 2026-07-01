from __future__ import annotations

from PromptOptimizer.core.compressor.budget import CompressionBudget
from core.stage import Stage

from models import PromptData

from .context import CompressionContext
from .registry import CompressionRegistry

from engines.compression.no_compression_engine import NoCompressionEngine


class CompressorStage(Stage):
    """
    Executes compression engines sequentially.
    """

    def __init__(
        self,
        registry: CompressionRegistry | None = None,
    ) -> None:

        self._registry = registry or CompressionRegistry()

        # fallback engine
        if not self._registry.engines:
            self._registry.register(NoCompressionEngine())

    def execute(self, prompt: PromptData) -> PromptData:

        # -----------------------------
        # Build token-aware budget
        # -----------------------------
    
        original_tokens = prompt.tokens.original_tokens
    
        # target based on mode
        if prompt.mode.name == "AGGRESSIVE":
            target_tokens = int(original_tokens * 0.4)
        elif prompt.mode.name == "BALANCED":
            target_tokens = int(original_tokens * 0.6)
        else:
            target_tokens = int(original_tokens * 0.8)
    
        budget = CompressionBudget(
            original_tokens=original_tokens,
            target_tokens=target_tokens,
        )
    
        context = CompressionContext(
            mode=prompt.mode,
            analysis=prompt.analysis,
            budget=budget,
        )
    
        text = prompt.current_prompt
    
        active_engine = None
    
        for engine in self._registry.engines:
        
            active_engine = engine
    
            # Pass budget-aware context to engine
            text = engine.compress(text, prompt)
    
        prompt.current_prompt = text
    
        prompt.compression.success = True
    
        prompt.compression.engine = (
            active_engine.name
            if active_engine is not None
            else "None"
        )
    
        return prompt