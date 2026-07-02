from __future__ import annotations

from .registry import IntentRegistry

from .detectors.role_detector import RoleDetector
from .detectors.explanation_detector import ExplanationDetector
from .detectors.planning_detector import PlanningDetector
from .detectors.coding_detector import CodingDetector
from .detectors.debugging_detector import DebuggingDetector


def create_default_registry() -> IntentRegistry:

    registry = IntentRegistry()

    registry.extend(

        [

            RoleDetector(),

            ExplanationDetector(),

            PlanningDetector(),

            CodingDetector(),

            DebuggingDetector(),

        ]

    )

    return registry