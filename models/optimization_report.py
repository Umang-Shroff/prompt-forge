from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationStep:
    """
    Represents a single optimizer execution result.
    """

    name: str
    changed: bool
    chars_before: int = 0
    chars_after: int = 0

    @property
    def chars_removed(self) -> int:
        return max(0, self.chars_before - self.chars_after)


@dataclass(slots=True)
class OptimizationReport:
    """
    Tracks which optimizers ran and their impact.
    """

    steps: list[OptimizationStep] = field(default_factory=list)

    def add_step(
        self,
        name: str,
        before: str,
        after: str,
    ) -> None:

        self.steps.append(
            OptimizationStep(
                name=name,
                changed=(before != after),
                chars_before=len(before),
                chars_after=len(after),
            )
        )

    @property
    def changed_steps(self) -> list[OptimizationStep]:
        return [s for s in self.steps if s.changed]

    @property
    def unchanged_steps(self) -> list[OptimizationStep]:
        return [s for s in self.steps if not s.changed]

    @property
    def total_chars_saved(self) -> int:
        return sum(s.chars_removed for s in self.steps)