from __future__ import annotations


from .vocabulary import (
    IntentVocabulary,
    VocabularyEntry,
)

from models import IntentType

VOCABULARY = IntentVocabulary(
    {

        IntentType.ROLE: VocabularyEntry(

            phrases=(

                ("act as", 0.40),

                ("assume the role", 0.40),

                ("behave as", 0.35),

                ("you are", 0.30),

            ),

            keywords=(

                ("expert", 0.18),

                ("architect", 0.18),

                ("consultant", 0.15),

                ("senior", 0.12),

            ),
        ),

        IntentType.DEBUG: VocabularyEntry(

            phrases=(

                ("stack trace", 0.40),

            ),

            keywords=(

                ("debug", 0.20),

                ("bug", 0.18),

                ("error", 0.18),

                ("traceback", 0.30),

                ("exception", 0.25),

                ("fix", 0.15),

            ),
        ),

        IntentType.PLAN: VocabularyEntry(

            keywords=(

                ("architecture", 0.22),

                ("roadmap", 0.22),

                ("design", 0.18),

                ("implementation", 0.18),

                ("strategy", 0.18),

            ),
        ),

        IntentType.EXPLAIN: VocabularyEntry(

            keywords=(

                ("explain", 0.20),

                ("describe", 0.18),

                ("teach", 0.18),

                ("why", 0.15),

                ("how", 0.15),

            ),
        ),

        IntentType.GENERATE_CODE: VocabularyEntry(

            keywords=(

                ("implement", 0.22),

                ("build", 0.20),

                ("create", 0.18),

                ("python", 0.15),

                ("java", 0.15),

                ("react", 0.15),

                ("fastapi", 0.15),

                ("api", 0.12),

                ("class", 0.10),

                ("function", 0.10),

            ),
        ),

    }
)