from __future__ import annotations

from dataclasses import dataclass, field

from .score import ImportanceScore


@dataclass(slots=True)
class ImportanceResult:
    """
    Combined importance assigned to one chunk.
    """

    scores: list[ImportanceScore] = field(
        default_factory=list,
    )

    def add(
        self,
        score: ImportanceScore,
    ) -> None:

        self.scores.append(score)

    @property
    def confidence(
        self,
    ) -> float:

        if not self.scores:
            return 0.50

        return max(
            score.confidence
            for score in self.scores
        )

    @property
    def evidence(
        self,
    ) -> list[str]:

        result: list[str] = []

        for score in self.scores:
            result.extend(score.evidence)

        return result