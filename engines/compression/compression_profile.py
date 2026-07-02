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

    force_tokens: list[str] = field(
        default_factory=list,
    )

    force_reserve: list[str] = field(
        default_factory=list,
    )

    rank_method: str = "longllmlingua"

    preserve_structure: bool = False

    preserve_lists: bool = False

    preserve_code: bool = False