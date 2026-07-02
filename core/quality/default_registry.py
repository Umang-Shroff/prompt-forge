from __future__ import annotations

from .registry import QualityRegistry

from .rules.clarity_rule import ClarityRule
from .rules.structure_rule import StructureRule
from .rules.conciseness_rule import ConcisenessRule
from .rules.completeness_rule import CompletenessRule
from .rules.specificity_rule import SpecificityRule
from .rules.overall_rule import OverallRule


def create_default_registry() -> QualityRegistry:

    registry = QualityRegistry()

    registry.extend(
        [
            ClarityRule(),
            StructureRule(),
            ConcisenessRule(),
            CompletenessRule(),
            SpecificityRule(),
            OverallRule(),
        ]
    )

    return registry