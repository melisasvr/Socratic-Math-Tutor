from collections.abc import Iterable


MISTAKE_PATTERNS = {
    "sign_error": [
        "sign",
        "negative",
        "minus",
        "plus",
        "opposite sign",
    ],
    "arithmetic_error": [
        "arithmetic",
        "calculation",
        "multiply",
        "division",
        "addition",
        "subtraction",
    ],
    "algebra_step_error": [
        "factor",
        "distribute",
        "expand",
        "simplify",
        "combine like terms",
        "equation balance",
    ],
    "formula_misuse": [
        "formula",
        "identity",
        "theorem",
        "rule",
        "substitute",
    ],
    "unit_error": [
        "unit",
        "dimension",
    ],
    "fraction_decimal_error": [
        "fraction",
        "decimal",
        "denominator",
        "numerator",
    ],
}


CORRECTION_SIGNALS = [
    "not quite",
    "incorrect",
    "mistake",
    "check",
    "try again",
    "fix",
    "error",
]


def _normalize_text(parts: Iterable[str]) -> str:
    cleaned = [part.strip().lower() for part in parts if isinstance(part, str) and part.strip()]
    return "\n".join(cleaned)


def is_correction_feedback(feedback_text: str) -> bool:
    text = _normalize_text([feedback_text])
    if not text:
        return False
    return any(signal in text for signal in CORRECTION_SIGNALS)


def detect_mistake_patterns(student_text: str, feedback_text: str) -> list[str]:
    combined = _normalize_text([student_text, feedback_text])
    if not combined:
        return []

    tags: list[str] = []
    for tag, keywords in MISTAKE_PATTERNS.items():
        if any(keyword in combined for keyword in keywords):
            tags.append(tag)
    return tags
