from __future__ import annotations

from models import PromptData
from .compression_profile import CompressionProfile


class CompressionProfileBuilder:
    """
    Builds an adaptive compression profile for the current prompt.
    """

    def build(
        self,
        prompt: PromptData,
    ) -> CompressionProfile:

        intent = prompt.intent
        quality = prompt.quality.overall
        mode = prompt.mode
        tokens = prompt.tokens.original_tokens
        analysis = prompt.analysis

        # ----------------------------------
        # Base compression ratio
        # ----------------------------------

        if mode.name == "CONSERVATIVE":
            ratio = 0.80

        elif mode.name == "BALANCED":
            ratio = 0.65

        else:
            ratio = 0.45

        enabled = True

        preserve_structure = False
        preserve_lists = False
        preserve_code = False
        preserve_examples = False
        preserve_reasoning = False
        preserve_roles = False
        preserve_instructions = False
        aggressive_filtering = False

        # ----------------------------------
        # Adaptive Rules
        # ----------------------------------

        # Very short prompts rarely benefit
        # from compression.
        if tokens < 80:
            enabled = False

        # Structured data should be preserved.
        if analysis.contains_json or analysis.contains_xml:

            ratio = max(
                ratio,
                0.90,
            )

            preserve_structure = True

        # Code prompts should retain identifiers.
        if analysis.contains_code:

            ratio = max(
                ratio,
                0.80,
            )

            preserve_code = True

        # Markdown formatting is valuable.
        if analysis.contains_markdown:

            ratio = max(
                ratio,
                0.75,
            )

            preserve_lists = True

        
        # Preserve role prompts.

        if (
            intent.primary is not None
            and intent.primary.name == "ROLE"
        ):
            preserve_roles = True

        # Preserve explanations.

        if (
            intent.primary is not None
            and intent.primary.name == "EXPLAIN"
        ):
            preserve_reasoning = True

        # Preserve planning prompts.

        if (
            intent.primary is not None
            and intent.primary.name == "PLAN"
        ):
            preserve_lists = True

        # Preserve debugging context.

        if (
            intent.primary is not None
            and intent.primary.name == "DEBUG"
        ):
            preserve_examples = True

        # Large prompts benefit from stronger compression.
        if tokens > 2000:

            if quality < 60:

                ratio *= 0.85

                aggressive_filtering = True

            elif quality > 90:
            
                ratio *= 1.05

            ratio *= 0.80

        elif tokens > 800:

            ratio *= 0.90

        # Keep ratio within safe bounds.
        ratio = max(
            0.20,
            min(
                ratio,
                0.95,
            ),
        )

        return CompressionProfile(
            enabled=enabled,
            target_ratio=ratio,
            reorder_context="original",
            force_tokens=sorted(
                prompt.optimization_hints.preferred_keywords,
            ),
            force_reserve=sorted(
                prompt.optimization_hints.protected_phrases,
            ),
            preserve_structure=preserve_structure,
            preserve_lists=preserve_lists,
            preserve_code=preserve_code,
            preserve_examples=preserve_examples,
            preserve_reasoning=preserve_reasoning,
            preserve_roles=preserve_roles,
            preserve_instructions=preserve_instructions,
            aggressive_filtering=aggressive_filtering,
        )