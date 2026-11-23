from sqlalchemy.orm import Session

from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage
from datetime import datetime, timezone
from app.models.course import Course
from app.models.topic import Topic
from app.services.ai_provider import (
    generate_ai_response,
)


def validate_learning_context(
    db: Session,
    course_id: int | None,
    topic_id: int | None,
) -> bool:
    """Validate optional course and topic context."""

    if course_id is not None:
        course = db.query(Course).filter(
            Course.id == course_id
        ).first()

        if not course:
            return False

    if topic_id is not None:
        topic = db.query(Topic).filter(
            Topic.id == topic_id
        ).first()

        if not topic:
            return False

        if course_id is None or topic.course_id != course_id:
            return False

    return True


def send_chat_message(
    db: Session,
    user_id: int,
    chat_data,
):
    """Generate and save a user/assistant message pair."""

    conversation = None

    if chat_data.conversation_id is not None:
        conversation = db.query(AIConversation).filter(
            AIConversation.id == chat_data.conversation_id,
            AIConversation.user_id == user_id,
        ).first()

        if not conversation:
            return None

        # A follow-up cannot silently change conversation context.
        if (
            chat_data.course_id is not None
            and chat_data.course_id != conversation.course_id
        ):
            return None

        if (
            chat_data.topic_id is not None
            and chat_data.topic_id != conversation.topic_id
        ):
            return None

        course_id = conversation.course_id
        topic_id = conversation.topic_id

    else:
        course_id = chat_data.course_id
        topic_id = chat_data.topic_id

        if not validate_learning_context(
            db,
            course_id,
            topic_id,
        ):
            return None

    history = []

    if conversation is not None:
        previous_messages = db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation.id
        ).order_by(
            AIMessage.created_at.asc(),
            AIMessage.id.asc(),
        ).all()

        history = [
            {
                "role": item.role,
                "content": item.content,
            }
            for item in previous_messages
        ]

    # Generate the answer before saving anything.
    # If the provider is unavailable, no partial exchange is stored.
    assistant_content = generate_ai_response(
        message=chat_data.message,
        course_id=course_id,
        topic_id=topic_id,
        history=history,
    )

    if not isinstance(assistant_content, str) or not assistant_content.strip():
        raise ValueError("AI provider returned an empty response.")

    try:
        if conversation is None:
            title = " ".join(chat_data.message.split())[:200]

            conversation = AIConversation(
                user_id=user_id,
                course_id=course_id,
                topic_id=topic_id,
                title=title,
            )

            db.add(conversation)
            db.flush()

        user_message = AIMessage(
            conversation_id=conversation.id,
            role="user",
            content=chat_data.message,
        )

        assistant_message = AIMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_content.strip(),
        )

        db.add(user_message)
        db.add(assistant_message)
        conversation.updated_at = datetime.now(timezone.utc)

        db.commit()

        db.refresh(conversation)
        db.refresh(user_message)
        db.refresh(assistant_message)

        return {
            "conversation_id": conversation.id,
            "user_message": user_message,
            "assistant_message": assistant_message,
        }

    except Exception:
        db.rollback()
        raise


def get_user_conversations(
    db: Session,
    user_id: int,
    limit: int = 20,
    offset: int = 0,
):
    return db.query(AIConversation).filter(
        AIConversation.user_id == user_id
    ).order_by(
        AIConversation.updated_at.desc(),
        AIConversation.id.desc(),
    ).offset(
        offset
    ).limit(
        limit
    ).all()


def get_conversation_detail(
    db: Session,
    conversation_id: int,
    user_id: int,
):
    conversation = db.query(AIConversation).filter(
        AIConversation.id == conversation_id,
        AIConversation.user_id == user_id,
    ).first()

    if not conversation:
        return None

    messages = db.query(AIMessage).filter(
        AIMessage.conversation_id == conversation.id
    ).order_by(
        AIMessage.created_at.asc(),
        AIMessage.id.asc(),
    ).all()

    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "course_id": conversation.course_id,
        "topic_id": conversation.topic_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": messages,
    }


def delete_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
) -> bool:
    conversation = db.query(AIConversation).filter(
        AIConversation.id == conversation_id,
        AIConversation.user_id == user_id,
    ).first()

    if not conversation:
        return False

    try:
        db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation.id
        ).delete(synchronize_session=False)

        db.delete(conversation)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise
