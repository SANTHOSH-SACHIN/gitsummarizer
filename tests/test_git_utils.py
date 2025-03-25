"""
Tests for the git_utils module.
"""

import unittest
from unittest import mock
import git
from git import Repo

from gitsummarizer.git_utils import get_repo, get_commit_log, get_commit_details, compare_branches, GitError


class TestGitUtils(unittest.TestCase):
    """Test suite for the git_utils module."""

    @mock.patch('gitsummarizer.git_utils.Repo')
    def test_get_repo(self, mock_repo_class):
        # Setup mock
        mock_repo = mock.Mock()
        mock_repo_class.return_value = mock_repo

        # Call function
        result = get_repo()

        # Assertions
        self.assertEqual(result, mock_repo)
        mock_repo_class.assert_called_once()

    @mock.patch('gitsummarizer.git_utils.get_repo')
    def test_get_commit_log(self, mock_get_repo):
        # Setup mock repo
        mock_repo = mock.Mock(spec=Repo)
        mock_commit1 = self._create_mock_commit("abc123", "First commit", "John Doe", "john@example.com")
        mock_commit2 = self._create_mock_commit("def456", "Second commit", "Jane Smith", "jane@example.com")

        mock_repo.iter_commits.return_value = [mock_commit1, mock_commit2]
        mock_get_repo.return_value = mock_repo

        # Call function
        result = get_commit_log(num_commits=2)

        # Assertions
        self.assertIn("abc123", result)
        self.assertIn("def456", result)
        self.assertIn("First commit", result)
        self.assertIn("Second commit", result)
        self.assertIn("John Doe", result)
        self.assertIn("Jane Smith", result)

    @mock.patch('gitsummarizer.git_utils.get_repo')
    def test_get_commit_details(self, mock_get_repo):
        # Setup mock repo
        mock_repo = mock.Mock(spec=Repo)
        mock_commit = self._create_mock_commit("abc123", "Test commit", "John Doe", "john@example.com")

        # Setup diff
        mock_diff = mock.Mock()
        mock_diff.a_path = "file1.txt"
        mock_diff.b_path = "file1.txt"
        mock_diff.a_blob.data_stream.read.return_value = b"old content"
        mock_diff.b_blob.data_stream.read.return_value = b"new content"

        mock_commit.diff.return_value = [mock_diff]
        mock_repo.commit.return_value = mock_commit
        mock_get_repo.return_value = mock_repo

        # Call function
        result = get_commit_details("abc123")

        # Assertions
        self.assertIn("abc123", result)
        self.assertIn("Test commit", result)
        self.assertIn("John Doe", result)
        self.assertIn("file1.txt", result)

    @mock.patch('gitsummarizer.git_utils.get_repo')
    def test_compare_branches(self, mock_get_repo):
        # Setup mock repo
        mock_repo = mock.Mock(spec=Repo)

        # Create mock branch objects
        mock_main = mock.Mock()
        mock_main.name = "main"
        mock_feature = mock.Mock()
        mock_feature.name = "feature"
        mock_repo.branches = [mock_main, mock_feature]

        mock_repo.git.merge_base.return_value = "base123"

        mock_commit = self._create_mock_commit("abc123", "Feature commit", "John Doe", "john@example.com")
        mock_repo.iter_commits.return_value = [mock_commit]

        mock_repo.git.diff.return_value = "file1.txt | 2 +-"
        mock_get_repo.return_value = mock_repo

        # Call function
        result = compare_branches("main", "feature")

        # Assertions
        self.assertIn("Branch comparison between main and feature", result)
        self.assertIn("abc123", result)
        self.assertIn("Feature commit", result)
        self.assertIn("file1.txt", result)

    def _create_mock_commit(self, hexsha, message, author_name, author_email):
        """Helper to create mock commits."""
        mock_commit = mock.Mock()
        mock_commit.hexsha = hexsha
        mock_commit.message = message

        mock_commit.author = mock.Mock()
        mock_commit.author.name = author_name
        mock_commit.author.email = author_email

        mock_commit.authored_datetime.strftime.return_value = "2025-03-15 10:00:00"

        # Mock stats
        mock_commit.stats.files = {
            "file1.txt": {"insertions": 5, "deletions": 2}
        }
        mock_commit.stats.total = {"files": 1, "insertions": 5, "deletions": 2}

        # Mock parents
        mock_parent = mock.Mock()
        mock_commit.parents = [mock_parent]

        # Mock diff
        mock_commit.diff.return_value = []

        return mock_commit


if __name__ == '__main__':
    unittest.main()
