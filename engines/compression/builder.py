from __future__ import annotations

from dataclasses import dataclass

from core.compressor.context import CompressionContext

from models import PromptData

from .policy import CompressionPolicy


@dataclass(slots=True)
class CompressionRequestBuilder:
    """
    Builds the keyword arguments required by LLMLingua.

    The rest of the application never needs to know
    the exact PromptCompressor API.
    """

    def build(
        self,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
        chunks: list[str],
        compress_flags: list[bool] | None = None,
        scores: list[float] | None = None,
    ) -> dict:

        original_tokens = max(
            1,
            prompt.tokens.original_tokens,
        )

        target_tokens = max(
            1,
            int(original_tokens * policy.target_ratio),
        )

        kwargs = {
            "context": chunks,
            "instruction": "",
            "question": "",
            "target_token": target_tokens,
            "context_budget": policy.context_budget,
            "token_budget_ratio": policy.token_budget_ratio,
            "use_context_level_filter": True,
            "use_token_level_filter": True,
            "use_sentence_level_filter": False,
            "reorder_context": "original",
            "strict_preserve_uncompressed": True,
        }

        if compress_flags is not None:

            kwargs["context_segs"] = chunks
            kwargs["context_segs_compress"] = compress_flags

        if scores is not None:

            kwargs["context_segs"] = chunks

            kwargs["context_segs_rate"] = [
                max(
                    0.10,
                    min(score, 1.0),
                )
                for score in scores
            ]

        return kwargs