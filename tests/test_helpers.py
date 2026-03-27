from socratic_tutor.helpers import extract_bold_question, is_solution_likely_correct


def test_extract_bold_question_found():
    text = "Nice work. **What is your next step?**"
    assert extract_bold_question(text) == "What is your next step?"


def test_extract_bold_question_missing():
    text = "No bold question here"
    assert extract_bold_question(text) is None


def test_solution_likely_correct_positive():
    review = "Great job.\n{\"solved\": true}"
    assert is_solution_likely_correct(review) is True


def test_solution_likely_correct_negative():
    review = "There is a mistake in step 2.\n{\"solved\": false}"
    assert is_solution_likely_correct(review) is False


def test_solution_likely_correct_rejects_plain_text_without_json():
    review = "Excellent work. Your solution is correct and complete."
    assert is_solution_likely_correct(review) is False
