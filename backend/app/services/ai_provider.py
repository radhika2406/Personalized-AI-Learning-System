class AIProviderUnavailable(Exception):
    """Raised when the AI/ML provider is not configured or unavailable."""


def generate_ai_response(
    message: str,
    course_id: int | None = None,
    topic_id: int | None = None,
    history: list[dict[str, str]] | None = None,
) -> str:
    """
    Integration interface for the Learnova AI/ML module.

    Replace this implementation only after the AI/ML team confirms
    its request and response contract.
    """

    raise AIProviderUnavailable(
        "AI Tutor is not connected to the AI service yet."
    )
