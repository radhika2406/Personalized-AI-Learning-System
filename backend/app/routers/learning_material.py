from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.learning_material import (
    LearningMaterialCreate,
    LearningMaterialResponse,
)
from app.services.learning_material_service import (
    create_learning_material,
    get_materials_by_topic,
    get_learning_material_by_id,
)

router = APIRouter(
    prefix="/learning-materials",
    tags=["Learning Materials"]
)


@router.post(
    "/",
    response_model=LearningMaterialResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_learning_material(
    material_data: LearningMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_learning_material(db, material_data)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    "/topic/{topic_id}",
    response_model=list[LearningMaterialResponse]
)
def list_topic_materials(
    topic_id: int,
    db: Session = Depends(get_db),
):
    return get_materials_by_topic(db, topic_id)


@router.get(
    "/{material_id}",
    response_model=LearningMaterialResponse
)
def get_learning_material(
    material_id: int,
    db: Session = Depends(get_db),
):
    material = get_learning_material_by_id(db, material_id)

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Learning material not found"
        )

    return material
