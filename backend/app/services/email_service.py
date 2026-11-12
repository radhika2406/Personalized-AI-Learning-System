
import logging
from html import escape

import httpx

from app.core.config import (
    BREVO_API_KEY,
    BREVO_SENDER_EMAIL,
    BREVO_SENDER_NAME,
    FRONTEND_URL,
)

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_welcome_email(email: str, full_name: str) -> bool:
    """Send a personalized welcome email to a newly registered learner."""

    safe_name = escape(full_name or "Learner")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:30px 15px;
                 background-color:#f5f1ff;
                 font-family:Arial,sans-serif;">

        <div style="max-width:600px; margin:auto;
                    background:#ffffff; border-radius:16px;
                    overflow:hidden;">

            <div style="background:#24143f; padding:35px 25px;
                        text-align:center; color:white;">

                <h1 style="margin:0; color:#ffffff;
                           font-size:30px;">Learnova</h1>

                <p style="color:#e4d5ff; margin-bottom:0;">
                    Your Personalized Learning Universe
                </p>
            </div>

            <div style="padding:35px 30px; color:#333333;">

                <h2 style="color:#5631a8;">
                    Welcome to the Universe of Learnova! 🚀
                </h2>

                <p>Hey <strong>{safe_name}</strong>,</p>

                <p>
                    We're delighted to have you here!
                    Your personalized learning journey starts now.
                </p>

                <h3 style="color:#5631a8;">
                    Explore your learning universe
                </h3>

                <ul style="line-height:2;">
                    <li>Discover courses based on your interests.</li>
                    <li>Follow a structured learning path.</li>
                    <li>Learn through interactive study materials.</li>
                    <li>Challenge yourself with quizzes.</li>
                    <li>Track your progress and improve every day.</li>
                </ul>

                <div style="background:#f5f0ff; padding:20px;
                            border-radius:12px; margin:25px 0;">

                    <h3 style="color:#5631a8; margin-top:0;">
                        A little learning advice 💡
                    </h3>

                    <p style="line-height:1.7; margin-bottom:0;">
                        Stay consistent, practice regularly,
                        explore new topics and celebrate every
                        small achievement.
                    </p>
                </div>

         <p style="text-align:center; margin:30px 0;">
                    <a href="{FRONTEND_URL}/dashboard"
                    style="background:#7044c5; color:white;
                    padding:14px 28px;
                    text-decoration:none;
                    border-radius:8px;
                    font-weight:bold;">
                    Start Learning
                    </a>
                    </p>

                <p>
                    Your future starts with one step.
                    Keep learning. Keep growing. Keep exploring!
                </p>

                <p style="margin-top:30px;">
                    Warm regards,<br>
                    <strong>Team Learnova 💜</strong>
                </p>

            </div>

            <div style="background:#24143f; padding:18px;
                        text-align:center; color:#e4d5ff;
                        font-size:12px;">
                © Learnova | Your Personalized Learning Universe
            </div>

        </div>
    </body>
    </html>
    """

    payload = {
        "sender": {
            "name": BREVO_SENDER_NAME,
            "email": BREVO_SENDER_EMAIL,
        },
        "to": [
            {
                "email": email,
                "name": full_name or "Learner",
            }
        ],
        "subject": "Welcome to the Universe of Learnova! 🚀",
        "htmlContent": html_content,
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    try:
        response = httpx.post(
            BREVO_API_URL,
            json=payload,
            headers=headers,
            timeout=15.0,
        )

        response.raise_for_status()

        logger.info("Welcome email sent successfully to %s", email)
        return True

    except httpx.HTTPStatusError as error:
        logger.error(
            "Brevo rejected welcome email for %s. Status: %s, Response: %s",
            email,
            error.response.status_code,
            error.response.text,
        )
        return False

    except httpx.RequestError:
        logger.exception(
            "Unable to connect to Brevo while sending welcome email to %s",
            email,
        )
        return False
