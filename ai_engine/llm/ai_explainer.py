"""AI Explainer module using standard library HTTP calls.

Provides LLM-assisted explanations for incorrect quiz answers with bulletproof
fallback templates when the LLM is unavailable, offline, or times out.
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any


def call_llm(prompt: str, timeout: int = 5) -> str | None:
    """Isolated LLM caller using standard library urllib.

    Reads API key from LLM_API_KEY environment variable.
    Returns the generated response string, or None on failure, timeout, or missing key.
    """
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key or not api_key.strip():
        return None

    # Endpoint URL (configurable or standard Gemini API REST endpoint)
    # Using Gemini v1beta REST API as specified in README Tech Stack
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 200,
        },
    }

    try:
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                return None
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            # Extract candidate text
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    text = parts[0].get("text", "").strip()
                    return text if text else None
            return None

    except (urllib.error.URLError, TimeoutError, Exception):
        # Network drop, invalid key, HTTP error, or timeout -> graceful None fallback
        return None


def explain_wrong_answer(
    question: str,
    chosen_answer: str,
    correct_answer: str,
    explanation: str,
) -> str:
    """Provide a friendly explanation of why an answer was wrong.

    Falls back to a structured template built from the question's explanation field
    if the LLM is absent or unavailable.
    """
    # Deterministic fallback template
    fallback_text = (
        f"You selected '{chosen_answer}', but the correct answer is '{correct_answer}'. "
        f"Explanation: {explanation}"
    )

    prompt = (
        f"You are a helpful Python tutor for beginners.\n"
        f"Question: {question}\n"
        f"The student incorrectly chose: {chosen_answer}\n"
        f"The correct answer is: {correct_answer}\n"
        f"Key concept: {explanation}\n\n"
        f"Explain clearly in 2 friendly sentences why '{chosen_answer}' is wrong and why '{correct_answer}' is right."
    )

    llm_result = call_llm(prompt)
    if llm_result and len(llm_result.strip()) > 0:
        return llm_result.strip()

    return fallback_text
