
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
)
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

# Profile image storage
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "profile_images"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def delete_old_image(image_path: str | None):
    if not image_path:
        return

    filename = Path(image_path).name
    file_path = (UPLOAD_DIR / filename).resolve()

    if file_path.parent == UPLOAD_DIR.resolve() and file_path.is_file():
        file_path.unlink()


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
        user = create_user(db, user_data)

        try:
            send_welcome_email(
                email=user.email,
                full_name=user.full_name,
            )
        except Exception:
            import logging
            logging.exception("Unable to send registration welcome email.")

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


@router.post("/me/profile-image", response_model=UserResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    extension = ALLOWED_TYPES.get(file.content_type)

    if not extension:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed.",
        )

    image_data = await file.read(MAX_FILE_SIZE + 1)

    if not image_data:
        raise HTTPException(status_code=400, detail="The image is empty.")

    if len(image_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image size must not exceed 5 MB.",
        )

    # Check actual image format, not only the supplied MIME type.
    signatures = {
        "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
        "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/webp": lambda data: (
            len(data) >= 12
            and data.startswith(b"RIFF")
            and data[8:12] == b"WEBP"
        ),
    }

    if not signatures[file.content_type](image_data):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        )

    filename = f"user_{current_user.id}_{uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename

    try:
        destination.write_bytes(image_data)

        old_image = current_user.profile_image

        current_user.profile_image = (
            f"/uploads/profile_images/{filename}"
        )

        db.commit()
        db.refresh(current_user)

    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise

    delete_old_image(old_image)

    return current_user


@router.delete("/me/profile-image", response_model=UserResponse)
def remove_profile_image(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    old_image = current_user.profile_image

    if not old_image:
        return current_user

    try:
        current_user.profile_image = None
        db.commit()
        db.refresh(current_user)
    except Exception:
        db.rollback()
        raise

    delete_old_image(old_image)

    return current_user
