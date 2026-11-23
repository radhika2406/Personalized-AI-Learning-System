from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.ai_tutor import (
    AIChatRequest,
    AIChatResponse,
    AIConversationResponse,
    AIConversationDetailResponse,
)

from app.services.ai_tutor_service import (
    send_chat_message,
    get_user_conversations,
    get_conversation_detail,
    delete_conversation,
)

from app.services.ai_provider import AIProviderUnavailable


router = APIRouter(
    prefix="/ai-tutor",
    tags=["AI Tutor"],
)


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat_with_ai_tutor(
    chat_data: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = send_chat_message(
            db=db,
            user_id=current_user.id,
            chat_data=chat_data,
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or learning context is invalid.",
            )

        return result

    except AIProviderUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )


@router.get(
    "/history",
    response_model=list[AIConversationResponse],
)
def get_chat_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_conversations(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=AIConversationDetailResponse,
)
def get_chat_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = get_conversation_detail(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return conversation


@router.delete(
    "/conversations/{conversation_id}",
)
def remove_chat_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return {
        "message": "Conversation deleted successfully."
    }
