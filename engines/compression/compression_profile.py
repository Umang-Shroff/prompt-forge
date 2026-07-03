from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CompressionProfile:
    """
    Describes how the compression engine should
    compress the current prompt.
    """

    target_ratio: float

    enabled: bool = True

    reorder_context: str = "original"

    rank_method: str = "longllmlingua"

    force_tokens: list[str] = field(default_factory=list)

    force_reserve: list[str] = field(default_factory=list)

    preserve_structure: bool = False

    preserve_lists: bool = False

    preserve_code: bool = False

    preserve_examples: bool = False

    preserve_reasoning: bool = False

    preserve_roles: bool = False

    preserve_instructions: bool = False

    aggressive_filtering: bool = False

    chunk_size: int = 900