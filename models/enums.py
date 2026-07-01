from enum import Enum, auto


class OptimizationMode(Enum):
    """
    Determines how aggressively the prompt should be optimized.
    """

    CONSERVATIVE = auto()
    BALANCED = auto()
    AGGRESSIVE = auto()


class ValidationStatus(Enum):
    """
    Overall validation result after the pipeline completes.
    """

    NOT_RUN = auto()
    PASSED = auto()
    WARNING = auto()
    FAILED = auto()


class PromptType(Enum):
    """
    High-level classification of the prompt.
    """

    TEXT = auto()
    CODE = auto()
    MARKDOWN = auto()
    JSON = auto()
    XML = auto()
    SQL = auto()
    LOGS = auto()
    MIXED = auto()


class CompressionEngine(Enum):
    """
    Available compression backends.
    """

    NONE = auto()
    LLMLINGUA = auto()
    LONGLLMLINGUA = auto()
    CUSTOM = auto()