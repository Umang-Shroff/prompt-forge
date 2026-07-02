from __future__ import annotations

from models import PromptData

from .rules import score_chunk


class ImportanceScorer:
    """
    Computes importance scores for prompt chunks.
    """

    def score(
        self,
        chunks: list[str],
        prompt: PromptData,
    ) -> list[float]:

        total_chunks = max(
            1,
            len(chunks),
        )

        return [
            score_chunk(
                chunk=chunk,
                index=index,
                total_chunks=total_chunks,
                prompt=prompt,
            )
            for index, chunk in enumerate(chunks)
        ]