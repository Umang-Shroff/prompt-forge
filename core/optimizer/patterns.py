"""
Semantic optimization patterns.

Each optimizer imports only the rules it needs.
"""

from __future__ import annotations

# ==========================================================
# Filler phrases
# ==========================================================

FILLER_PATTERNS = {
    r"\bcould you please\b": "please",
    r"\bcan you please\b": "please",
    r"\bi would like you to\b": "",
    r"\bif possible\b": "",
    r"\bkindly\b": "",
    r"\bplease kindly\b": "please",
    r"\bi was wondering if you could\b": "",
}

# ==========================================================
# Sentence simplifications
# ==========================================================

SENTENCE_PATTERNS = {
    r"\bin order to\b": "to",
    r"\bdue to the fact that\b": "because",
    r"\bat this point in time\b": "now",
    r"\bin the event that\b": "if",
    r"\bfor the purpose of\b": "for",
    r"\bwith regard to\b": "regarding",
}

# ==========================================================
# Repeated words
# ==========================================================

REDUNDANT_WORD_PATTERN = (
    r"\b([A-Za-z0-9_]+)\b(?:\s+\1\b)+"
)

# ==========================================================
# Instruction simplifications
# ==========================================================

INSTRUCTION_PATTERNS = {
    r"\bplease provide\b": "provide",
    r"\bplease explain\b": "explain",
    r"\bplease analyze\b": "analyze",
    r"\bplease generate\b": "generate",
    r"\bplease write\b": "write",
    r"\bplease create\b": "create",
    r"\bplease tell me\b": "tell me",
    r"\bplease give me\b": "give",
    r"\bprovide a detailed explanation of\b": "explain",
    r"\bgive me a detailed explanation of\b": "explain",
    r"\bprovide an explanation of\b": "explain",
    r"\bprovide a summary of\b": "summarize",
    r"\bgive me a summary of\b": "summarize",
}

# ==========================================================
# Role simplifications
# ==========================================================

ROLE_PATTERNS = {
    r"you are an expert software engineer specializing in python development":
        "You are a Python expert.",

    r"you are an expert software engineer":
        "You are a software engineer.",

    r"you are an experienced python developer":
        "You are a Python developer.",

    r"act as an expert":
        "Act as an expert.",

    r"assume the role of":
        "Act as",
}