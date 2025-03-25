"""
Git utilities for GitSummarizer.

This module provides functions to interact with Git repositories
using the gitpython library.
"""

import git
from git import Repo
from typing import List, Dict, Any, Optional, Tuple
import os


class GitError(Exception):
    """Exception raised for Git-related errors."""
    pass


def get_repo() -> Repo:
    """Get git repository from current directory."""
    try:
        return Repo(os.getcwd(), search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        raise GitError("Not a git repository (or any parent directories)")
    except git.NoSuchPathError:
        raise GitError("Path does not exist")


def get_commit_log(num_commits: int = 5, branch: Optional[str] = None) -> str:
    """
    Get git log for the specified number of commits and branch.

    Args:
        num_commits: Number of commits to retrieve
        branch: Branch name (optional)

    Returns:
        String containing git log information
    """
    repo = get_repo()

    try:
        # Get the correct branch if specified
        if branch:
            try:
                repo_branch = repo.branches[branch]
            except IndexError:
                raise GitError(f"Branch '{branch}' not found")
            commits = list(repo.iter_commits(branch, max_count=num_commits))
        else:
            commits = list(repo.iter_commits(max_count=num_commits))

        # Format the commits similar to git log --stat
        log_output = ""
        for commit in commits:
            # Get the stats for this commit
            stats = commit.stats

            # Format the commit line
            short_hash = commit.hexsha[:7]
            first_line = commit.message.split('\n')[0]
            log_output += f"{short_hash} {first_line}\n"

            # Add stats info
            log_output += f"Author: {commit.author.name} <{commit.author.email}>\n"
            log_output += f"Date:   {commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            # Add file changes
            for file_path, file_stats in stats.files.items():
                insertions = file_stats.get('insertions', 0)
                deletions = file_stats.get('deletions', 0)
                changes = f"{insertions} insertion{'s' if insertions != 1 else ''}(+), " \
                         f"{deletions} deletion{'s' if deletions != 1 else ''}(-)"
                log_output += f"    {file_path} | {changes}\n"

            log_output += f"\n {stats.total['files']} file{'s' if stats.total['files'] != 1 else ''} changed, " \
                         f"{stats.total['insertions']} insertion{'s' if stats.total['insertions'] != 1 else ''}(+), " \
                         f"{stats.total['deletions']} deletion{'s' if stats.total['deletions'] != 1 else ''}(-)\n\n"

        return log_output

    except git.GitCommandError as e:
        raise GitError(f"Git command error: {e}")


def get_commit_details(commit_hash: str) -> str:
    """
    Get detailed information for a specific commit.

    Args:
        commit_hash: Hash of the commit to get details for

    Returns:
        String containing commit details
    """
    repo = get_repo()

    try:
        # Try to get the commit
        commit = repo.commit(commit_hash)

        # Format the output similar to git show
        output = f"commit {commit.hexsha}\n"
        output += f"Author: {commit.author.name} <{commit.author.email}>\n"
        output += f"Date:   {commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        output += f"    {commit.message}\n\n"

        # Add the diffs
        for diff in commit.diff(commit.parents[0] if commit.parents else git.NULL_TREE):
            output += f"diff --git a/{diff.a_path} b/{diff.b_path}\n"

            # Add the diff content
            if diff.a_blob and diff.b_blob:
                output += f"--- a/{diff.a_path}\n"
                output += f"+++ b/{diff.b_path}\n"

                # Add a simplified diff output
                a_lines = diff.a_blob.data_stream.read().decode('utf-8', errors='replace').splitlines()
                b_lines = diff.b_blob.data_stream.read().decode('utf-8', errors='replace').splitlines()

                for i, line in enumerate(a_lines[:5]):  # Show first 5 lines only to avoid huge outputs
                    output += f"-{line}\n"

                if len(a_lines) > 5:
                    output += "...\n"

                for i, line in enumerate(b_lines[:5]):  # Show first 5 lines only
                    output += f"+{line}\n"

                if len(b_lines) > 5:
                    output += "...\n"

        return output

    except (git.GitCommandError, ValueError) as e:
        raise GitError(f"Error getting commit details: {e}")


def get_commits_in_time_range(start_date: str, end_date: str, branch: Optional[str] = None) -> str:
    """
    Get git log for commits between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        branch: Branch name (optional)

    Returns:
        String containing git log information
    """
    repo = get_repo()

    try:
        # Validate date format
        from datetime import datetime
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')

        # Build the date range query
        date_range = f"--since='{start_date}' --until='{end_date}'"

        # Get the commits in the date range
        if branch:
            commits = list(repo.iter_commits(branch, since=start_date, until=end_date))
        else:
            commits = list(repo.iter_commits(since=start_date, until=end_date))

        if not commits:
            return f"No commits found between {start_date} and {end_date}"

        # Format the output similar to get_commit_log
        log_output = f"Commits between {start_date} and {end_date}:\n\n"
        for commit in commits:
            short_hash = commit.hexsha[:7]
            first_line = commit.message.split('\n')[0]
            log_output += f"{short_hash} {first_line}\n"
            log_output += f"Author: {commit.author.name} <{commit.author.email}>\n"
            log_output += f"Date:   {commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        return log_output

    except ValueError as e:
        raise GitError(f"Invalid date format: {e}. Please use YYYY-MM-DD format.")
    except git.GitCommandError as e:
        raise GitError(f"Git command error: {e}")


def compare_branches(base_branch: str, compare_branch: str) -> str:
    """
    Compare two branches and return a summary of differences.

    Args:
        base_branch: Name of the base branch
        compare_branch: Name of the branch to compare against

    Returns:
        String containing branch comparison information
    """
    repo = get_repo()

    try:
        # Check if branches exist
        if base_branch not in [b.name for b in repo.branches]:
            raise GitError(f"Branch '{base_branch}' not found")

        if compare_branch not in [b.name for b in repo.branches]:
            raise GitError(f"Branch '{compare_branch}' not found")

        # Get the merge base commit
        merge_base = repo.git.merge_base(base_branch, compare_branch)

        # Get commits in compare_branch but not in base_branch
        commits = list(repo.iter_commits(f"{base_branch}..{compare_branch}"))

        output = f"Branch comparison between {base_branch} and {compare_branch}:\n\n"
        output += f"Number of commits ahead: {len(commits)}\n\n"

        # List commits
        output += "Commits:\n"
        for commit in commits:
            short_hash = commit.hexsha[:7]
            first_line = commit.message.split('\n')[0]
            output += f"{short_hash} {first_line}\n"

        output += "\nDiff stats:\n"
        diff_index = repo.git.diff(base_branch, compare_branch, stat=True)
        output += diff_index

        return output

    except git.GitCommandError as e:
        raise GitError(f"Git command error during branch comparison: {e}")
