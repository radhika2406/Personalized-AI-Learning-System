from sqlalchemy.orm import Session

from app.models.learning_material import LearningMaterial
from app.models.topic import Topic
from app.schemas.learning_material import LearningMaterialCreate


def create_learning_material(
    db: Session,
    material_data: LearningMaterialCreate
) -> LearningMaterial:

    # Check whether the topic exists
    topic = db.query(Topic).filter(
        Topic.id == material_data.topic_id
    ).first()

    if not topic:
        raise ValueError("Topic not found")

    # Create learning material
    new_material = LearningMaterial(
        title=material_data.title,
        description=material_data.description,
        material_type=material_data.material_type,
        content_text=material_data.content_text,
        content_url=(
            str(material_data.content_url)
            if material_data.content_url
            else None
        ),
        topic_id=material_data.topic_id
    )

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return new_material


def get_materials_by_topic(
    db: Session,
    topic_id: int
) -> list[LearningMaterial]:

    return db.query(LearningMaterial).filter(
        LearningMaterial.topic_id == topic_id
    ).order_by(LearningMaterial.id).all()


def get_learning_material_by_id(
    db: Session,
    material_id: int
) -> LearningMaterial | None:

    return db.query(LearningMaterial).filter(
        LearningMaterial.id == material_id
    ).first()
