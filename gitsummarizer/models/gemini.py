"""
Google Gemini LLM provider for GitSummarizer.
"""

import requests
from typing import Dict, Any, Optional
from .base import LLMProvider, ModelError


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Gemini provider.

        Args:
            api_key: Google API key
            model: Model to use (default: gemini-2.0-flash)
        """
        self.api_key = api_key
        self.model = model or "gemini-2.0-flash"

        if not self.api_key:
            raise ModelError("Google API key is required")

    def generate(self, prompt: str) -> str:
        """
        Generate a summary using the Google Gemini API.

        Args:
            prompt: Prompt to send to the API

        Returns:
            Generated summary
        """
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.5,
                    "maxOutputTokens": 1000
                }
            }

            response = requests.post(
                f"{api_url}?key={self.api_key}",
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]

        except requests.exceptions.RequestException as e:
            raise ModelError(f"Error calling Gemini API: {str(e)}")