from __future__ import annotations

from models import PromptData, PromptType

from .detector import Detector


class MixedDetector(Detector):
    """
    Determines the final prompt type after all
    detectors have completed.
    """

    @property
    def priority(self) -> int:
        return 1000

    def detect(self, prompt: PromptData) -> None:

        confidence = prompt.analysis.confidence

        active = {
            key: value
            for key, value in confidence.items()
            if value > 0
        }

        if not active:

            prompt.analysis.prompt_type = PromptType.TEXT
            return

        if len(active) > 1:

            prompt.analysis.prompt_type = PromptType.MIXED
            return

        detector = max(
            active.items(),
            key=lambda item: item[1],
        )[0]

        mapping = {
            "code": PromptType.CODE,
            "markdown": PromptType.MARKDOWN,
            "json": PromptType.JSON,
            "xml": PromptType.XML,
            "sql": PromptType.SQL,
            "logs": PromptType.LOGS,
        }

        prompt.analysis.prompt_type = mapping.get(
            detector,
            PromptType.TEXT,
        )