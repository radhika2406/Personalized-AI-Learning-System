"""AI Explainer module using Gemini API.

Generates learner-friendly explanations for incorrect quiz answers.
Uses deterministic fallback explanations whenever the LLM is unavailable
or returns an invalid response.
"""

import json
import os
import urllib.request


def call_llm(prompt: str, timeout: int = 10) -> str | None:
    """Call Gemini and return generated text, or None on failure."""

    api_key = os.environ.get("LLM_API_KEY")
    if not api_key or not api_key.strip():
        return None

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.6-flash:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "thinkingConfig": {"thinkingLevel": "minimal"},
            "temperature": 0.3,
            "maxOutputTokens": 512,
        },
    }

    try:
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return None

            data = json.loads(response.read().decode("utf-8"))

        candidates = data.get("candidates", [])
        if not candidates:
            return None

        candidate = candidates[0]

        # Do not accept truncated or blocked responses.
        if candidate.get("finishReason") != "STOP":
            return None

        parts = candidate.get("content", {}).get("parts", [])

        # Collect visible text, ignoring internal thought parts.
        visible_text = [
            part["text"].strip()
            for part in parts
            if isinstance(part, dict)
            and isinstance(part.get("text"), str)
            and part["text"].strip()
            and not part.get("thought", False)
        ]

        result = "\n".join(visible_text).strip()
        return result if result else None

    except Exception:
        # Network errors, invalid API responses, and timeouts use fallback.
        return None


def explain_wrong_answer(
    question: str,
    chosen_answer: str,
    correct_answer: str,
    explanation: str,
) -> str:
    """Explain an incorrect answer, falling back to the supplied explanation."""

    fallback_text = (
        f"You selected '{chosen_answer}', but the correct answer is "
        f"'{correct_answer}'. Explanation: {explanation}"
    )

    prompt = (
        "You are a helpful Python tutor for beginners.\n"
        "Explain the learner's mistake accurately and kindly.\n"
        "Use only the information supported by the question and key concept.\n"
        "Do not invent facts or change the correct answer.\n"
        "Keep the explanation to 2 or 3 simple sentences.\n\n"
        f"Question: {question}\n"
        f"Learner's incorrect answer: {chosen_answer}\n"
        f"Correct answer: {correct_answer}\n"
        f"Key concept: {explanation}\n\n"
        "Explain why the selected answer is incorrect and why the correct "
        "answer is right."
    )

    llm_result = call_llm(prompt)

    if llm_result and llm_result.strip():
        return llm_result.strip()

    return fallback_text
