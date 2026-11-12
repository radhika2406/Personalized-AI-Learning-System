from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError

from app.core.security import get_current_user, create_access_token
from app.core.config import GOOGLE_CLIENT_ID
from app.db.database import get_db
from app.models.user import User
from app.services.email_service import send_welcome_email
from app.schemas.user import LoginRequest, TokenResponse, GoogleLoginRequest
from app.services.user_service import authenticate_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Existing email/password login
@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=str(credentials.email),
        password=credentials.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# Google login
@router.post("/google", response_model=TokenResponse)
def google_login(
    credentials: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    try:
        google_user = id_token.verify_oauth2_token(
            credentials.credential,
            Request(),
            GOOGLE_CLIENT_ID,
        )
    except (ValueError, GoogleAuthError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Google token",
        )

    # Verify that Google has verified the email address.
    if not google_user.get("email_verified"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google email is not verified",
        )

    google_id = google_user.get("sub")
    email = google_user.get("email")
    full_name = google_user.get("name")

    if not google_id or not email or not full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required Google account information is missing",
        )

    # First, look for an existing Google-linked account.
    user = (
        db.query(User)
        .filter(User.google_id == google_id)
        .first()
    )

    if user:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

    else:
        # Check whether this email already has a password account.
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            if not existing_user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user",
                )

            # Link the verified Google identity to the existing account.
            if existing_user.google_id and existing_user.google_id != google_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This email is already linked to another Google account.",
                )

            existing_user.google_id = google_id

            try:
                db.commit()
                db.refresh(existing_user)
            except Exception:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unable to link your Google account.",
                )

            user = existing_user


        else:
    # Create a new Google-only account.
          user = User(
            full_name=full_name[:100],
            email=email,
            google_id=google_id,
            password_hash=None,
            is_active=True,
           )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create your Google account.",
        )

    # Send welcome email only to newly registered Google users.
    try:
        send_welcome_email(
            email=user.email,
            full_name=user.full_name,
        )
    except Exception:
        import logging
        logging.exception("Unexpected error while sending Google welcome email.")

    # Use the existing Learnova JWT authentication system.
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
