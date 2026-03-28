from socratic_tutor.mistakes import detect_mistake_patterns, is_correction_feedback


def test_is_correction_feedback_true_for_correction_signal():
    feedback = "Not quite. Check the sign in your second step."
    assert is_correction_feedback(feedback) is True


def test_is_correction_feedback_false_for_positive_feedback():
    feedback = "Great work. Your approach is correct."
    assert is_correction_feedback(feedback) is False


def test_detect_mistake_patterns_sign_and_algebra():
    student = "I distributed and got x-3 instead of x+3"
    feedback = "Check the sign while you distribute."
    tags = detect_mistake_patterns(student, feedback)
    assert "sign_error" in tags
    assert "algebra_step_error" in tags


def test_detect_mistake_patterns_formula_misuse():
    student = "I used the wrong formula for area"
    feedback = "Try applying the correct formula first."
    tags = detect_mistake_patterns(student, feedback)
    assert tags == ["formula_misuse"]


def test_detect_mistake_patterns_empty_inputs():
    assert detect_mistake_patterns("", "") == []
