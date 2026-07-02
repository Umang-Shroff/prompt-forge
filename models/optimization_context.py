from __future__ import annotations

from dataclasses import dataclass

from .enums import (
    OptimizationMode,
    PromptType,
)
from .intent_result import IntentResult
from .normalization_report import NormalizationReport
from .optimization_hints import OptimizationHints
from .prompt_data import AnalysisResult
from .quality_score import QualityScore


# TYPE_CHECKING avoids a circular dependency because
# OptimizationPlan lives under core/.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.optimizer.optimization_plan import OptimizationPlan


@dataclass(slots=True, frozen=True)
class OptimizationContext:
    """
    Read-only context supplied to every optimizer.

    It exposes all information required for semantic
    optimization while keeping PromptData encapsulated.
    """

    mode: OptimizationMode

    analysis: AnalysisResult

    intent: IntentResult

    quality: QualityScore

    normalization: NormalizationReport

    optimization_hints: OptimizationHints

    plan: "OptimizationPlan"

    # ======================================================
    # Optimization Mode
    # ======================================================

    @property
    def is_conservative(self) -> bool:
        return self.mode == OptimizationMode.CONSERVATIVE

    @property
    def is_balanced(self) -> bool:
        return self.mode == OptimizationMode.BALANCED

    @property
    def is_aggressive(self) -> bool:
        return self.mode == OptimizationMode.AGGRESSIVE

    # ======================================================
    # Prompt Type
    # ======================================================

    @property
    def prompt_type(self) -> PromptType:
        return self.analysis.prompt_type

    @property
    def is_text(self) -> bool:
        return self.prompt_type == PromptType.TEXT

    @property
    def is_code(self) -> bool:
        return self.prompt_type == PromptType.CODE

    @property
    def is_markdown(self) -> bool:
        return self.prompt_type == PromptType.MARKDOWN

    @property
    def is_json(self) -> bool:
        return self.prompt_type == PromptType.JSON

    @property
    def is_xml(self) -> bool:
        return self.prompt_type == PromptType.XML

    @property
    def is_sql(self) -> bool:
        return self.prompt_type == PromptType.SQL

    @property
    def is_logs(self) -> bool:
        return self.prompt_type == PromptType.LOGS

    @property
    def is_mixed(self) -> bool:
        return self.prompt_type == PromptType.MIXED

    @property
    def is_structured(self) -> bool:
        """
        Structured formats whose formatting should be
        preserved as much as possible.
        """
        return (
            self.is_json
            or self.is_xml
            or self.is_sql
        )

    # ======================================================
    # Analysis Shortcuts
    # ======================================================

    @property
    def languages(self) -> tuple[str, ...]:
        return tuple(self.analysis.detected_languages)

    @property
    def contains_code(self) -> bool:
        return self.analysis.contains_code

    @property
    def contains_markdown(self) -> bool:
        return self.analysis.contains_markdown

    @property
    def contains_json(self) -> bool:
        return self.analysis.contains_json

    @property
    def contains_xml(self) -> bool:
        return self.analysis.contains_xml

    @property
    def contains_sql(self) -> bool:
        return self.analysis.contains_sql

    @property
    def contains_logs(self) -> bool:
        return self.analysis.contains_logs

    # ======================================================
    # Intent Shortcuts
    # ======================================================

    @property
    def primary_intent(self):
        return self.intent.primary

    @property
    def intent_confidence(self) -> float:
        return self.intent.confidence

    # ======================================================
    # Quality Shortcuts
    # ======================================================

    @property
    def quality_score(self) -> float:
        return self.quality.overall

    @property
    def needs_aggressive_optimization(self) -> bool:
        return (
            self.is_aggressive
            or self.quality.overall < 70
            or self.plan.aggressive
        )