from __future__ import annotations

from core.pipeline import Pipeline
from core.pipeline_builder import create_default_pipeline

from models import (
    OptimizationMode,
    PromptData,
)


class PromptOptimizer:
    """
    Public optimization API for PromptForge.

    This class provides a simple interface to the complete
    optimization pipeline without exposing its internal stages.
    """

    def __init__(
        self,
        pipeline: Pipeline | None = None,
    ) -> None:

        self._pipeline = pipeline or create_default_pipeline()

    def optimize(
        self,
        prompt: str,
        mode: OptimizationMode = OptimizationMode.BALANCED,
    ) -> PromptData:
        """
        Optimize a prompt.

        Parameters
        ----------
        prompt:
            The user's original prompt.

        mode:
            Desired optimization mode.

        Returns
        -------
        PromptData
            Fully populated optimization result.
        """

        prompt_data = PromptData(
            original_prompt=prompt,
            mode=mode,
        )

        return self._pipeline.run(prompt_data)