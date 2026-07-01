from __future__ import annotations

from models import PromptData

from core.compressor.context import CompressionContext

from .engine import CompressionEngine


class NoCompressionEngine(CompressionEngine):
    """
    Fallback engine (no-op compression).
    """

    def compress(
        self,
        text: str,
        prompt: PromptData,
        context: CompressionContext | None = None,
    ) -> str:
        return text