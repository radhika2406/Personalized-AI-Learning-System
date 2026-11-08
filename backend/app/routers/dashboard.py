from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.dashboard import (
    DashboardSummary,
    CourseDashboardSummary,
    TopicProgressSummary
)
from app.services import dashboard_service
from app.models.course import Course
from app.models.course_enrollment import CourseEnrollment


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/me", response_model=DashboardSummary)
def get_my_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return dashboard_service.get_dashboard_summary(
        db=db,
        user_id=current_user.id
    )


@router.get("/course/{course_id}", response_model=CourseDashboardSummary)
def get_course_dashboard(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check whether the course exists
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check whether the learner is enrolled
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=403,
            detail="You are not enrolled in this course"
        )

    return dashboard_service.get_course_dashboard_summary(
        db=db,
        user_id=current_user.id,
        course_id=course_id
    )

@router.get(
    "/course/{course_id}/topics",
    response_model=list[TopicProgressSummary]
)
def get_course_topics_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check whether the course exists
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check enrollment
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=403,
            detail="You are not enrolled in this course"
        )

    return dashboard_service.get_course_topic_progress(
        db=db,
        user_id=current_user.id,
        course_id=course_id
    )
