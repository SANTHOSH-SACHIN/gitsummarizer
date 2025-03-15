"""
LLM provider models for GitSummarizer.
"""

from .base import LLMProvider, ModelError
from .groq import GroqProvider
from .openai import OpenAIProvider
from .gemini import GeminiProvider
from .ollama import OllamaProvider

# Map of provider names to provider classes
PROVIDERS = {
    "groq": GroqProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "ollama": OllamaProvider
}


def get_provider(provider_name: str, api_key=None, model=None) -> LLMProvider:
    """
    Get a provider instance by name.

    Args:
        provider_name: Name of the provider
        api_key: API key for the provider
        model: Model to use

    Returns:
        Provider instance
    """
    if provider_name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_name}")

    provider_class = PROVIDERS[provider_name]
    return provider_class(api_key=api_key, model=model)