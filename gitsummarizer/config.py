"""
Configuration module for GitSummarizer.

Handles loading, saving, and managing user configurations.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Configuration constants
CONFIG_DIR = Path.home() / ".config" / "gitsumm"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "provider": "groq",  # Default LLM provider
    "api_keys": {},
    "model_preferences": {
        "groq": "llama-3.2-1b-preview",
        "openai": "gpt-4o",
        "gemini": "gemini-2.0-flash",
        "ollama": "llama3",
        "anthropic": "claude-3.5-sonnet-20240229"
    },
    "prompt_templates": {
        "default": """
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
    },
    "defaults": {
        "recent_commits": 5,
        "compare_branch": "main",
        "output_format": "text"  # text, json, or markdown
    }
}


def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load configuration from the config file."""
    ensure_config_dir()

    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        # Ensure all required keys are present
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value

        return config
    except (json.JSONDecodeError, IOError):
        # If there's an error reading the config, return default
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]):
    """Save configuration to the config file."""
    ensure_config_dir()

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving configuration: {e}")


def get_provider_api_key(provider: str) -> Optional[str]:
    """Get API key for a specific provider."""
    config = load_config()

    # Check if the key exists in the config
    if provider in config.get("api_keys", {}):
        return config["api_keys"][provider]

    # Try to get from environment variables
    env_var_name = f"{provider.upper()}_API_KEY"
    return os.environ.get(env_var_name)


def set_provider_api_key(provider: str, api_key: str):
    """Set API key for a specific provider."""
    config = load_config()

    if "api_keys" not in config:
        config["api_keys"] = {}

    config["api_keys"][provider] = api_key
    save_config(config)


def get_current_provider() -> str:
    """Get the currently selected LLM provider."""
    config = load_config()
    return config.get("provider", "groq")


def set_current_provider(provider: str):
    """Set the current LLM provider."""
    config = load_config()
    config["provider"] = provider
    save_config(config)


def get_model_for_provider(provider: str) -> str:
    """Get the selected model for a specific provider."""
    config = load_config()
    return config.get("model_preferences", {}).get(provider, "")


def set_model_for_provider(provider: str, model: str):
    """Set the model for a specific provider."""
    config = load_config()

    if "model_preferences" not in config:
        config["model_preferences"] = {}

    config["model_preferences"][provider] = model
    save_config(config)


def get_default_recent_commits() -> int:
    """Get the default number of recent commits to summarize."""
    config = load_config()
    return config.get("defaults", {}).get("recent_commits", 5)


def set_default_recent_commits(count: int):
    """Set the default number of recent commits to summarize."""
    config = load_config()

    if "defaults" not in config:
        config["defaults"] = {}

    config["defaults"]["recent_commits"] = count
    save_config(config)


def get_default_compare_branch() -> str:
    """Get the default branch to compare against."""
    config = load_config()
    return config.get("defaults", {}).get("compare_branch", "main")


def set_default_compare_branch(branch: str):
    """Set the default branch to compare against."""
    config = load_config()

    if "defaults" not in config:
        config["defaults"] = {}

    config["defaults"]["compare_branch"] = branch
    save_config(config)


def get_default_output_format() -> str:
    """Get the default output format (text/json/markdown)."""
    config = load_config()
    return config.get("defaults", {}).get("output_format", "text")


def set_default_output_format(format: str):
    """Set the default output format (text/json/markdown)."""
    config = load_config()

    if "defaults" not in config:
        config["defaults"] = {}

    config["defaults"]["output_format"] = format
    save_config(config)

def get_prompt_template(template_name: str = "default") -> str:
    """Get a prompt template by name.

    Args:
        template_name: Name of the template to retrieve. Defaults to "default".

    Returns:
        The prompt template string.
    """
    config = load_config()
    return config.get("prompt_templates", {}).get(template_name, DEFAULT_CONFIG["prompt_templates"]["default"])

def set_prompt_template(template_name: str, template: str):
    """Set a prompt template.

    Args:
        template_name: Name of the template to set
        template: The prompt template string
    """
    config = load_config()

    if "prompt_templates" not in config:
        config["prompt_templates"] = {}

    config["prompt_templates"][template_name] = template
    save_config(config)

def get_active_template_name() -> str:
    """Get the name of the currently active prompt template."""
    config = load_config()
    return config.get("defaults", {}).get("active_template", "default")

def set_active_template(template_name: str):
    """Set the active prompt template.

    Args:
        template_name: Name of the template to set as active
    """
    config = load_config()

    if "defaults" not in config:
        config["defaults"] = {}

    config["defaults"]["active_template"] = template_name
    save_config(config)
