from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenizerConfig:
    """
    Configuration for token counting.

    The optimizer is model-agnostic, so token counting
    should also be configurable.
    """

    model_name: str = "gpt-4o-mini"

    fallback_encoding: str = "cl100k_base"