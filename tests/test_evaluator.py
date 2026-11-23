
import pytest

from assessment.scoring.evaluator import evaluate_answers


@pytest.fixture
def questions():
    return {
        "q1": {
            "correct": "a",
            "explanation": "Option A is correct."
        },
        "q2": {
            "correct": "b",
            "explanation": "Option B is correct."
        },
        "q3": {
            "correct": "c",
            "explanation": "Option C is correct."
        }
    }


def test_all_answers_correct(questions):
    answers = {"q1": "a", "q2": "b", "q3": "c"}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 3
    assert result["total_questions"] == 3
    assert result["score_pct"] == 100
    assert result["wrong_question_ids"] == []


def test_all_answers_wrong(questions):
    answers = {"q1": "b", "q2": "c", "q3": "a"}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 0
    assert result["total_questions"] == 3
    assert result["score_pct"] == 0
    assert len(result["wrong_question_ids"]) == 3


def test_mixed_answers(questions):
    answers = {"q1": "a", "q2": "c", "q3": "c"}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 2
    assert result["total_questions"] == 3
    assert result["score_pct"] == 67
    assert result["wrong_question_ids"] == ["q2"]


def test_skipped_answer(questions):
    answers = {"q1": "a", "q2": None}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 1
    assert result["total_questions"] == 2
    assert result["score_pct"] == 50
    assert "q2" in result["wrong_question_ids"]

    skipped = result["breakdown"][1]
    assert skipped["is_skipped"] is True
    assert skipped["is_correct"] is False
    assert skipped["chosen"] is None


def test_empty_string_is_skipped(questions):
    answers = {"q1": ""}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 0
    assert result["score_pct"] == 0
    assert result["breakdown"][0]["is_skipped"] is True


def test_answer_with_spaces_and_uppercase(questions):
    answers = {"q1": " A "}

    result = evaluate_answers(answers, questions)

    assert result["correct_count"] == 1
    assert result["score_pct"] == 100


def test_invalid_answer_choice_raises_error(questions):
    answers = {"q1": "z"}

    with pytest.raises(ValueError):
        evaluate_answers(answers, questions)


def test_unknown_question_id_raises_error(questions):
    answers = {"unknown_q": "a"}

    with pytest.raises(ValueError):
        evaluate_answers(answers, questions)


def test_empty_answers_raise_error(questions):
    with pytest.raises(ValueError):
        evaluate_answers({}, questions)


def test_breakdown_contains_explanation(questions):
    answers = {"q1": "a"}

    result = evaluate_answers(answers, questions)

    assert result["breakdown"][0]["explanation"] == "Option A is correct."
