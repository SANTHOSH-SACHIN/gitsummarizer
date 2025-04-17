"""Test model functionality."""

from unittest import TestCase, mock
from gitsummarizer.models.base import LLMProvider
from gitsummarizer import config

class TestLLMProvider(TestCase):
    """Test LLMProvider base class functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create a concrete implementation of the abstract base class for testing
        class ConcreteLLMProvider(LLMProvider):
            def __init__(self, api_key=None, model=None):
                pass

            def generate(self, prompt: str) -> str:
                return f"Generated: {prompt}"

        self.provider = ConcreteLLMProvider()

    def test_prompt_template_usage(self):
        """Test that LLMProvider uses configured prompt templates."""
        # Set up a custom template
        custom_template = "Custom summary for: {git_data}"
        config.set_prompt_template("custom", custom_template)
        config.set_active_template("custom")

        # Test that create_prompt uses the custom template
        git_data = "test commit data"
        prompt = self.provider.create_prompt(git_data)
        self.assertEqual(prompt, custom_template.format(git_data=git_data))

    def test_default_template(self):
        """Test that default template is used when appropriate."""
        # Test when "default" is active template
        config.set_active_template("default")
        git_data = "test commit data"
        prompt = self.provider.create_prompt(git_data)
        self.assertEqual(prompt, LLMProvider.DEFAULT_TEMPLATE.format(git_data=git_data))

        # Test when non-existent template is active
        config.set_active_template("nonexistent")
        prompt = self.provider.create_prompt(git_data)
        self.assertEqual(prompt, LLMProvider.DEFAULT_TEMPLATE.format(git_data=git_data))

    def test_template_formatting(self):
        """Test template formatting with git data."""
        git_data = "commit 1\ncommit 2"
        prompt = self.provider.create_prompt(git_data)
        self.assertIn(git_data, prompt)
