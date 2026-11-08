from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.models.course import Course
from app.schemas.topic import TopicCreate


def create_topic(db: Session, topic_data: TopicCreate) -> Topic:
    # Check whether the course exists
    course = db.query(Course).filter(
        Course.id == topic_data.course_id
    ).first()

    if not course:
        raise ValueError("Course not found")

    # Create the topic
    new_topic = Topic(
        title=topic_data.title,
        description=topic_data.description,
        course_id=topic_data.course_id,
        sequence_number=topic_data.sequence_number
    )

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic


def get_topics_by_course(db: Session, course_id: int) -> list[Topic]:
    return db.query(Topic).filter(
        Topic.course_id == course_id
    ).order_by(
        Topic.sequence_number.asc(),
        Topic.id.asc()
    ).all()


def get_topic_by_id(db: Session, topic_id: int) -> Topic | None:
    return db.query(Topic).filter(
        Topic.id == topic_id
    ).first()