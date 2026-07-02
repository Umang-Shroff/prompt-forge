from __future__ import annotations

from typing import Any

from .compression_profile import CompressionProfile
from core.compressor.context import CompressionContext
from .profile_builder import CompressionProfileBuilder
from models import (
    CompressionConfig,
    PromptData,
)
from .importance import (
    ImportanceScorer,
    reorder_chunks,
)
from .builder import CompressionRequestBuilder
from .chunker import PromptChunker
from .engine import CompressionEngine
from .extractor import CompressionResultExtractor
from .loader import CompressorLoader
from .compressor_cache import CompressorCache
from .policy import CompressionPolicy


class LongLLMLinguaEngine(CompressionEngine):
    """
    Production implementation of Microsoft's LongLLMLingua.

    Responsibilities
    ----------------
    • Lazy-load LLMLingua
    • Chunk the prompt
    • Build LLMLingua request
    • Execute compression
    • Extract compressed text
    • Update PromptData
    """

    def __init__(
        self,
        config: CompressionConfig | None = None,
    ) -> None:

        self._config = config or CompressionConfig()

        self._builder = CompressionRequestBuilder()

        self._extractor = CompressionResultExtractor()

        self._chunker = PromptChunker()

        self._profile_builder = CompressionProfileBuilder()

        # Lazy initialization.
        self._compressor: Any | None = None

        self._importance_scorer = ImportanceScorer()

    def _load_compressor(self) -> Any:
        """
        Lazily retrieve the shared PromptCompressor instance.
        """
    
        if self._compressor is None:
        
            self._compressor = CompressorCache.get(
                self._config,
            )
    
        return self._compressor
    

    def _update_statistics(
        self,
        prompt: PromptData,
        compressed_text: str,
    ) -> None:
        """
        Update token statistics after compression.

        Currently we use a simple whitespace-based estimate.
        This will later be replaced with the TokenCounter
        (tiktoken) implemented in Phase 8.
        """

        original = max(
            1,
            prompt.tokens.original_tokens,
        )

        optimized = max(
            1,
            len(compressed_text.split()),
        )

        prompt.tokens.optimized_tokens = optimized

        prompt.tokens.tokens_saved = max(
            0,
            original - optimized,
        )

        prompt.tokens.reduction_percentage = (
            prompt.tokens.tokens_saved
            / original
        ) * 100

        prompt.compression.compression_ratio = (
            optimized / original
        )


    def _chunk_prompt(
        self,
        text: str,
    ) -> list[str]:
        """
        Split the prompt into chunks suitable for LLMLingua.

        Falls back to the original prompt if the chunker
        produces no output.
        """

        chunks = self._chunker.chunk(text)

        if not chunks:
            return [text]

        return chunks
    
    def _order_chunks(
        self,
        chunks: list[str],
        scores: list[float],
    ) -> tuple[list[str], list[float]]:
        """
        Order chunks by descending importance.
        """

        ordered = sorted(
            zip(
                chunks,
                scores,
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        return (
            [c for c, _ in ordered],
            [s for _, s in ordered],
        )


    def _build_compression_flags(
        self,
        scores: list[float],
    ) -> list[bool]:
        """
        Decide which chunks may be compressed.
        """

        if not scores:
            return []

        average = sum(scores) / len(scores)

        return [
            score < average
            for score in scores
        ]
    
    

    def _build_request(
        self,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
        profile: CompressionProfile,
        chunks: list[str],
        compress_flags: list[bool],
        scores: list[float],
    ) -> dict:
        """
        Build the request passed to LLMLingua.

        The builder is responsible for converting chunk scores
        into LLMLingua-specific request parameters.
        """

        return self._builder.build(
            prompt=prompt,
            policy=policy,
            profile=profile,
            chunks=chunks,
            compress_flags=compress_flags,
            scores=scores,
        )
    

    def _compress_with_llmlingua(
        self,
        request: dict,
    ):
        """
        Execute Microsoft's LLMLingua.

        All interaction with PromptCompressor is isolated
        inside this method.
        """

        compressor = self._load_compressor()

        return compressor.compress_prompt(
            **request,
        )
    

    def _extract_compressed_text(
        self,
        result,
        fallback: str,
    ) -> str:
        """
        Normalize LLMLingua's response.

        Future API changes should only require modifications
        to CompressionResultExtractor.
        """

        return self._extractor.extract(
            result=result,
            fallback=fallback,
        )
    

    def compress(
        self,
        text: str,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
    ) -> str:
        """
        Compress a prompt using Microsoft's LongLLMLingua.
        """

        if not text.strip():
            return text

        profile = self._profile_builder.build(
            prompt,
        )

        if not profile.enabled:
            return text
        
        try:

            # ---------------------------------
            # Chunk prompt
            # ---------------------------------

            chunks = self._chunk_prompt(
                text,
            )

            # ---------------------------------
            # Score chunks
            # ---------------------------------

            scores = self._importance_scorer.score(
                chunks=chunks,
                prompt=prompt,
            )

            ordered_chunks, ordered_scores = self._order_chunks(
                chunks,
                scores,
            )

            compress_flags = self._build_compression_flags(
                ordered_scores,
            )

            compress_flags = [
                score < 0.80
                for score in scores
            ]

            # ---------------------------------
            # Build LLMLingua request
            # ---------------------------------

            request = self._build_request(
                prompt=prompt,
                context=context,
                policy=policy,
                profile=profile,
                chunks=ordered_chunks,
                compress_flags=compress_flags,
                scores=ordered_scores,
            )

            # ---------------------------------
            # Execute LLMLingua
            # ---------------------------------

            result = self._compress_with_llmlingua(
                request,
            )

            # ---------------------------------
            # Extract compressed text
            # ---------------------------------

            compressed = self._extract_compressed_text(
                result=result,
                fallback=text,
            )

            # ---------------------------------
            # Update statistics
            # ---------------------------------

            self._update_statistics(
                prompt,
                compressed,
            )

            prompt.compression.success = True

            return compressed

        except Exception as exc:

            import traceback

            traceback.print_exc()

            prompt.compression.success = False

            prompt.diagnostics.warnings.append(
                f"LongLLMLingua compression failed: {exc}"
            )

            raise