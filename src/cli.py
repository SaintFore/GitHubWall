import click
import shutil
from datetime import date
from pathlib import Path

from src.core.pattern import Pattern, load_pattern, generate_random, generate_fill_all
from src.core.scheduler import Scheduler
from src.core.git_engine import GitEngine


@click.group()
def cli():
    """GitHubWall - Auto-fill GitHub contribution heatmap"""
    pass


@cli.command()
@click.option('--repo', default='.', help='Repository path')
@click.option('--pattern', 'pattern_name', help='Pattern name or file path')
@click.option('--random', 'use_random', is_flag=True, help='Use random pattern')
@click.option('--density', default=0.5, help='Random density (0.0-1.0)')
@click.option('--fill', 'fill_all', is_flag=True, help='Fill every day with commits')
@click.option('--level', default=2, type=click.IntRange(1, 4), help='Fixed level for --fill (1-4)')
@click.option('--vary', is_flag=True, help='Vary levels randomly for --fill (natural look)')
@click.option('--year', type=int, help='Target year')
@click.option('--start', 'start_date', help='Start date (YYYY-MM-DD)')
@click.option('--end', 'end_date', help='End date (YYYY-MM-DD)')
def create(repo, pattern_name, use_random, density, fill_all, level, vary, year, start_date, end_date):
    """Create commits to fill heatmap."""
    # Determine date range
    if start_date and end_date:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    elif year:
        start = date(year, 1, 1)
        end = date(year, 12, 31)
    else:
        start = date(date.today().year, 1, 1)
        end = date(date.today().year, 12, 31)

    # Determine pattern
    if fill_all:
        pattern = generate_fill_all(width=52, level=level, vary=vary)
    elif use_random:
        pattern = generate_random(width=52, density=density)
    elif pattern_name:
        if pattern_name.endswith('.json'):
            pattern = load_pattern(pattern_name)
        else:
            pattern = load_pattern(f'src/patterns/{pattern_name}.json')
    else:
        pattern = load_pattern('src/patterns/heart.json')

    # Generate commit schedule
    scheduler = Scheduler(start, end)
    schedule = scheduler.generate_schedule(pattern)

    # Create repo and commits
    engine = GitEngine(repo)
    engine.init_repo()

    click.echo(f"Creating {len(schedule)} commits...")
    with click.progressbar(schedule) as bar:
        for commit_date in bar:
            engine.create_commit(commit_date)

    click.echo(f"Done! Repository created at {repo}")


@cli.command()
@click.option('--repo', default='.', help='Repository path')
@click.option('--remote', default='origin', help='Remote name')
def push(repo, remote):
    """Push to remote repository."""
    engine = GitEngine(repo)
    engine.push(remote)
    click.echo("Pushed successfully!")


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind')
@click.option('--port', default=8000, type=int, help='Port to bind')
def web(host, port):
    """Start web interface"""
    from src.web.app import run_web
    click.echo(f"Starting web interface at http://{host}:{port}")
    run_web(host, port)


@cli.command()
@click.option('--repo', default='.', help='Target repository path')
def workflow(repo):
    """Generate GitHub Actions workflow for daily commits."""
    repo_path = Path(repo)
    workflow_dir = repo_path / '.github' / 'workflows'
    workflow_dir.mkdir(parents=True, exist_ok=True)

    # Find the template workflow
    template_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'daily-commit.yml'
    if not template_path.exists():
        click.echo("Error: Workflow template not found")
        return

    target_path = workflow_dir / 'daily-commit.yml'
    shutil.copy2(template_path, target_path)
    click.echo(f"Workflow generated at {target_path}")
    click.echo("")
    click.echo("Next steps:")
    click.echo("1. Go to your GitHub repo -> Settings -> Secrets -> Actions")
    click.echo("2. Add a new secret named 'PAT' with your Personal Access Token")
    click.echo("3. Token needs 'Contents: Read and write' permission")
    click.echo("4. The workflow will run daily at 20:00 Beijing time")


if __name__ == '__main__':
    cli()
