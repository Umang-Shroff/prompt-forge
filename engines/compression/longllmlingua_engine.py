from __future__ import annotations

from typing import List

from models import PromptData

from core.compressor.context import CompressionContext

from .engine import CompressionEngine
from .chunker import PromptChunker
from .scorer import ImportanceScorer


class LongLLMLinguaEngine(CompressionEngine):
    """
    Budget-aware LongLLMLingua wrapper (structured compression).
    """

    def __init__(self, model=None):
        self.model = model  # placeholder for real LLMLingua model
        self.chunker = PromptChunker()
        self.scorer = ImportanceScorer()

    def compress(
        self,
        text: str,
        prompt: PromptData,
        context: CompressionContext | None = None,
    ) -> str:

        chunks = self.chunker.chunk(text)

        if not chunks:
            return text

        # -----------------------------
        # Step 1: score chunks
        # -----------------------------
        scored: List[tuple[str, float]] = []

        for c in chunks:
            score = self.scorer.score(c)
            scored.append((c, score))

        # -----------------------------
        # Step 2: determine keep ratio
        # -----------------------------
        keep_ratio = 0.8

        if context:
            if context.high_pressure:
                keep_ratio = 0.4
            elif context.is_balanced:
                keep_ratio = 0.6
            else:
                keep_ratio = 0.8

        # -----------------------------
        # Step 3: select top chunks
        # -----------------------------
        scored.sort(key=lambda x: x[1], reverse=True)

        keep_count = max(1, int(len(scored) * keep_ratio))

        selected = [c for c, _ in scored[:keep_count]]

        # -----------------------------
        # Step 4: reconstruct prompt
        # -----------------------------
        return "\n\n".join(selected)