"""
Tests for the CLI commands.
"""

import unittest
from unittest import mock
import argparse
from io import StringIO
import sys

from gitsummarizer.cli import (
    setup_command,
    recent_command,
    commit_command,
    compare_command,
    time_range_command,
    provider_command,
    main
)
from gitsummarizer import config, git_utils
from gitsummarizer.summarizer import Summarizer


class TestCLI(unittest.TestCase):
    """Test suite for CLI commands."""

    def setUp(self):
        # Mock console print to capture output
        self.console_patcher = mock.patch('gitsummarizer.cli.console')
        self.mock_console = self.console_patcher.start()

        # Mock config methods
        self.config_patcher = mock.patch('gitsummarizer.cli.config')
        self.mock_config = self.config_patcher.start()
        self.mock_config.get_current_provider.return_value = 'groq'
        self.mock_config.get_provider_api_key.return_value = 'test_key'

        # Mock git_utils
        self.git_utils_patcher = mock.patch('gitsummarizer.cli.git_utils')
        self.mock_git_utils = self.git_utils_patcher.start()

        # Mock Summarizer to always use groq
        self.summarizer_patcher = mock.patch('gitsummarizer.cli.Summarizer')
        self.mock_summarizer = self.summarizer_patcher.start()
        mock_summarizer = self.mock_summarizer.return_value
        mock_summarizer.provider_name = 'groq'

    def tearDown(self):
        self.console_patcher.stop()
        self.config_patcher.stop()
        self.git_utils_patcher.stop()
        self.summarizer_patcher.stop()

    @mock.patch('gitsummarizer.cli.Prompt')
    @mock.patch('gitsummarizer.cli.Confirm')
    def test_setup_command(self, mock_confirm, mock_prompt):
        """Test the setup command."""
        # Setup mocks
        mock_prompt.ask.side_effect = [
            'groq',  # Provider selection
            'test_api_key',  # API key
            'llama2-70b'  # Model selection
        ]
        mock_confirm.ask.return_value = True

        # Mock config
        self.mock_config.get_current_provider.return_value = 'groq'
        self.mock_config.get_provider_api_key.return_value = 'test_key'

        # Call the command
        setup_command()

        # Verify calls
        # Verify provider selection prompt was called with correct choices (order doesn't matter)
        provider_call = None
        for call in mock_prompt.ask.call_args_list:
            if call[0][0] == "Select LLM provider":
                provider_call = call
                break
        self.assertIsNotNone(provider_call)
        self.assertEqual(provider_call[0][0], "Select LLM provider")
        self.assertEqual(set(provider_call[1]['choices']),
                        {'anthropic', 'gemini', 'groq', 'ollama', 'openai'})
        self.assertEqual(provider_call[1]['default'], 'groq')
        self.mock_config.set_current_provider.assert_called_once_with('groq')
        mock_prompt.ask.assert_any_call("API Key", password=True)
        self.mock_config.set_provider_api_key.assert_called_once_with('groq', 'test_api_key')
        # Verify model prompt was called with correct question
        model_calls = [call for call in mock_prompt.ask.call_args_list
                      if len(call[0]) > 0 and call[0][0] == "Model for groq"]
        self.assertEqual(len(model_calls), 1, "Model prompt not called exactly once")
        self.mock_config.set_model_for_provider.assert_called_once_with('groq', 'llama2-70b')

        # Verify console prints
        self.mock_console.print.assert_any_call("[bold green]GitSummarizer Setup[/bold green]")
        self.mock_console.print.assert_any_call("[bold green]✓ Setup complete![/bold green]")
        self.mock_console.print.assert_any_call("Using groq with model llama2-70b")

    def test_recent_command(self):
        """Test the recent commits command."""
        # Create mock args
        args = mock.Mock()
        args.num = 5
        args.branch = "main"

        # Mock summarizer
        mock_summarizer = self.mock_summarizer.return_value
        mock_summarizer.summarize_recent_commits.return_value = "Test summary"
        mock_summarizer.provider_name = 'groq'
        self.assertEqual(mock_summarizer.provider_name, 'groq')

        # Mock console.status
        mock_status = mock.MagicMock()
        self.mock_console.status.return_value.__enter__.return_value = mock_status

        # Call the command
        recent_command(args)

        # Verify calls
        self.mock_summarizer.assert_called_once()
        mock_summarizer.summarize_recent_commits.assert_called_once_with(5, "main")
        self.mock_console.status.assert_called_once_with("[bold green]Analyzing recent commits...[/bold green]")
        # Verify panel print with correct title and style
        self.mock_console.print.assert_called_once()
        panel = self.mock_console.print.call_args[0][0]
        self.assertEqual(panel.title, "Git Summary")
        self.assertEqual(panel.border_style, "green")

    def test_commit_command(self):
        """Test the commit summary command."""
        # Create mock args
        args = mock.Mock()
        args.commit_hash = "abc123"

        # Mock summarizer
        mock_summarizer = self.mock_summarizer.return_value
        mock_summarizer.summarize_commit.return_value = "Test commit summary"
        mock_summarizer.provider_name = 'groq'
        self.assertEqual(mock_summarizer.provider_name, 'groq')

        # Mock console.status
        mock_status = mock.MagicMock()
        self.mock_console.status.return_value.__enter__.return_value = mock_status

        # Call the command
        commit_command(args)

        # Verify calls
        self.mock_summarizer.assert_called_once()
        mock_summarizer.summarize_commit.assert_called_once_with("abc123")
        self.mock_console.status.assert_called_once_with(
            "[bold green]Analyzing commit abc123...[/bold green]"
        )
        # Verify panel print was called with expected content
        self.mock_console.print.assert_called_once()
        panel = self.mock_console.print.call_args[0][0]
        self.assertEqual(panel.title, "Commit abc123 Summary")
        self.assertEqual(panel.border_style, "green")
        self.assertIn("Test commit summary", str(panel.renderable.markup))

    def test_compare_command(self):
        """Test the branch comparison command."""
        # Create mock args
        args = mock.Mock()
        args.base_branch = "main"
        args.compare_branch = "feature"

        # Mock summarizer
        mock_summarizer = self.mock_summarizer.return_value
        mock_summarizer.compare_branches.return_value = "Test comparison summary"
        mock_summarizer.provider_name = 'groq'
        self.assertEqual(mock_summarizer.provider_name, 'groq')

        # Mock console.status
        mock_status = mock.MagicMock()
        self.mock_console.status.return_value.__enter__.return_value = mock_status

        # Call the command
        compare_command(args)

        # Verify calls
        self.mock_summarizer.assert_called_once()
        mock_summarizer.compare_branches.assert_called_once_with("main", "feature")
        self.mock_console.status.assert_called_once_with(
            "[bold green]Comparing main and feature...[/bold green]"
        )
        # Verify panel print with correct title and style
        self.mock_console.print.assert_called_once()
        panel = self.mock_console.print.call_args[0][0]
        self.assertEqual(panel.title, "Comparison: main → feature")
        self.assertEqual(panel.border_style, "green")

    def test_time_range_command(self):
        """Test the time range summary command."""
        # Create mock args
        args = mock.Mock()
        args.start_date = "2025-01-01"
        args.end_date = "2025-01-31"
        args.branch = "main"

        # Mock summarizer
        mock_summarizer = self.mock_summarizer.return_value
        mock_summarizer.summarize_time_range.return_value = "Test time range summary"
        mock_summarizer.provider_name = 'groq'
        self.assertEqual(mock_summarizer.provider_name, 'groq')

        # Mock console.status
        mock_status = mock.MagicMock()
        self.mock_console.status.return_value.__enter__.return_value = mock_status

        # Call the command
        time_range_command(args)

        # Verify calls
        self.mock_summarizer.assert_called_once()
        mock_summarizer.summarize_time_range.assert_called_once_with(
            "2025-01-01", "2025-01-31", "main"
        )
        self.mock_console.status.assert_called_once_with(
            "[bold green]Analyzing commits between 2025-01-01 and 2025-01-31...[/bold green]"
        )
        # Verify panel print with correct title and style
        self.mock_console.print.assert_called_once()
        panel = self.mock_console.print.call_args[0][0]
        self.assertEqual(panel.title, "Summary: 2025-01-01 to 2025-01-31")
        self.assertEqual(panel.border_style, "green")

    def test_provider_command_list(self):
        """Test listing available providers."""
        # Create mock args
        args = mock.Mock()
        args.list = True
        args.provider = None

        # Mock config
        self.mock_config.get_current_provider.return_value = "groq"
        self.mock_config.get_available_providers.return_value = [
            "groq", "openai", "gemini", "ollama", "anthropic"
        ]

        # Call the command
        provider_command(args)

        # Verify calls
        self.mock_config.get_current_provider.assert_called_once()
        # Verify the header was printed and current provider was marked
        self.assertIn(mock.call("[bold green]Available LLM Providers:[/bold green]"),
                     self.mock_console.print.call_args_list)
        self.assertIn(mock.call("→ [bold]groq[/bold] (current)"),
                     self.mock_console.print.call_args_list)

    def test_provider_command_set_valid(self):
        """Test setting a valid provider."""
        # Create mock args
        args = mock.Mock()
        args.list = False
        args.provider = "openai"

        # Mock config
        self.mock_config.get_provider_api_key.return_value = "test_key"

        # Call the command
        provider_command(args)

        # Verify calls
        self.mock_config.set_current_provider.assert_called_once_with("openai")
        self.mock_console.print.assert_called_with("[bold green]✓ Provider set to openai[/bold green]")

    def test_provider_command_set_invalid(self):
        """Test setting an invalid provider."""
        # Create mock args
        args = mock.Mock()
        args.list = False
        args.provider = "invalid"

        # Call the command
        provider_command(args)

        # Verify calls
        # Verify error message was printed (could be one of multiple calls)
        error_found = False
        for call in self.mock_console.print.call_args_list:
            if "[bold red]Error:[/bold red] Unknown provider: invalid" in call[0][0]:
                error_found = True
                break
        self.assertTrue(error_found, "Error message not found in console prints")
        self.mock_config.set_current_provider.assert_not_called()

    def test_provider_command_missing_key(self):
        """Test switching to provider with missing API key."""
        # Create mock args
        args = mock.Mock()
        args.list = False
        args.provider = "anthropic"

        # Mock config
        self.mock_config.get_provider_api_key.return_value = None

        # Call the command
        provider_command(args)

        # Verify calls
        self.mock_config.set_current_provider.assert_called_once_with("anthropic")
        self.mock_console.print.assert_called_with("[yellow]No API key found for this provider. Run 'gitsumm setup' to configure.[/yellow]")

    @mock.patch('gitsummarizer.cli.recent_command')
    def test_main_recent_command(self, mock_recent_command):
        """Test main() with recent command."""
        # Mock sys.argv
        with mock.patch('sys.argv', ['gitsumm', 'recent', '-n', '5']):
            main()

        # Verify recent_command was called with expected args
        args = mock_recent_command.call_args[0][0]
        self.assertEqual(args.num, 5)
        self.assertIsNone(args.branch)

    @mock.patch('gitsummarizer.cli.commit_command')
    def test_main_commit_command(self, mock_commit_command):
        """Test main() with commit command."""
        # Mock sys.argv
        with mock.patch('sys.argv', ['gitsumm', 'commit', 'abc123']):
            main()

        # Verify commit_command was called with expected args
        args = mock_commit_command.call_args[0][0]
        self.assertEqual(args.commit_hash, 'abc123')

    @mock.patch('gitsummarizer.cli.provider_command')
    def test_main_provider_command(self, mock_provider_command):
        """Test main() with provider command."""
        # Mock sys.argv
        with mock.patch('sys.argv', ['gitsumm', 'provider', 'openai']):
            main()

        # Verify provider_command was called with expected args
        args = mock_provider_command.call_args[0][0]
        self.assertEqual(args.provider, 'openai')
        self.assertFalse(args.list)

    def test_main_no_command(self):
        """Test main() with no command shows help."""
        # Mock sys.argv
        with mock.patch('sys.argv', ['gitsumm']):
            with mock.patch('gitsummarizer.cli.argparse.ArgumentParser.print_help') as mock_print_help:
                main()

        # Verify help was printed
        mock_print_help.assert_called_once()

    def test_main_git_error(self):
        """Test main() handles git errors."""
        # Mock sys.argv
        with mock.patch('sys.argv', ['gitsumm', 'recent']):
            # Mock git_utils to raise error
            self.mock_git_utils.get_repo.side_effect = git_utils.GitError("Not a git repo")

            # Call main and verify exit
            with self.assertRaises(SystemExit):
                main()

        # Verify error was printed
        self.mock_console.print.assert_called_with("[bold red]Error:[/bold red] Not a git repo")


if __name__ == '__main__':
    unittest.main()
