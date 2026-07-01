from __future__ import annotations

from core.stage import Stage
from core.compressor.budget import CompressionBudget
from core.compressor.context import CompressionContext
from core.compressor.registry import CompressionRegistry
from .default_registry import create_default_registry
from engines.compression.no_compression_engine import NoCompressionEngine
from engines.compression.policy import PolicyFactory

from models import (
    OptimizationMode,
    PromptData,
)


class CompressorStage(Stage):
    """
    Executes the registered compression engines.

    Responsibilities
    ----------------
    • Build the compression budget.
    • Build the compression context.
    • Create the compression policy.
    • Execute compression engines.
    • Store compression metadata.
    """

    def __init__(
        self,
        registry: CompressionRegistry | None = None,
    ) -> None:

        self._registry = registry or create_default_registry()

        if not self._registry.engines:
            self._registry.register(
                NoCompressionEngine()
            )

    def execute(
        self,
        prompt: PromptData,
    ) -> PromptData:

        # ----------------------------------
        # Build compression budget
        # ----------------------------------
            

        original_tokens = prompt.tokens.original_tokens

        if prompt.mode == OptimizationMode.AGGRESSIVE:
            target_tokens = int(original_tokens * 0.35)

        elif prompt.mode == OptimizationMode.BALANCED:
            target_tokens = int(original_tokens * 0.60)

        else:
            target_tokens = int(original_tokens * 0.80)

        budget = CompressionBudget(
            original_tokens=original_tokens,
            target_tokens=target_tokens,
        )

        # ----------------------------------
        # Build compression context
        # ----------------------------------

        context = CompressionContext(
            mode=prompt.mode,
            analysis=prompt.analysis,
            budget=budget,
        )

        # ----------------------------------
        # Compression policy
        # ----------------------------------

        policy = PolicyFactory.create(
            prompt.mode,
        )

        # ----------------------------------
        # Execute engines
        # ----------------------------------

        text = prompt.current_prompt

        active_engine = None

        for engine in self._registry.engines:
            print("\nRegistered compression engines:")

            for e in self._registry.engines:
                print(" -", e.__class__.__name__)

            active_engine = engine

            text = engine.compress(
                text=text,
                prompt=prompt,
                context=context,
                policy=policy,
            )

        # ----------------------------------
        # Store results
        # ----------------------------------

        prompt.current_prompt = text

        prompt.compression.success = True

        prompt.compression.engine = (
            active_engine.name
            if active_engine is not None
            else "None"
        )

        return prompt