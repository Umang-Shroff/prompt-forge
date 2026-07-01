from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from .enums import ValidationStatus


@dataclass(slots=True)
class Metadata:
    """
    Stores metadata about pipeline execution.
    """

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    started_at: float = field(default_factory=perf_counter)
    finished_at: float | None = None

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    completed_stages: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validation_status: ValidationStatus = ValidationStatus.NOT_RUN

    # ---------------------------------------------------------
    # Version
    # ---------------------------------------------------------

    version: str = "0.1.0"

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def processing_time(self) -> float | None:
        """
        Returns total execution time in seconds.
        """

        if self.finished_at is None:
            return None

        return self.finished_at - self.started_at

    @property
    def total_stages(self) -> int:
        """
        Number of successfully completed stages.
        """

        return len(self.completed_stages)

    def mark_stage_completed(self, stage_name: str) -> None:
        """
        Record a completed pipeline stage.
        """

        self.completed_stages.append(stage_name)

    def finish(self) -> None:
        """
        Mark pipeline execution as completed.
        """

        self.finished_at = perf_counter()