"""
Base model class for LLM providers.

This module defines the abstract base class for LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize the LLM provider."""
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a summary from the given prompt."""
        pass

    @staticmethod
    def get_prompt_template() -> str:
        """Get the prompt template for summarizing git changes."""
        return """
        I need you to summarize the following git repository changes in clear,
        human-readable language. Focus on the high-level impact of the changes
        rather than listing every file. Group related changes when possible,
        and identify the key themes or purposes behind the commits.

        Here are the git changes to summarize:

        {git_data}

        Provide a concise but informative summary, highlighting:
        1. Main purpose/theme of these changes
        2. Key components or areas affected
        3. Any notable technical details worth mentioning

        Format your response as Markdown with appropriate headings.
        """

    def create_prompt(self, git_data: str) -> str:
        """Create a prompt for the LLM using the given git data."""
        return self.get_prompt_template().format(git_data=git_data)


class ModelError(Exception):
    """Exception raised for LLM-related errors."""
    pass