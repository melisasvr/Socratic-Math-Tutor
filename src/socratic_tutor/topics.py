import re

TOPIC_LABELS = {
    "algebra": "Algebra",
    "calculus": "Calculus",
    "geometry": "Geometry",
    "trigonometry": "Trigonometry",
    "linear_algebra": "Linear Algebra",
    "statistics": "Statistics",
    "number_theory": "Number Theory",
    "general": "General Math",
}


TOPIC_KEYWORDS = {
    "linear_algebra": ["matrix", "vector", "eigen", "determinant", "span", "basis"],
    "statistics": ["probability", "mean", "median", "variance", "distribution", "hypothesis", "sample"],
    "number_theory": ["prime", "mod", "divisible", "gcd", "lcm", "congruence", "integer"],
    "calculus": ["derivative", "integral", "limit", "differentiate", "dx", "slope"],
    "trigonometry": ["sin", "cos", "tan", "triangle", "radian", "degree"],
    "geometry": ["circle", "area", "perimeter", "angle", "polygon", "triangle"],
    "algebra": ["equation", "factor", "quadratic", "polynomial", "solve for", "x="],
}


TOPIC_GUIDANCE = {
    "linear_algebra": "Emphasize vector space intuition, dimensions, and matrix operations with small checks.",
    "statistics": "Emphasize assumptions, data interpretation, and the meaning of each computed value.",
    "number_theory": "Emphasize divisibility logic, modular arithmetic rules, and proof-style reasoning.",
    "calculus": "Emphasize derivative/integral rules and what each step means geometrically.",
    "trigonometry": "Emphasize identities, units, and right-triangle relationships.",
    "geometry": "Emphasize diagrams, known formulas, and step-by-step constraints.",
    "algebra": "Emphasize symbolic manipulation and equation-balance principles.",
    "general": "Use general mathematical reasoning with one small step at a time.",
}


def detect_topic(problem_text: str) -> str:
    text = (problem_text or "").lower()

    def has_keyword(keyword: str) -> bool:
        pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"
        return re.search(pattern, text) is not None

    for topic in [
        "linear_algebra",
        "statistics",
        "number_theory",
        "calculus",
        "trigonometry",
        "geometry",
        "algebra",
    ]:
        if any(has_keyword(keyword) for keyword in TOPIC_KEYWORDS[topic]):
            return topic
    return "general"


def topic_instruction(topic: str) -> str:
    return TOPIC_GUIDANCE.get(topic, TOPIC_GUIDANCE["general"])
