"""Unit tests for the AI Explainer module.

Tests LLM call isolation and fallback mechanisms without making external network calls.
"""

import os
import unittest
from unittest.mock import patch

from ai_engine.llm.ai_explainer import call_llm, explain_wrong_answer


class TestAiExplainer(unittest.TestCase):
    """Test wrong-answer explanations and fallback behaviors."""

    def test_missing_api_key_falls_back(self):
        """When LLM_API_KEY is not set, must return template without crashing."""
        with patch.dict(os.environ, {}, clear=True):
            explanation = explain_wrong_answer(
                question="What is the result of 2 + 2?",
                chosen_answer="5",
                correct_answer="4",
                explanation="2 plus 2 equals 4.",
            )
            self.assertIn("You selected '5'", explanation)
            self.assertIn("correct answer is '4'", explanation)
            self.assertIn("2 plus 2 equals 4.", explanation)

    def test_failing_llm_call_falls_back(self):
        """When call_llm encounters an error or network drop, must fall back cleanly."""
        with patch("ai_engine.llm.ai_explainer.call_llm", return_value=None):
            explanation = explain_wrong_answer(
                question="Which keyword defines a function?",
                chosen_answer="func",
                correct_answer="def",
                explanation="In Python, functions are defined using the 'def' keyword.",
            )
            self.assertIn("You selected 'func'", explanation)
            self.assertIn("correct answer is 'def'", explanation)
            self.assertIn("functions are defined using the 'def' keyword", explanation)

    def test_empty_llm_response_falls_back(self):
        """When call_llm returns empty whitespace, must fall back to template."""
        with patch("ai_engine.llm.ai_explainer.call_llm", return_value="   "):
            explanation = explain_wrong_answer(
                question="What does len() do?",
                chosen_answer="Deletes an item",
                correct_answer="Returns the length of an object",
                explanation="len() returns the number of items in a sequence.",
            )
            self.assertIn("You selected 'Deletes an item'", explanation)
            self.assertIn("Returns the length of an object", explanation)

    def test_successful_llm_call(self):
        """When call_llm returns a valid string, return the LLM response."""
        mock_text = "Selecting 'func' is common in other languages, but Python uses 'def' for function definitions."
        with patch("ai_engine.llm.ai_explainer.call_llm", return_value=mock_text):
            explanation = explain_wrong_answer(
                question="Which keyword defines a function?",
                chosen_answer="func",
                correct_answer="def",
                explanation="In Python, functions are defined using 'def'.",
            )
            self.assertEqual(explanation, mock_text)

    def test_call_llm_handles_network_exception(self):
        """call_llm catches all network exceptions and returns None safely."""
        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", side_effect=TimeoutError("Connection timed out")):
                result = call_llm("test prompt")
                self.assertIsNone(result)
    def test_call_llm_parses_valid_gemini_response(self):
        """A valid Gemini response should return its generated text."""
        mock_response = {
            "candidates": [
                {
                    "finishReason": "STOP",
                    "content": {
                        "parts": [{"text": "Python uses def to define functions."}]
                    }
                }
            ]
        }

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                import json
                return json.dumps(mock_response).encode("utf-8")

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Explain Python functions.")

        self.assertEqual(result, "Python uses def to define functions.")

    def test_call_llm_handles_malformed_json(self):
        """Malformed JSON from Gemini should return None safely."""

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b"not valid json"

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Test prompt")

        self.assertIsNone(result)

    def test_call_llm_handles_empty_candidates(self):
        """An empty Gemini candidates list should return None."""

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                return b'{"candidates": []}'

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Test prompt")

        self.assertIsNone(result)


    def test_call_llm_handles_multiple_text_parts(self):
        """Multiple visible Gemini text parts should be combined."""
        mock_response = {
            "candidates": [{
                "finishReason": "STOP",
                "content": {
                    "parts": [
                        {"text": "Python uses def"},
                        {"text": " to define functions."}
                    ]
                }
            }]
        }

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                import json
                return json.dumps(mock_response).encode("utf-8")

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Explain Python functions.")

        self.assertEqual(result, "Python uses def\nto define functions.")

    def test_call_llm_ignores_thought_parts(self):
        """Internal thought parts should not appear in the returned answer."""
        mock_response = {
            "candidates": [{
                "finishReason": "STOP",
                "content": {
                    "parts": [
                        {"text": "Internal reasoning", "thought": True},
                        {"text": "Python uses def to define functions."}
                    ]
                }
            }]
        }

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                import json
                return json.dumps(mock_response).encode("utf-8")

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Explain Python functions.")

        self.assertEqual(result, "Python uses def to define functions.")

    def test_call_llm_rejects_truncated_response(self):
        """A response stopped by the token limit should return None."""
        mock_response = {
            "candidates": [{
                "finishReason": "MAX_TOKENS",
                "content": {
                    "parts": [{"text": "Incomplete explanation"}]
                }
            }]
        }

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                import json
                return json.dumps(mock_response).encode("utf-8")

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Explain Python functions.")

        self.assertIsNone(result)

    def test_call_llm_rejects_thought_only_response(self):
        """A response containing only internal thoughts should return None."""
        mock_response = {
            "candidates": [{
                "finishReason": "STOP",
                "content": {
                    "parts": [
                        {"text": "Internal reasoning", "thought": True}
                    ]
                }
            }]
        }

        class MockHttpResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self):
                import json
                return json.dumps(mock_response).encode("utf-8")

        with patch.dict(os.environ, {"LLM_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen", return_value=MockHttpResponse()):
                result = call_llm("Explain Python functions.")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
