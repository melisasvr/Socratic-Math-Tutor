import re
from typing import List

# Common mistake patterns to detect in student responses or tutor corrections
# This dictionary uses "Regular Expressions" (regex) to find keywords in the chat
MISTAKE_PATTERNS = {
    "sign_error": [
        r"sign", r"positive", r"negative", r"\+", r"\-", r"flipped"
    ],
    "arithmetic_error": [
        r"calculation", r"add", r"subtract", r"multiply", r"divide", r"wrong sum"
    ],
    "algebra_step_error": [
        r"isolate", r"both sides", r"transpose", r"variable", r"coefficient"
    ],
    "formula_misuse": [
        r"formula", r"plug", r"substitute", r"wrong equation"
    ],
    "unit_error": [
        r"unit", r"meters", r"seconds", r"kg", r"conversion"
    ],
    "fraction_decimal_error": [
        r"fraction", r"decimal", r"numerator", r"denominator", r"simplify"
    ]
}

def is_correction_feedback(tutor_reply: str) -> bool:
    """
    Detects if the tutor's reply indicates a mistake was made.
    This prevents the app from tagging mistakes when the student is doing well.
    """
    correction_signals = [
        "not quite", "almost", "check your", "look again", 
        "re-examine", "mistake", "error", "wait", "hold on"
    ]
    return any(signal in tutor_reply.lower() for signal in correction_signals)

def detect_mistake_patterns(student_input: str, tutor_reply: str) -> List[str]:
    """
    Analyzes the interaction to tag what kind of mistake occurred.
    It combines the student's message and the AI's reply to find matches.
    """
    detected_tags = set()
    combined_text = (student_input + " " + tutor_reply).lower()

    for tag, patterns in MISTAKE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, combined_text):
                detected_tags.add(tag)
    
    return list(detected_tags)