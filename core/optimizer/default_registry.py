from .filler_optimizer import FillerOptimizer
from .redundancy_optimizer import RedundancyOptimizer
from .registry import OptimizerRegistry
from .sentence_optimizer import SentenceOptimizer
from .instruction_optimizer import InstructionOptimizer
from .role_optimizer import RoleOptimizer
from .repetition_optimizer import RepetitionOptimizer

def create_default_registry() -> OptimizerRegistry:

    registry = OptimizerRegistry()

    registry.extend(
        [
            FillerOptimizer(),
            InstructionOptimizer(),
            SentenceOptimizer(),
            RoleOptimizer(),
            RedundancyOptimizer(),
            RepetitionOptimizer(),
        ]
    )

    return registry