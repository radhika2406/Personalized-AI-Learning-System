from sqlalchemy.orm import Session

from app.models.quiz import Quiz
from app.models.topic import Topic

def create_quiz(db: Session, quiz_data):
    # Check whether the topic exists
    topic = db.query(Topic).filter(
        Topic.id == quiz_data.topic_id
    ).first()

    if not topic:
        return None

    quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        topic_id=quiz_data.topic_id,
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz


def get_quiz_by_id(db: Session, quiz_id: int):
    return db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()


def get_quizzes_by_topic(db: Session, topic_id: int):
    return db.query(Quiz).filter(
        Quiz.topic_id == topic_id
    ).all()
