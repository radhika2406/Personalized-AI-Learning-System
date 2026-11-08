from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.quiz import Quiz


def create_question(db: Session, quiz_id: int, question_data):
    # Check whether the quiz exists
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        return None

    question = Question(
        quiz_id=quiz_id,
        question_text=question_data.question_text,
        option_a=question_data.option_a,
        option_b=question_data.option_b,
        option_c=question_data.option_c,
        option_d=question_data.option_d,
        correct_option=question_data.correct_option,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def get_questions_by_quiz(db: Session, quiz_id: int):
    return db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()


def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).filter(
        Question.id == question_id
    ).first()
