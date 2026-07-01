from __future__ import annotations

import xml.etree.ElementTree as ET

from models import PromptData

from .detector import Detector


class XmlDetector(Detector):
    """
    Detects XML content.
    """

    @property
    def priority(self) -> int:
        return 30

    def detect(self, prompt: PromptData) -> None:

        text = prompt.current_prompt.strip()

        try:

            ET.fromstring(text)

            prompt.analysis.contains_xml = True

            prompt.analysis.set_confidence(
                "xml",
                1.0,
            )

        except ET.ParseError:

            return