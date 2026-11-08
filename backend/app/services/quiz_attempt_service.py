from datetime import datetime, timezone
from app.services import topic_mastery_service
from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_answer import QuizAnswer


def submit_quiz(db: Session, user_id: int, quiz_id: int, submission):
    # Check whether the quiz exists
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        return None

    # Get all questions belonging to this quiz
    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    if not questions:
        raise ValueError("This quiz has no questions")

    # Prevent duplicate answers for the same question
    question_ids = [answer.question_id for answer in submission.answers]

    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Duplicate question answers are not allowed")

    # Validate submitted question IDs
    question_map = {question.id: question for question in questions}

    for answer in submission.answers:
        if answer.question_id not in question_map:
            raise ValueError(
                "A submitted question does not belong to this quiz"
            )

    # Create the quiz attempt
    attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=0,
        total_questions=len(questions),
    )

    db.add(attempt)
    db.flush()

    score = 0

    # Save submitted answers and calculate score
    for answer in submission.answers:
        question = question_map[answer.question_id]

        if answer.selected_option == question.correct_option:
            score += 1

        quiz_answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=answer.question_id,
            selected_option=answer.selected_option,
        )

        db.add(quiz_answer)

    # Update attempt result
        attempt.score = score
    attempt.submitted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(attempt)

    quiz_percentage = round(
        (attempt.score / attempt.total_questions) * 100,
        2
    )

    topic_mastery_service.update_topic_mastery(
        db=db,
        user_id=user_id,
        topic_id=quiz.topic_id,
        quiz_percentage=quiz_percentage
    )

    return attempt


def get_attempt_by_id(db: Session, attempt_id: int, user_id: int):
    return db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.user_id == user_id,
    ).first()


def get_attempts_by_user(db: Session, user_id: int):
    return db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id
    ).order_by(QuizAttempt.started_at.desc()).all()
