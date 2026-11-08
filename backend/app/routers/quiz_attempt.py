from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.quiz_attempt import (
    QuizSubmission,
    QuizResultResponse,
    QuizAttemptResponse,
)
from app.services import quiz_attempt_service

router = APIRouter(
    prefix="/quiz-attempts",
    tags=["Quiz Attempts"],
)


@router.post(
    "/quiz/{quiz_id}/submit",
    response_model=QuizResultResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        attempt = quiz_attempt_service.submit_quiz(
            db=db,
            user_id=current_user.id,
            quiz_id=quiz_id,
            submission=submission,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    percentage = round(
        (attempt.score / attempt.total_questions) * 100,
        2,
    )

    return QuizResultResponse(
        attempt_id=attempt.id,
        quiz_id=attempt.quiz_id,
        score=attempt.score,
        total_questions=attempt.total_questions,
        percentage=percentage,
        submitted_at=attempt.submitted_at,
    )


@router.get("/me", response_model=list[QuizAttemptResponse])
def get_my_quiz_attempts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return quiz_attempt_service.get_attempts_by_user(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{attempt_id}", response_model=QuizAttemptResponse)
def get_my_quiz_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attempt = quiz_attempt_service.get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Quiz attempt not found",
        )

    return attempt
