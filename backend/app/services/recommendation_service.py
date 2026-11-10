from sqlalchemy.orm import Session
from app.models.learning_progress import LearningProgress
from app.models.learning_material import LearningMaterial
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate
from app.models.topic import Topic


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

def generate_user_recommendations(
    db: Session,
    user_id: int,
) -> list[Recommendation]:

    generated = []

    # Get topics where the user has attempted quizzes
    quiz_data = db.query(
        Quiz.topic_id,
        QuizAttempt.score,
        QuizAttempt.total_questions,
    ).join(
        QuizAttempt,
        QuizAttempt.quiz_id == Quiz.id,
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.total_questions > 0,
    ).all()

    topic_scores = {}

    for topic_id, score, total in quiz_data:
        topic_scores.setdefault(topic_id, []).append(
            (score / total) * 100
        )

    # Analyze quiz performance
    for topic_id, scores in topic_scores.items():
        course_id = db.query(Topic.course_id).filter(
            Topic.id == topic_id
        ).scalar()
        average = sum(scores) / len(scores)
        low_score_attempts = sum(
            1 for score in scores if score < 60
        )

        if average < 60:
            title = "Revise Topic"
            description = (
                "Review the learning materials for this topic "
                "and attempt its quiz again."
            )

            reason = (
                f"Your average quiz score for this topic "
                f"is {average:.1f}%. "
                f"You have {low_score_attempts} low-score attempts."
            )

            if average < 40 or low_score_attempts >= 3:
                priority = 4
            else:
                priority = 3

        elif average >= 80:
            title = "Strengthen Your Learning"
            description = (
                "Continue practicing this topic to maintain "
                "your strong understanding."
            )
            reason = (
                f"Your average quiz score for this topic "
                f"is {average:.1f}%."
            )
            priority = 1

        else:
            continue

        existing = db.query(Recommendation).filter(
            Recommendation.user_id == user_id,
            Recommendation.topic_id == topic_id,
            Recommendation.recommendation_type == "quiz_performance",
            Recommendation.status == "pending",
        ).first()

        if existing:
            existing.title = title
            existing.description = description
            existing.reason = reason
            existing.priority = priority
            existing.course_id = course_id
            generated.append(existing)
            continue

        recommendation = Recommendation(
            user_id=user_id,
            topic_id=topic_id,
            course_id=course_id,
            recommendation_type="quiz_performance",
            title=title,
            description=description,
            reason=reason,
            priority=priority,
            
        )

        db.add(recommendation)
        generated.append(recommendation)

    
    # Resolve outdated learning recommendations
    pending_learning_recommendations = db.query(
        Recommendation
    ).filter(
        Recommendation.user_id == user_id,
        Recommendation.recommendation_type == "learning_progress",
        Recommendation.status == "pending",
    ).all()

    for recommendation in pending_learning_recommendations:

        topic_material_ids = db.query(
            LearningMaterial.id
        ).filter(
            LearningMaterial.topic_id == recommendation.topic_id
        ).all()

        material_ids = [row[0] for row in topic_material_ids]

        if not material_ids:
            recommendation.status = "completed"
            continue

        completed_count = db.query(
            LearningProgress
        ).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.learning_material_id.in_(material_ids),
            LearningProgress.status == "completed",
        ).count()

        if completed_count == len(material_ids):
            recommendation.status = "completed"

    # Analyze unfinished learning materials
    unfinished = db.query(
        LearningMaterial.topic_id,
    LearningMaterial.id,
    LearningMaterial.title,
    LearningProgress.status,
).outerjoin(
    LearningProgress,
    (LearningProgress.learning_material_id == LearningMaterial.id)
    & (LearningProgress.user_id == user_id),
).filter(
    (LearningProgress.id == None)
    | (LearningProgress.status != "completed")
).all()

    unfinished_topics = {}

    for topic_id, material_id, material_title, progress_status in unfinished:
        unfinished_topics.setdefault(topic_id, []).append(material_title)

    for topic_id, materials in unfinished_topics.items():
        course_id = db.query(Topic.course_id).filter(
            Topic.id == topic_id
        ).scalar()

        existing = db.query(Recommendation).filter(
            Recommendation.user_id == user_id,
            Recommendation.topic_id == topic_id,
            Recommendation.recommendation_type == "learning_progress",
            Recommendation.status == "pending",
        ).first()

        if existing:
            existing.title = "Continue Learning"
            existing.description = (
                f"You have {len(materials)} unfinished "
                f"learning material(s) in this topic."
            )
            existing.reason = (
                "Complete your remaining learning materials."
            )
            existing.priority = 2
            existing.course_id = course_id

            generated.append(existing)
            continue

        recommendation = Recommendation(
            user_id=user_id,
            topic_id=topic_id,
            course_id=course_id,
            recommendation_type="learning_progress",
            title="Continue Learning",
            description=(
                f"You have {len(materials)} unfinished "
                f"learning material(s) in this topic."
            ),
            reason="Complete your remaining learning materials.",
            priority=2,
        )

        db.add(recommendation)
        generated.append(recommendation)

    db.commit()

    for recommendation in generated:
        db.refresh(recommendation)

    return generated
