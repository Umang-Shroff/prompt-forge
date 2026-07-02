from __future__ import annotations

from core.analyzer import AnalyzerStage
from core.compressor import CompressorStage
from core.intent import IntentStage
from core.normalizer import NormalizerStage
from core.optimizer import OptimizerStage
from core.pipeline import Pipeline
from core.quality import QualityStage
from core.reconstructor import ReconstructorStage
from core.tokenizer.token_stage import TokenCounterStage


def create_default_pipeline() -> Pipeline:
    """
    Create the default PromptForge optimization pipeline.
    """

    return Pipeline(
        [
            AnalyzerStage(),
            NormalizerStage(),
            IntentStage(),
            QualityStage(),
            OptimizerStage(),
            ReconstructorStage(),
            TokenCounterStage(),
            CompressorStage(),
            TokenCounterStage(),
        ]
    )