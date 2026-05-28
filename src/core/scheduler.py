from datetime import date, timedelta
from typing import List

from src.core.pattern import Pattern


def get_commit_count(level: int) -> int:
    mapping = {0: 0, 1: 1, 2: 3, 3: 5, 4: 10}
    if level not in mapping:
        raise ValueError(f"Invalid level: {level}. Must be 0-4")
    return mapping[level]


def align_to_sunday(d: date) -> date:
    days_since_sunday = (d.weekday() + 1) % 7
    return d - timedelta(days=days_since_sunday)


class Scheduler:
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date

    def generate_schedule(self, pattern: Pattern) -> List[date]:
        dates = []
        current = align_to_sunday(self.start_date)

        for week in range(pattern.width):
            for day in range(7):
                target_date = current + timedelta(weeks=week, days=day)
                if self.start_date <= target_date <= self.end_date:
                    level = pattern.data[day][week]
                    count = get_commit_count(level)
                    for _ in range(count):
                        dates.append(target_date)

        return sorted(dates)
