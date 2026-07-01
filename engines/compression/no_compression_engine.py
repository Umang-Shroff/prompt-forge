from __future__ import annotations

from core.compressor.context import CompressionContext

from engines.compression.policy import CompressionPolicy

from models import PromptData

from .engine import CompressionEngine


class NoCompressionEngine(CompressionEngine):
    """
    Fallback engine that performs no compression.
    """

    def compress(
        self,
        text: str,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
    ) -> str:

        return text