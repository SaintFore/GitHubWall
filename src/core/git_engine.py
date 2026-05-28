import subprocess
import os
from datetime import date

GIT_NO_AUTO_MAINTENANCE = (
    'git',
    '-c', 'gc.auto=0',
    '-c', 'maintenance.auto=false',
)


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

    def create_commits_batch(self, dates: list, message: str = "Contribution"):
        """Create multiple commits without triggering git auto-maintenance."""
        import time

        for i, commit_date in enumerate(dates):
            date_str = commit_date.strftime("%Y-%m-%dT12:00:00")

            # Write to file
            contributions_file = os.path.join(self.repo_path, '.contributions')
            with open(contributions_file, 'a') as f:
                f.write(f"{date_str}\n")

            # Stage and commit
            subprocess.run(
                [*GIT_NO_AUTO_MAINTENANCE, 'add', '.contributions'],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str

            subprocess.run(
                [*GIT_NO_AUTO_MAINTENANCE, 'commit', '-m', message],
                cwd=self.repo_path,
                env=env,
                check=True,
                capture_output=True
            )

            # Small delay every 100 commits
            if (i + 1) % 100 == 0:
                time.sleep(0.5)

    def create_commit(self, commit_date: date, message: str = "Contribution"):
        """Create a single commit with a specific date."""
        self.create_commits_batch([commit_date], message)

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
