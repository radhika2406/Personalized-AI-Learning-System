import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing from .env")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not GOOGLE_CLIENT_ID:
    raise ValueError("GOOGLE_CLIENT_ID is missing from .env")

# Brevo Email Configuration
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

if not BREVO_API_KEY:
    raise ValueError("BREVO_API_KEY is missing from .env")

BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME", "Learnova")

if not BREVO_SENDER_EMAIL:
    raise ValueError("BREVO_SENDER_EMAIL is missing from .env")
