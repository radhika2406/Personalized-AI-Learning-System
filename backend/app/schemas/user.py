from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    profile_image: str | None = None

    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_new_user: bool = False

class GoogleLoginRequest(BaseModel):
    credential: str = Field(min_length=1)


class RegistrationResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    access_token: str
    token_type: str = "bearer"
    is_new_user: bool = True
