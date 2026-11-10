from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.topic import Topic
from app.models.learning_material import LearningMaterial
from app.models.learning_progress import LearningProgress

router = APIRouter(
    prefix="/learning-path",
    tags=["Learning Path"]
)


@router.get("/course/{course_id}")
def get_learning_path(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    topics = (
        db.query(Topic)
        .filter(Topic.course_id == course_id)
        .order_by(Topic.sequence_number)
        .all()
    )

    if not topics:
        raise HTTPException(
            status_code=404,
            detail="No topics found for this course"
        )

    learning_path = []
    next_topic_found = False

    for topic in topics:
        materials = (
            db.query(LearningMaterial)
            .filter(LearningMaterial.topic_id == topic.id)
            .all()
        )

        topic_materials = []
        completed_count = 0

        for material in materials:
            progress = (
                db.query(LearningProgress)
                .filter(
                    LearningProgress.user_id == current_user.id,
                    LearningProgress.learning_material_id == material.id
                )
                .first()
            )

            status = progress.status if progress else "not_started"

            if status == "completed":
                completed_count += 1

            topic_materials.append({
                "material_id": material.id,
                "title": material.title,
                "material_type": material.material_type,
                "status": status
            })

        total_materials = len(materials)

        completion_percentage = (
            (completed_count / total_materials) * 100
            if total_materials > 0 else 0
        )

        if not next_topic_found and completion_percentage < 100:
            topic_status = "current"
            next_topic_found = True
        elif completion_percentage == 100:
            topic_status = "completed"
        else:
            topic_status = "upcoming"

        learning_path.append({
            "topic_id": topic.id,
            "topic_title": topic.title,
            "sequence_number": topic.sequence_number,
            "total_materials": total_materials,
            "completed_materials": completed_count,
            "completion_percentage": round(completion_percentage, 2),
            "status": topic_status,
            "materials": topic_materials
        })

    return {
        "course_id": course_id,
        "total_topics": len(learning_path),
        "learning_path": learning_path
    }
