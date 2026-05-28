import subprocess
import os
from datetime import date


class GitEngine:
    """Handles all git operations for creating contributions."""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def init_repo(self):
        """Initialize a new git repository."""
        os.makedirs(self.repo_path, exist_ok=True)
        subprocess.run(
            ['git', 'init'],
            cwd=self.repo_path,
            check=True,
            capture_output=True
        )

    def create_commit(self, commit_date: date, message: str = "Contribution"):
        """Create a commit with a specific date.

        Uses GIT_AUTHOR_DATE and GIT_COMMITTER_DATE environment variables
        to backdate the commit. Supports empty commits via --allow-empty.
        """
        env = os.environ.copy()
        date_str = commit_date.strftime("%Y-%m-%dT12:00:00")
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        subprocess.run(
            ['git', 'commit', '--allow-empty', '-m', message],
            cwd=self.repo_path,
            env=env,
            check=True,
            capture_output=True
        )

    def add_remote(self, remote_name: str, remote_url: str):
        """Add a remote repository."""
        subprocess.run(
            ['git', 'remote', 'add', remote_name, remote_url],
            cwd=self.repo_path,
            check=True,
            capture_output=True
        )

    def push(self, remote_name: str = "origin", branch: str = "main"):
        """Push to a remote repository."""
        subprocess.run(
            ['git', 'push', '-u', remote_name, branch],
            cwd=self.repo_path,
            check=True,
            capture_output=True
        )
