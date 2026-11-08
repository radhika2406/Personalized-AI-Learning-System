from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.course_enrollment import CourseEnrollmentResponse
from app.services import course_enrollment_service


router = APIRouter(
    prefix="/enrollments",
    tags=["Course Enrollment"]
)


@router.post(
    "/courses/{course_id}",
    response_model=CourseEnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    enrollment, error = course_enrollment_service.enroll_user_in_course(
        db=db,
        user_id=current_user.id,
        course_id=course_id
    )

    if error == "Course not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Already enrolled in this course":
        raise HTTPException(
            status_code=409,
            detail=error
        )

    return enrollment


@router.get(
    "/me",
    response_model=list[CourseEnrollmentResponse]
)
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return course_enrollment_service.get_user_enrollments(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/courses/{course_id}",
    response_model=CourseEnrollmentResponse
)
def get_my_course_enrollment(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    enrollment = course_enrollment_service.get_user_course_enrollment(
        db=db,
        user_id=current_user.id,
        course_id=course_id
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


@router.delete(
    "/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def unenroll_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = course_enrollment_service.unenroll_user_from_course(
        db=db,
        user_id=current_user.id,
        course_id=course_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )