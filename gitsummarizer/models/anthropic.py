"""
Anthropic Claude model implementation for GitSummarizer.
"""

from typing import Optional
import anthropic
from .base import LLMProvider, ModelError


class AnthropicModel(LLMProvider):
    """Anthropic Claude model implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the Anthropic client."""
        self.api_key = api_key
        self.model = model or "claude-3-sonnet-20240229"
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        """Generate a summary using Anthropic Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise ModelError(f"Anthropic API error: {str(e)}") from e
