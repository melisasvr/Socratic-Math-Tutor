from socratic_tutor.topics import detect_topic


def test_detect_topic_linear_algebra():
    prompt = "Find the determinant of this matrix and its eigenvalues"
    assert detect_topic(prompt) == "linear_algebra"


def test_detect_topic_statistics():
    prompt = "Compute mean and variance for this sample distribution"
    assert detect_topic(prompt) == "statistics"


def test_detect_topic_number_theory():
    prompt = "Is this integer divisible by 3 and what is gcd(24, 18)?"
    assert detect_topic(prompt) == "number_theory"


def test_detect_topic_general_fallback():
    prompt = "Help me solve this math problem"
    assert detect_topic(prompt) == "general"


def test_detect_topic_avoids_substring_false_positive():
    prompt = "Since this is unclear, can you explain the approach?"
    assert detect_topic(prompt) == "general"
