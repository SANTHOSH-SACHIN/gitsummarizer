"""
Core summarization logic for GitSummarizer.
"""

import os
from typing import Optional, Dict, Any

from . import git_utils
from . import config
from .models import get_provider, ModelError, LLMProvider


class Summarizer:
    """Main summarizer class for GitSummarizer."""

    def __init__(self, provider_name: Optional[str] = None, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the summarizer.

        Args:
            provider_name: Name of the LLM provider to use
            api_key: API key for the provider
            model: Model to use
        """
        # Use provided values or fall back to config
        self.provider_name = provider_name or config.get_current_provider()
        self.api_key = api_key or config.get_provider_api_key(self.provider_name)
        self.model = model or config.get_model_for_provider(self.provider_name)

    def _get_provider(self) -> LLMProvider:
        """Get the LLM provider instance."""
        # Use the module-level get_provider function which can be mocked in tests
        from .models import get_provider
        return get_provider(self.provider_name, self.api_key, self.model)

    def summarize_recent_commits(self, num_commits: int = 5, branch: Optional[str] = None) -> str:
        """
        Summarize recent commits.

        Args:
            num_commits: Number of commits to summarize
            branch: Branch name (optional)

        Returns:
            Summary of recent commits
        """
        try:
            # Get git log
            git_log = git_utils.get_commit_log(num_commits, branch)

            # Generate summary
            provider = self._get_provider()
            prompt = provider.create_prompt(git_log)
            return provider.generate(prompt)

        except (git_utils.GitError, ModelError) as e:
            return f"Error generating summary: {str(e)}"

    def summarize_commit(self, commit_hash: str) -> str:
        """
        Summarize a specific commit.

        Args:
            commit_hash: Hash of the commit to summarize

        Returns:
            Summary of the commit
        """
        try:
            # Get commit details
            commit_details = git_utils.get_commit_details(commit_hash)

            # Generate summary
            provider = self._get_provider()
            prompt = provider.create_prompt(commit_details)
            return provider.generate(prompt)

        except (git_utils.GitError, ModelError) as e:
            return f"Error generating summary: {str(e)}"

    def compare_branches(self, base_branch: str, compare_branch: str) -> str:
        """
        Compare and summarize differences between two branches.

        Args:
            base_branch: Name of the base branch
            compare_branch: Name of the branch to compare against

        Returns:
            Summary of differences between branches
        """
        try:
            # Get branch comparison
            comparison = git_utils.compare_branches(base_branch, compare_branch)

            # Generate summary
            provider = self._get_provider()
            prompt = provider.create_prompt(comparison)
            return provider.generate(prompt)

        except (git_utils.GitError, ModelError) as e:
            return f"Error generating summary: {str(e)}"
