from __future__ import annotations

from dataclasses import dataclass
from dataclasses import dataclass, field

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

    # model_name: str = "microsoft/Phi-3-mini-4k-instruct"
    model_name: str = "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank"

    # ------------------------------------------------------
    # Device
    # ------------------------------------------------------

    # "cpu"
    # "cuda"
    # "auto"
    device_map: str = "auto"

    # ------------------------------------------------------
    # Optional cache location
    # ------------------------------------------------------

    cache_dir: str | None = None

    model_config: dict = field(
        default_factory=lambda: {
            "trust_remote_code": True,
        }
    )

    # ------------------------------------------------------
    # LLMLingua Version
    # ------------------------------------------------------

    use_llmlingua2: bool = True