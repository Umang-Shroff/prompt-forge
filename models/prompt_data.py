from __future__ import annotations

from dataclasses import dataclass, field
from .optimization_report import OptimizationReport
from .enums import (
    CompressionEngine,
    OptimizationMode,
    PromptType,
)
from .metadata import Metadata
from .normalization_report import NormalizationReport

from dataclasses import dataclass

# ==========================================================
# Analysis Result
# ==========================================================


@dataclass(slots=True)
class AnalysisResult:
    """
    Stores information discovered during prompt analysis.

    Each detector reports what it found along with a confidence
    score. The MixedDetector later combines these results to
    determine the final PromptType.
    """

    # ------------------------------------------------------
    # Final Classification
    # ------------------------------------------------------

    prompt_type: PromptType = PromptType.TEXT

    # ------------------------------------------------------
    # Detector Flags
    # ------------------------------------------------------

    contains_code: bool = False
    contains_markdown: bool = False
    contains_json: bool = False
    contains_xml: bool = False
    contains_sql: bool = False
    contains_logs: bool = False

    # ------------------------------------------------------
    # Language Detection
    # ------------------------------------------------------

    detected_languages: list[str] = field(default_factory=list)

    # ------------------------------------------------------
    # Detector Confidence Scores
    # ------------------------------------------------------

    confidence: dict[str, float] = field(
        default_factory=lambda: {
            "code": 0.0,
            "markdown": 0.0,
            "json": 0.0,
            "xml": 0.0,
            "sql": 0.0,
            "logs": 0.0,
        }
    )

    # ------------------------------------------------------
    # Utility
    # ------------------------------------------------------

    def set_confidence(self, detector: str, score: float) -> None:
        """
        Store the highest confidence reported by a detector.
        """

        current = self.confidence.get(detector, 0.0)

        if score > current:
            self.confidence[detector] = score

    def mark_detected(
        self,
        detector: str,
        confidence: float,
    ) -> None:
        """
        Mark a detector as having identified its content type
        and record its confidence.
        """

        attribute = f"contains_{detector}"

        if hasattr(self, attribute):
            setattr(self, attribute, True)

        self.set_confidence(detector, confidence)

    def add_language(self, language: str) -> None:
        """
        Add a detected programming language if it has not
        already been recorded.
        """

        if language not in self.detected_languages:
            self.detected_languages.append(language)

    @property
    def detected_types(self) -> list[str]:
        """
        Returns all detector names that successfully detected
        their respective content type.
        """

        return [
            detector
            for detector, score in self.confidence.items()
            if score > 0
        ]


# ==========================================================
# Token Statistics
# ==========================================================


@dataclass(slots=True)
class TokenStats:
    """
    Stores token statistics before and after optimization.
    """

    original_tokens: int = 0
    optimized_tokens: int = 0

    tokens_saved: int = 0
    reduction_percentage: float = 0.0

    def update(self) -> None:
        """
        Recalculate derived metrics.
        """

        self.tokens_saved = max(
            0,
            self.original_tokens - self.optimized_tokens,
        )

        if self.original_tokens > 0:
            self.reduction_percentage = (
                self.tokens_saved / self.original_tokens
            ) * 100
        else:
            self.reduction_percentage = 0.0


# ==========================================================
# Compression Result
# ==========================================================


@dataclass(slots=True)
class CompressionResult:
    """
    Stores compression-related information.
    """

    engine: str = "None"

    compression_ratio: float = 0.0

    semantic_similarity: float | None = None

    success: bool = False


# ==========================================================
# Diagnostics
# ==========================================================


@dataclass(slots=True)
class Diagnostics:
    """
    Stores warnings and errors produced by pipeline stages.
    """

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


# ==========================================================
# Prompt Data
# ==========================================================


@dataclass(slots=True)
class PromptData:
    """
    Shared object that flows through the entire optimization
    pipeline.

    Every stage receives this object, updates only the
    information it owns, and returns the same instance.
    """

    # ------------------------------------------------------
    # Prompt Content
    # ------------------------------------------------------

    original_prompt: str

    current_prompt: str = ""

    # ------------------------------------------------------
    # User Configuration
    # ------------------------------------------------------

    mode: OptimizationMode = OptimizationMode.BALANCED

    # ------------------------------------------------------
    # Pipeline Results
    # ------------------------------------------------------
    @property
    def compression_ratio(self) -> float:
        if self.tokens.original_tokens == 0:
            return 0.0
        return self.tokens.reduction_percentage
    
    @property
    def reduction_percentage(self) -> float:
        if self.tokens.original_tokens == 0:
            return 0.0
    
        return self.tokens.reduction_percentage
    
    @property
    def tokens_saved(self) -> int:
        """
        Number of tokens removed by optimization.
        """

        return max(
            0,
            self.tokens.original_tokens
            - self.tokens.optimized_tokens,
        )

    @property
    def compression_applied(self) -> bool:
        """
        Whether the optimization actually reduced the prompt.
        """

        return self.tokens_saved > 0

    @property
    def compression_engine(self) -> str:
        """
        Name of the compression engine used.
        """

        return str(self.compression.engine)

    @property
    def original_tokens(self) -> int:
        """
        Original prompt token count.
        """

        return self.tokens.original_tokens

    @property
    def optimized_tokens(self) -> int:
        """
        Optimized prompt token count.
        """

        return self.tokens.optimized_tokens
    
    analysis: AnalysisResult = field(default_factory=AnalysisResult)
    
    # ------------------------------------------------------
    # Normalization
    # ------------------------------------------------------

    normalization: NormalizationReport = field(
        default_factory=NormalizationReport
    )

    optimization: OptimizationReport = field(
        default_factory=OptimizationReport
    )
    
    tokens: TokenStats = field(default_factory=TokenStats)

    compression: CompressionResult = field(
        default_factory=CompressionResult
    )

    diagnostics: Diagnostics = field(default_factory=Diagnostics)

    metadata: Metadata = field(default_factory=Metadata)

    def __post_init__(self) -> None:
        """
        If no current prompt is provided,
        initialize it with the original prompt.
        """

        if not self.current_prompt:
            self.current_prompt = self.original_prompt