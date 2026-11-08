from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate


def create_recommendation(
    db: Session,
    user_id: int,
    recommendation_data: RecommendationCreate,
) -> Recommendation:

    new_recommendation = Recommendation(
        user_id=user_id,
        course_id=recommendation_data.course_id,
        topic_id=recommendation_data.topic_id,
        recommendation_type=recommendation_data.recommendation_type,
        title=recommendation_data.title,
        description=recommendation_data.description,
        reason=recommendation_data.reason,
        priority=recommendation_data.priority,
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return new_recommendation


def get_user_recommendations(
    db: Session,
    user_id: int,
) -> list[Recommendation]:

    return db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(
        Recommendation.priority.desc(),
        Recommendation.created_at.desc()
    ).all()


def get_recommendation_by_id(
    db: Session,
    recommendation_id: int,
    user_id: int,
) -> Recommendation | None:

    return db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == user_id
    ).first()


def update_recommendation_status(
    db: Session,
    recommendation: Recommendation,
    new_status: str,
) -> Recommendation:

    recommendation.status = new_status

    db.commit()
    db.refresh(recommendation)

    return recommendation