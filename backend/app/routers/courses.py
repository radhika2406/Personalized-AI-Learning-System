from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse
from app.services.course_service import (
    create_course,
    get_all_courses,
    get_course_by_id,
)

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_course(db, course_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get("/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return get_all_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def retrieve_course(course_id: int, db: Session = Depends(get_db)):
    course = get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return course