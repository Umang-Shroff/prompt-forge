from __future__ import annotations

from dataclasses import dataclass

from core.compressor.context import CompressionContext

from models import PromptData

from .compression_profile import CompressionProfile
from .policy import CompressionPolicy


@dataclass(slots=True)
class CompressionRequestBuilder:
    """
    Builds the keyword arguments required by LLMLingua.

    The rest of the application never needs to know
    the exact PromptCompressor API.
    """

    def _compute_rate(
        self,
        prompt: PromptData,
        profile: CompressionProfile,
    ) -> float:
        """
        Computes an adaptive LLMLingua compression rate.

        Higher values preserve more information.
        Lower values compress more aggressively.
        """

        rate = profile.target_ratio

        quality = prompt.quality.overall

        # ----------------------------------------
        # Quality adjustment
        # ----------------------------------------

        if quality >= 90:
            rate += 0.10

        elif quality >= 80:
            rate += 0.05

        elif quality <= 60:
            rate -= 0.10

        elif quality <= 70:
            rate -= 0.05

        # ----------------------------------------
        # Mode adjustment
        # ----------------------------------------

        mode = prompt.mode.name

        if mode == "CONSERVATIVE":
            rate += 0.10

        elif mode == "AGGRESSIVE":
            rate -= 0.10

        # ----------------------------------------
        # Prompt characteristics
        # ----------------------------------------

        if profile.preserve_code:
            rate += 0.05

        if profile.preserve_structure:
            rate += 0.05

        if profile.preserve_lists:
            rate += 0.03

        # ----------------------------------------
        # Clamp
        # ----------------------------------------

        return max(
            0.30,
            min(
                rate,
                0.95,
            ),
        )

    def build(
        self,
        prompt: PromptData,
        policy: CompressionPolicy,
        profile: CompressionProfile,
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
            int(original_tokens * profile.target_ratio),
        )

        rate = self._compute_rate(
            prompt,
            profile,
        )
    
        use_context_filter = True
        use_token_filter = True
        use_sentence_filter = False

        if profile.preserve_code:
            use_sentence_filter = False

        elif profile.preserve_reasoning:
            use_sentence_filter = True

        elif profile.aggressive_filtering:
            use_sentence_filter = True

        reorder_context = profile.reorder_context

        if profile.preserve_roles:
            reorder_context = "original"

        elif profile.aggressive_filtering:
            reorder_context = "sort"

        kwargs = {
            "context": chunks,
            "instruction": "",
            "question": "",
            "rate": rate,
            "target_token": target_tokens,
            "context_budget": policy.context_budget,
            "token_budget_ratio": policy.token_budget_ratio,
            "use_context_level_filter": use_context_filter,
            "use_token_level_filter": use_token_filter,
            "use_sentence_level_filter": use_sentence_filter,
            "reorder_context": reorder_context,
            "strict_preserve_uncompressed": True,
        }
    
        # -----------------------------------------
        # Tell LLMLingua which chunks may compress
        # -----------------------------------------
    
        if compress_flags is not None:
        
            kwargs["context_segs"] = chunks
            kwargs["context_segs_compress"] = compress_flags
    
        # -----------------------------------------
        # Chunk importance
        # -----------------------------------------
    
        if scores is not None:
        
            rates = []

            for score in scores:
            
                if profile.aggressive_filtering:
                    score *= 0.90

                elif profile.preserve_reasoning:
                    score *= 1.10

                elif profile.preserve_roles:
                    score *= 1.10

                rates.append(
                    max(
                        0.10,
                        min(score, 1.0),
                    )
                )

            kwargs["context_segs_rate"] = rates
    
        # -----------------------------------------
        # Force preservation
        # -----------------------------------------
    
        if profile.force_tokens:
        
            kwargs["force_tokens"] = profile.force_tokens
    
        return kwargs