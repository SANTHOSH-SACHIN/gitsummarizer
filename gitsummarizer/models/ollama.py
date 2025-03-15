"""
Ollama local LLM provider for GitSummarizer.
"""

import requests
from typing import Dict, Any, Optional
from .base import LLMProvider, ModelError


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Ollama provider.

        Args:
            api_key: Not used for Ollama
            model: Model to use (default: llama3)
        """
        self.model = model or "llama3"
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        """
        Generate a summary using the local Ollama instance.

        Args:
            prompt: Prompt to send to Ollama

        Returns:
            Generated summary
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            result = response.json()
            return result["response"]

        except requests.exceptions.RequestException as e:
            raise ModelError(f"Error calling Ollama API: {str(e)}. Make sure Ollama is running locally.")