"""
Tests for the summarizer module.
"""

import unittest
from unittest import mock

from gitsummarizer.summarizer import Summarizer


class TestSummarizer(unittest.TestCase):
    """Test suite for the Summarizer class."""

    @mock.patch('gitsummarizer.git_utils.get_commit_log')
    @mock.patch('gitsummarizer.models.get_provider')
    def test_summarize_recent_commits(self, mock_get_provider, mock_get_commit_log):
        # Setup mocks
        mock_get_commit_log.return_value = "Mock git log"

        mock_provider = mock.Mock()
        mock_provider.create_prompt.side_effect = lambda x: f"Prompt for: {x}"
        mock_provider.generate.return_value = "Mock summary"
        mock_get_provider.return_value = mock_provider

        # Create summarizer with groq provider
        summarizer = Summarizer(provider_name="groq", api_key="test_key")
        self.assertEqual(summarizer.provider_name, "groq")

        # Call the method
        result = summarizer.summarize_recent_commits(num_commits=3, branch="main")

        # Assertions
        mock_get_commit_log.assert_called_once_with(3, "main")
        mock_provider.create_prompt.assert_called_once_with("Mock git log")
        mock_provider.generate.assert_called_once_with("Prompt for: Mock git log")
        self.assertEqual(result, "Mock summary")

    @mock.patch('gitsummarizer.git_utils.get_commit_details')
    @mock.patch('gitsummarizer.models.get_provider')
    def test_summarize_commit(self, mock_get_provider, mock_get_commit_details):
        # Setup mocks
        mock_get_commit_details.return_value = "Mock commit details"

        mock_provider = mock.Mock()
        mock_provider.create_prompt.side_effect = lambda x: f"Prompt for: {x}"
        mock_provider.generate.return_value = "Mock summary"
        mock_get_provider.return_value = mock_provider

        # Create summarizer
        summarizer = Summarizer(provider_name="groq", api_key="test_key")

        # Call the method
        result = summarizer.summarize_commit(commit_hash="abc123")

        # Assertions
        mock_get_commit_details.assert_called_once_with("abc123")
        mock_provider.create_prompt.assert_called_once_with("Mock commit details")
        mock_provider.generate.assert_called_once_with("Prompt for: Mock commit details")
        self.assertEqual(result, "Mock summary")

    @mock.patch('gitsummarizer.git_utils.compare_branches')
    @mock.patch('gitsummarizer.models.get_provider')
    def test_compare_branches(self, mock_get_provider, mock_compare_branches):
        # Setup mocks
        mock_compare_branches.return_value = "Mock branch comparison"

        mock_provider = mock.Mock()
        mock_provider.create_prompt.side_effect = lambda x: f"Prompt for: {x}"
        mock_provider.generate.return_value = "Mock summary"
        mock_get_provider.return_value = mock_provider

        # Create summarizer
        summarizer = Summarizer(provider_name="groq", api_key="test_key")

        # Call the method
        result = summarizer.compare_branches(base_branch="main", compare_branch="feature")

        # Assertions
        mock_compare_branches.assert_called_once_with("main", "feature")
        mock_provider.create_prompt.assert_called_once_with("Mock branch comparison")
        mock_provider.generate.assert_called_once_with("Prompt for: Mock branch comparison")
        self.assertEqual(result, "Mock summary")


if __name__ == '__main__':
    unittest.main()
