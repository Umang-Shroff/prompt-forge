from __future__ import annotations

from .blank_line_normalizer import BlankLineNormalizer
from .code_fence_normalizer import CodeFenceNormalizer
from .newline_normalizer import NewlineNormalizer
from .registry import NormalizerRegistry
from .trailing_space_normalizer import TrailingSpaceNormalizer
from .unicode_normalizer import UnicodeNormalizer
from .whitespace_normalizer import WhitespaceNormalizer


def create_default_registry() -> NormalizerRegistry:
    """
    Create the default normalizer registry.
    """

    registry = NormalizerRegistry()

    registry.extend(
        [
            NewlineNormalizer(),
            TrailingSpaceNormalizer(),
            UnicodeNormalizer(),
            WhitespaceNormalizer(),
            BlankLineNormalizer(),
            CodeFenceNormalizer(),
        ]
    )

    return registry