import click
from datetime import date

from src.core.pattern import Pattern, load_pattern, generate_random
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
@click.option('--year', type=int, help='Target year')
@click.option('--start', 'start_date', help='Start date (YYYY-MM-DD)')
@click.option('--end', 'end_date', help='End date (YYYY-MM-DD)')
def create(repo, pattern_name, use_random, density, year, start_date, end_date):
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
    if use_random:
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


if __name__ == '__main__':
    cli()
