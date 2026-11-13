from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user, create_access_token
from app.models.user import User
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, RegistrationResponse
from app.services.email_service import send_welcome_email
from app.services.user_service import create_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        # Create and save the new user.
        user = create_user(db, user_data)

        # Send welcome email after successful registration.
        try:
            send_welcome_email(
                email=user.email,
                full_name=user.full_name,
            )
        except Exception:
            import logging
            logging.exception("Unable to send registration welcome email.")

        # Generate JWT for the newly registered user.
        access_token = create_access_token(user.id)

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "is_active": user.is_active,
            "access_token": access_token,
            "token_type": "bearer",
            "is_new_user": True,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
