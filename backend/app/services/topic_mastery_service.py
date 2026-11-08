from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.topic_mastery import TopicMastery


def update_topic_mastery(
    db: Session,
    user_id: int,
    topic_id: int,
    quiz_percentage: float
):
    mastery = db.query(TopicMastery).filter(
        TopicMastery.user_id == user_id,
        TopicMastery.topic_id == topic_id
    ).first()

    if not mastery:
        mastery = TopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            mastery_score=quiz_percentage,
            quizzes_attempted=1,
            last_assessed_at=datetime.now(timezone.utc)
        )

        db.add(mastery)

    else:
        previous_attempts = mastery.quizzes_attempted

        new_mastery = (
            (mastery.mastery_score * previous_attempts)
            + quiz_percentage
        ) / (previous_attempts + 1)

        mastery.mastery_score = round(new_mastery, 2)
        mastery.quizzes_attempted += 1
        mastery.last_assessed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(mastery)

    return mastery


def get_user_topic_mastery(
    db: Session,
    user_id: int,
    topic_id: int
):
    return db.query(TopicMastery).filter(
        TopicMastery.user_id == user_id,
        TopicMastery.topic_id == topic_id
    ).first()


def get_all_user_masteries(
    db: Session,
    user_id: int
):
    return db.query(TopicMastery).filter(
        TopicMastery.user_id == user_id
    ).all()