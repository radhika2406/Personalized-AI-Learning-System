from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.services import topic_mastery_service
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_answer import QuizAnswer
from app.models.topic import Topic
from app.models.course import Course


def submit_quiz(db: Session, user_id: int, quiz_id: int, submission):
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        return None

    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    if not questions:
        raise ValueError("This quiz has no questions")

    question_map = {
        question.id: question for question in questions
    }

    submitted_ids = [
        answer.question_id for answer in submission.answers
    ]

    if len(submitted_ids) != len(set(submitted_ids)):
        raise ValueError("Duplicate question answers are not allowed")

    if set(submitted_ids) != set(question_map.keys()):
        raise ValueError(
            "You must submit an answer for every question in this quiz"
        )

    attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=0,
        total_questions=len(questions),
    )

    db.add(attempt)
    db.flush()

    score = 0

    for answer in submission.answers:
        question = question_map[answer.question_id]

        if answer.selected_option == question.correct_option:
            score += 1

        db.add(
            QuizAnswer(
                attempt_id=attempt.id,
                question_id=answer.question_id,
                selected_option=answer.selected_option,
            )
        )

    attempt.score = score
    attempt.submitted_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(attempt)

        quiz_percentage = round(
            (attempt.score / attempt.total_questions) * 100,
            2,
        )

        topic_mastery_service.update_topic_mastery(
            db=db,
            user_id=user_id,
            topic_id=quiz.topic_id,
            quiz_percentage=quiz_percentage,
        )

    except Exception:
        db.rollback()
        raise

    return attempt


def build_attempt_review(db: Session, attempt: QuizAttempt):
    answers = db.query(QuizAnswer).filter(
        QuizAnswer.attempt_id == attempt.id
    ).all()

    questions = {
        question.id: question
        for question in db.query(Question).filter(
            Question.quiz_id == attempt.quiz_id
        ).all()
    }

    review = []

    for answer in answers:
        question = questions.get(answer.question_id)

        if not question:
            continue

        review.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "selected_option": answer.selected_option,
            "correct_option": question.correct_option,
            "is_correct": (
                answer.selected_option == question.correct_option
            ),
            "explanation": question.explanation,
        })

    return review


def get_attempt_by_id(db: Session, attempt_id: int, user_id: int):
    return db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.user_id == user_id,
    ).first()


def get_attempts_by_user(db: Session, user_id: int):
    attempts = (
        db.query(
            QuizAttempt,
            Quiz.title.label("quiz_title"),
            Topic.title.label("topic_title"),
            Course.title.label("course_title"),
        )
        .join(
            Quiz,
            QuizAttempt.quiz_id == Quiz.id
        )
        .join(
            Topic,
            Quiz.topic_id == Topic.id
        )
        .join(
            Course,
            Topic.course_id == Course.id
        )
        .filter(
            QuizAttempt.user_id == user_id
        )
        .order_by(
            QuizAttempt.started_at.desc()
        )
        .all()
    )

    return [
        {
            "id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "started_at": attempt.started_at,
            "submitted_at": attempt.submitted_at,
            "quiz_title": quiz_title,
            "topic_title": topic_title,
            "course_title": course_title,
        }
        for (
            attempt,
            quiz_title,
            topic_title,
            course_title,
        ) in attempts
    ]


def get_attempt_review(db: Session, attempt_id: int, user_id: int):
    attempt = get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
        user_id=user_id,
    )

    if not attempt:
        return None

    return {
        "attempt": attempt,
        "review": build_attempt_review(db, attempt),
    }
