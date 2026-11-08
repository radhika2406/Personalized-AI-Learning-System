
from sqlalchemy.orm import Session

from app.models.course_enrollment import CourseEnrollment
from app.models.learning_progress import LearningProgress
from app.models.learning_material import LearningMaterial
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.topic import Topic
from app.models.topic_mastery import TopicMastery


def get_dashboard_summary(db: Session, user_id: int):
    enrolled_courses = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id
    ).count()

    completed_materials = db.query(LearningProgress).filter(
        LearningProgress.user_id == user_id,
        LearningProgress.status == "completed"
    ).count()

    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id
    ).all()

    quizzes_attempted = len(quiz_attempts)

    valid_attempts = [
        attempt for attempt in quiz_attempts
        if attempt.total_questions > 0
    ]

    if valid_attempts:
        average_quiz_percentage = round(
            sum(
                (attempt.score / attempt.total_questions) * 100
                for attempt in valid_attempts
            ) / len(valid_attempts),
            2
        )
    else:
        average_quiz_percentage = 0.0

    masteries = db.query(TopicMastery).filter(
        TopicMastery.user_id == user_id
    ).all()

    topics_tracked = len(masteries)

    if topics_tracked:
        average_topic_mastery = round(
            sum(mastery.mastery_score for mastery in masteries)
            / topics_tracked,
            2
        )
    else:
        average_topic_mastery = 0.0

    return {
        "enrolled_courses": enrolled_courses,
        "learning_materials_completed": completed_materials,
        "quizzes_attempted": quizzes_attempted,
        "average_quiz_percentage": average_quiz_percentage,
        "topics_tracked": topics_tracked,
        "average_topic_mastery": average_topic_mastery
    }


def get_course_dashboard_summary(
    db: Session,
    user_id: int,
    course_id: int
):
    # Get all topic IDs belonging to this course
    topic_ids = [
        topic.id
        for topic in db.query(Topic).filter(
            Topic.course_id == course_id
        ).all()
    ]

    # Count learning materials in this course
    total_learning_materials = db.query(LearningMaterial).filter(
        LearningMaterial.topic_id.in_(topic_ids)
    ).count()

    # Count completed learning materials for this user
    completed_learning_materials = db.query(LearningProgress).join(
        LearningMaterial,
        LearningProgress.learning_material_id == LearningMaterial.id
    ).filter(
        LearningProgress.user_id == user_id,
        LearningProgress.status == "completed",
        LearningMaterial.topic_id.in_(topic_ids)
    ).count()

    # Calculate material completion percentage
    if total_learning_materials > 0:
        completion_percentage = round(
            (completed_learning_materials / total_learning_materials) * 100,
            2
        )
    else:
        completion_percentage = 0.0

    # Get quiz attempts for quizzes belonging to this course
    quiz_attempts = db.query(QuizAttempt).join(
        Quiz,
        QuizAttempt.quiz_id == Quiz.id
    ).filter(
        Quiz.topic_id.in_(topic_ids),
        QuizAttempt.user_id == user_id
    ).all()

    quizzes_attempted = len(quiz_attempts)

    valid_attempts = [
        attempt for attempt in quiz_attempts
        if attempt.total_questions > 0
    ]

    if valid_attempts:
        average_quiz_percentage = round(
            sum(
                (attempt.score / attempt.total_questions) * 100
                for attempt in valid_attempts
            ) / len(valid_attempts),
            2
        )
    else:
        average_quiz_percentage = 0.0

    # Get mastery records for topics in this course
    masteries = db.query(TopicMastery).filter(
        TopicMastery.user_id == user_id,
        TopicMastery.topic_id.in_(topic_ids)
    ).all()

    topics_tracked = len(masteries)

    if topics_tracked:
        average_topic_mastery = round(
            sum(mastery.mastery_score for mastery in masteries)
            / topics_tracked,
            2
        )
    else:
        average_topic_mastery = 0.0

    return {
        "course_id": course_id,
        "total_learning_materials": total_learning_materials,
        "completed_learning_materials": completed_learning_materials,
        "learning_material_completion_percentage": completion_percentage,
        "quizzes_attempted": quizzes_attempted,
        "average_quiz_percentage": average_quiz_percentage,
        "topics_tracked": topics_tracked,
        "average_topic_mastery": average_topic_mastery
    }


def get_course_topic_progress(
    db: Session,
    user_id: int,
    course_id: int
):
    # Get topics belonging to the course in learning order
    topics = db.query(Topic).filter(
        Topic.course_id == course_id
    ).order_by(
        Topic.sequence_number.asc(),
        Topic.id.asc()
    ).all()

    topic_progress = []

    for topic in topics:
        # Count materials belonging to this topic
        total_materials = db.query(LearningMaterial).filter(
            LearningMaterial.topic_id == topic.id
        ).count()

        # Count completed materials for this learner
        completed_materials = db.query(LearningProgress).join(
            LearningMaterial,
            LearningProgress.learning_material_id == LearningMaterial.id
        ).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.status == "completed",
            LearningMaterial.topic_id == topic.id
        ).count()

        # Calculate completion percentage
        if total_materials > 0:
            completion_percentage = round(
                (completed_materials / total_materials) * 100,
                2
            )
        else:
            completion_percentage = 0.0

        # Count quiz attempts for this topic
        quizzes_attempted = db.query(QuizAttempt).join(
            Quiz,
            QuizAttempt.quiz_id == Quiz.id
        ).filter(
            Quiz.topic_id == topic.id,
            QuizAttempt.user_id == user_id
        ).count()

        # Get mastery score for this topic
        mastery = db.query(TopicMastery).filter(
            TopicMastery.user_id == user_id,
            TopicMastery.topic_id == topic.id
        ).first()

        mastery_score = mastery.mastery_score if mastery else 0.0

        topic_progress.append({
            "topic_id": topic.id,
            "topic_title": topic.title,
            "sequence_number": topic.sequence_number,
            "total_learning_materials": total_materials,
            "completed_learning_materials": completed_materials,
            "completion_percentage": completion_percentage,
            "quizzes_attempted": quizzes_attempted,
            "mastery_score": mastery_score
        })

    return topic_progress

