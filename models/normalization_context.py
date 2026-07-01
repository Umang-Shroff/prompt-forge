from __future__ import annotations

from dataclasses import dataclass

from .enums import OptimizationMode, PromptType
from .prompt_data import AnalysisResult


@dataclass(slots=True, frozen=True)
class NormalizationContext:
    """
    Read-only context supplied to every normalizer.
    """

    mode: OptimizationMode

    analysis: AnalysisResult

    @property
    def is_text(self) -> bool:
        return self.analysis.prompt_type == PromptType.TEXT

    @property
    def is_code(self) -> bool:
        return self.analysis.prompt_type == PromptType.CODE

    @property
    def is_markdown(self) -> bool:
        return self.analysis.prompt_type == PromptType.MARKDOWN

    @property
    def is_json(self) -> bool:
        return self.analysis.prompt_type == PromptType.JSON

    @property
    def is_xml(self) -> bool:
        return self.analysis.prompt_type == PromptType.XML

    @property
    def is_sql(self) -> bool:
        return self.analysis.prompt_type == PromptType.SQL

    @property
    def is_logs(self) -> bool:
        return self.analysis.prompt_type == PromptType.LOGS

    @property
    def is_mixed(self) -> bool:
        return self.analysis.prompt_type == PromptType.MIXED

    @property
    def is_structured(self) -> bool:
        """
        Structured formats should generally preserve formatting.
        """

        return (
            self.is_json
            or self.is_xml
            or self.is_sql
        )