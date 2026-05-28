import pytest
from click.testing import CliRunner
from src.cli import cli


def test_cli_help():
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'GitHubWall' in result.output


def test_cli_create_help():
    """Test create command help shows expected options."""
    runner = CliRunner()
    result = runner.invoke(cli, ['create', '--help'])
    assert result.exit_code == 0
    assert '--pattern' in result.output
    assert '--random' in result.output


def test_cli_create_with_random(tmp_path):
    """Test create command with random pattern."""
    runner = CliRunner()
    repo_path = str(tmp_path / "test-wall")
    result = runner.invoke(cli, [
        'create',
        '--repo', repo_path,
        '--random',
        '--density', '0.3',
        '--year', '2024'
    ])
    assert result.exit_code == 0
