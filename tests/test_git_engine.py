import pytest
import subprocess
import tempfile
import os
from datetime import date, timedelta
from unittest.mock import patch, MagicMock
from src.core.git_engine import GitEngine


def test_git_engine_init_repo():
    """Test initializing a repository"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitEngine(tmpdir)
        engine.init_repo()
        assert os.path.exists(os.path.join(tmpdir, '.git'))


def test_git_engine_create_commit():
    """Test creating a commit with a specific date"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitEngine(tmpdir)
        engine.init_repo()

        # Create a file so there is content to commit
        test_file = os.path.join(tmpdir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')

        subprocess.run(['git', 'add', '.'], cwd=tmpdir, check=True)
        engine.create_commit(date(2024, 1, 1), "Test commit")

        result = subprocess.run(
            ['git', 'log', '--format=%ai', '-1'],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )
        assert '2024-01-01' in result.stdout


def test_git_engine_create_empty_commit():
    """Test creating an empty commit"""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitEngine(tmpdir)
        engine.init_repo()

        # Need an initial commit first
        test_file = os.path.join(tmpdir, 'init.txt')
        with open(test_file, 'w') as f:
            f.write('init')
        subprocess.run(['git', 'add', '.'], cwd=tmpdir, check=True)
        subprocess.run(['git', 'commit', '-m', 'init'], cwd=tmpdir, check=True)

        engine.create_commit(date(2024, 6, 15), "Empty commit")

        result = subprocess.run(
            ['git', 'log', '--format=%ai', '-1'],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )
        assert '2024-06-15' in result.stdout


def test_git_engine_large_batch_disables_auto_maintenance():
    """Batch creation must not let git auto-maintenance race the commit loop."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitEngine(tmpdir)
        engine.init_repo()
        subprocess.run(['git', 'config', 'gc.auto', '1'], cwd=tmpdir, check=True)

        dates = [date(2024, 1, 1) + timedelta(days=i % 365) for i in range(300)]
        engine.create_commits_batch(dates)

        pack_dir = os.path.join(tmpdir, '.git', 'objects', 'pack')
        pack_files = [name for name in os.listdir(pack_dir) if name.startswith('pack-')]
        assert pack_files == []

        result = subprocess.run(
            ['git', 'fsck', '--full', '--no-reflogs'],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, result.stdout + result.stderr
