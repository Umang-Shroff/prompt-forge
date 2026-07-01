from __future__ import annotations

from typing import Any

from core.compressor.context import CompressionContext

from models import (
    CompressionConfig,
    PromptData,
)

from .builder import CompressionRequestBuilder
from .chunker import PromptChunker
from .engine import CompressionEngine
from .extractor import CompressionResultExtractor
from .loader import CompressorLoader
from .policy import CompressionPolicy
from .scorer import ImportanceScorer


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

        self._loader = CompressorLoader(
            self._config,
        )

        self._builder = CompressionRequestBuilder()

        self._extractor = CompressionResultExtractor()

        self._chunker = PromptChunker()

        self._scorer = ImportanceScorer()

        # Lazy initialization.
        self._compressor: Any | None = None

    def _load_compressor(self) -> Any:
        """
        Lazily initialize PromptCompressor.

        The HuggingFace model is loaded only when
        compression is actually requested.
        """

        if self._compressor is None:

            self._compressor = self._loader.load()

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
    

    def _score_chunks(
        self,
        chunks: list[str],
    ) -> tuple[list[str], list[float]]:
        """
        Score every chunk.

        We intentionally preserve the original order because
        LLMLingua performs its own ranking internally.

        The scores are retained for future support of
        per-segment compression.
        """

        scores: list[float] = []

        for chunk in chunks:

            score = self._scorer.score(chunk)

            scores.append(score)

        return chunks, scores
    

    def _build_request(
        self,
        prompt: PromptData,
        context: CompressionContext,
        policy: CompressionPolicy,
        chunks: list[str],
        scores: list[float],
    ) -> dict:
        """
        Build the request passed to LLMLingua.

        The builder is responsible for converting chunk scores
        into LLMLingua-specific request parameters.
        """

        return self._builder.build(
            prompt=prompt,
            context=context,
            policy=policy,
            chunks=chunks,
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

            ordered_chunks, scores = self._score_chunks(
                chunks,
            )

            # ---------------------------------
            # Build LLMLingua request
            # ---------------------------------

            request = self._build_request(
                prompt=prompt,
                context=context,
                policy=policy,
                chunks=ordered_chunks,
                scores=scores,
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

            prompt.compression.success = False

            prompt.diagnostics.warnings.append(
                f"LongLLMLingua compression failed: {exc}"
            )

            return text