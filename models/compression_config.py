from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)


@dataclass(slots=True, frozen=True)
class CompressionConfig:
    """
    Configuration for compression engines.

    This class contains everything related to loading and
    configuring an ML-backed compression engine.

    The engine itself should never hardcode model names,
    devices, or LLMLingua settings.
    """

    # ------------------------------------------------------
    # HuggingFace Model
    # ------------------------------------------------------

    # Alternative:
    # "microsoft/Phi-3-mini-4k-instruct"

    model_name: str = (
        "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank"
    )

    # ------------------------------------------------------
    # Device
    # ------------------------------------------------------

    # Supported values:
    # "cpu"
    # "cuda"
    # "auto"

    device_map: str = "auto"

    # ------------------------------------------------------
    # Optional Hugging Face cache directory
    # ------------------------------------------------------

    cache_dir: str | None = None

    # ------------------------------------------------------
    # Extra model configuration
    # ------------------------------------------------------

    model_config: dict = field(
        default_factory=lambda: {
            "trust_remote_code": True,
        }
    )

    # ------------------------------------------------------
    # LLMLingua Version
    # ------------------------------------------------------

    use_llmlingua2: bool = True

    # ------------------------------------------------------
    # Cache Key
    # ------------------------------------------------------

    @property
    def cache_key(self) -> tuple:
        """
        Unique identifier for this configuration.

        ML resources (PromptCompressor, AutoTokenizer, etc.)
        can safely reuse instances when their cache keys match.
        """

        return (
            self.model_name,
            self.device_map,
            self.cache_dir,
            self.use_llmlingua2,
        )

    # ------------------------------------------------------
    # Convenience
    # ------------------------------------------------------

    @property
    def is_gpu(self) -> bool:
        """
        Whether the preferred execution device is CUDA.
        """

        return self.device_map == "cuda"