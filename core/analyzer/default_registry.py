from __future__ import annotations

from .code_detector import CodeDetector
from .json_detector import JsonDetector
from .logs_detector import LogsDetector
from .markdown_detector import MarkdownDetector
from .mixed_detector import MixedDetector
from .registry import DetectorRegistry
from .sql_detector import SqlDetector
from .xml_detector import XmlDetector


def create_default_registry() -> DetectorRegistry:
    """
    Create the default detector registry used by the analyzer.

    All built-in detectors are registered here.
    """

    registry = DetectorRegistry()

    registry.extend(
        [
            CodeDetector(),
            JsonDetector(),
            XmlDetector(),
            SqlDetector(),
            MarkdownDetector(),
            LogsDetector(),
            MixedDetector(),
        ]
    )

    return registry