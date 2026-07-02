from __future__ import annotations

from typing import TYPE_CHECKING

from .engine import CompressionEngine

if TYPE_CHECKING:
    from models import PromptData
    from core.compressor.context import CompressionContext
    from engines.compression.policy import CompressionPolicy


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