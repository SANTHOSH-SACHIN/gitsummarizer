"""Test configuration module functionality."""

import os
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from gitsummarizer import config

class TestConfig(TestCase):
    """Test configuration functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.old_config_dir = config.CONFIG_DIR
        config.CONFIG_DIR = Path(self.temp_dir)
        config.CONFIG_FILE = config.CONFIG_DIR / "config.json"

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir)
        config.CONFIG_DIR = self.old_config_dir
        config.CONFIG_FILE = config.CONFIG_DIR / "config.json"

    def test_prompt_template_management(self):
        """Test prompt template management functions."""
        # Test getting default template
        default_template = config.get_prompt_template()
        self.assertIn("{git_data}", default_template)
        self.assertIn("human-readable language", default_template)

        # Test setting and getting custom template
        custom_template = """
        Custom template with {git_data} placeholder
        """
        config.set_prompt_template("custom", custom_template)
        retrieved_template = config.get_prompt_template("custom")
        self.assertEqual(retrieved_template, custom_template)

        # Test getting non-existent template returns default
        nonexistent = config.get_prompt_template("nonexistent")
        self.assertEqual(nonexistent, config.DEFAULT_CONFIG["prompt_templates"]["default"])

    def test_active_template_management(self):
        """Test active template management functions."""
        # Test default active template
        self.assertEqual(config.get_active_template_name(), "default")

        # Test setting and getting active template
        config.set_active_template("custom")
        self.assertEqual(config.get_active_template_name(), "custom")

        # Test active template persists in config
        saved_config = config.load_config()
        self.assertEqual(saved_config["defaults"]["active_template"], "custom")
