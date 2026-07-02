from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationHints:
    """
    Intent-aware optimization hints.

    Strategies populate these hints and downstream optimizer/
    compressor stages consume them.
    """

    preserve_terms: set[str] = field(
        default_factory=set,
    )

    protected_phrases: set[str] = field(
        default_factory=set,
    )

    removable_phrases: set[str] = field(
        default_factory=set,
    )

    preferred_keywords: set[str] = field(
        default_factory=set,
    )

    def clear(self) -> None:

        self.preserve_terms.clear()

        self.protected_phrases.clear()

        self.removable_phrases.clear()

        self.preferred_keywords.clear()