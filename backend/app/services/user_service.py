from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    new_user = User(
        full_name=user_data.full_name,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
