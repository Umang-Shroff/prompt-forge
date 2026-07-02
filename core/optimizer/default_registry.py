from PromptOptimizer.core.optimizer.hint_aware_optimizer import HintAwareOptimizer

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
            RoleOptimizer(),
            InstructionOptimizer(),
            SentenceOptimizer(),
            FillerOptimizer(),
            RedundancyOptimizer(),
            RepetitionOptimizer(),
        ]
    )

    return registry