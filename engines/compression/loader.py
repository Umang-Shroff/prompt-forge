from __future__ import annotations

import torch

from llmlingua import PromptCompressor

from models import CompressionConfig


class CompressorLoader:
    """
    Responsible for creating PromptCompressor instances.

    All HuggingFace and LLMLingua initialization is isolated
    inside this class.
    """

    def __init__(
        self,
        config: CompressionConfig,
    ) -> None:

        self._config = config

    def _resolve_device(self) -> str:
        """
        Resolve the configured device.

        "auto" selects CUDA if available,
        otherwise CPU.
        """

        if self._config.device_map != "auto":
            return self._config.device_map

        return "cuda" if torch.cuda.is_available() else "cpu"

    def load(self) -> PromptCompressor:

        kwargs = {
            "model_name": self._config.model_name,
            "device_map": self._resolve_device(),
            "model_config": self._config.model_config,
            "use_llmlingua2": self._config.use_llmlingua2,
        }

        if self._config.cache_dir is not None:
            kwargs["cache_dir"] = self._config.cache_dir

        return PromptCompressor(**kwargs)