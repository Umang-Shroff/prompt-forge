from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class QualityScore:
    """
    Stores prompt quality metrics.
    """

    clarity: float = 0.0
    structure: float = 0.0
    completeness: float = 0.0
    conciseness: float = 0.0
    specificity: float = 0.0

    overall: float = 0.0

    suggestions: list[str] = field(
        default_factory=list,
    )