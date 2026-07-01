from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NormalizationReport:
    """
    Records which normalizers modified the prompt.
    """

    applied: list[str] = field(default_factory=list)

    skipped: list[str] = field(default_factory=list)

    def mark_applied(
        self,
        normalizer: str,
    ) -> None:

        if normalizer not in self.applied:
            self.applied.append(normalizer)

    def mark_skipped(
        self,
        normalizer: str,
    ) -> None:

        if (
            normalizer not in self.applied
            and normalizer not in self.skipped
        ):
            self.skipped.append(normalizer)