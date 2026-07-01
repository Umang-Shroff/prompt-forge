from __future__ import annotations

import json

from models import PromptData

from .detector import Detector


class JsonDetector(Detector):
    """
    Detects JSON content.
    """

    @property
    def priority(self) -> int:
        return 20

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt.strip()

        try:

            json.loads(text)

            prompt.analysis.contains_json = True

            prompt.analysis.set_confidence(
                "json",
                1.0,
            )

        except Exception:

            return