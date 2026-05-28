import pytest
import subprocess
import tempfile
import os
from datetime import date
from src.core.pattern import Pattern, generate_random
from src.core.scheduler import Scheduler
from src.core.git_engine import GitEngine


def test_full_workflow_random():
    """Test complete random pattern workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, "test-wall")

        # Generate random pattern
        pattern = generate_random(width=4, density=0.5)

        # Create scheduler
        start = date(2024, 1, 1)
        end = date(2024, 1, 28)
        scheduler = Scheduler(start, end)
        schedule = scheduler.generate_schedule(pattern)

        # Create repo and commits
        engine = GitEngine(repo_path)
        engine.init_repo()

        for commit_date in schedule:
            engine.create_commit(commit_date)

        # Verify commits
        result = subprocess.run(
            ['git', 'log', '--oneline'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        assert len(result.stdout.strip().split('\n')) == len(schedule)


def test_full_workflow_preset():
    """Test complete preset pattern workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, "test-wall")

        # Load preset pattern
        pattern = Pattern(name="test", data=[[1, 0, 0, 0, 0, 0, 0]] * 7)

        # Create scheduler
        start = date(2024, 1, 1)
        end = date(2024, 1, 7)
        scheduler = Scheduler(start, end)
        schedule = scheduler.generate_schedule(pattern)

        # Create repo and commits
        engine = GitEngine(repo_path)
        engine.init_repo()

        for commit_date in schedule:
            engine.create_commit(commit_date)

        # Verify commit dates
        result = subprocess.run(
            ['git', 'log', '--format=%ai'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        dates = result.stdout.strip().split('\n')
        assert len(dates) > 0
