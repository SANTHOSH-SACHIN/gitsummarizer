"""
Groq LLM provider for GitSummarizer.
"""

import requests
from typing import Dict, Any, Optional
from .base import LLMProvider, ModelError


class GroqProvider(LLMProvider):
    """Groq LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Groq provider.

        Args:
            api_key: Groq API key
            model: Model to use (default: llama-3.1-8b-instant)
        """
        self.api_key = api_key
        self.model = model or "llama-3.1-8b-instant"

        if not self.api_key:
            raise ModelError("Groq API key is required")

    def generate(self, prompt: str) -> str:
        """
        Generate a summary using the Groq API.

        Args:
            prompt: Prompt to send to the API

        Returns:
            Generated summary
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 1000
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise ModelError(f"Error calling Groq API: {str(e)}")
