from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.quiz import QuizCreate, QuizResponse
from app.schemas.question import QuestionCreate, QuestionResponse
from app.services import quiz_service, question_service

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quiz = quiz_service.create_quiz(db, quiz_data)

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )

    return quiz


@router.get("/topic/{topic_id}", response_model=list[QuizResponse])
def get_quizzes_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return quiz_service.get_quizzes_by_topic(db, topic_id)


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quiz = quiz_service.get_quiz_by_id(db, quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return quiz


@router.post(
    "/{quiz_id}/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_question(
    quiz_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    question = question_service.create_question(
        db,
        quiz_id,
        question_data
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return question


@router.get(
    "/{quiz_id}/questions",
    response_model=list[QuestionResponse]
)
def get_questions_by_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quiz = quiz_service.get_quiz_by_id(db, quiz_id)

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return question_service.get_questions_by_quiz(db, quiz_id)
