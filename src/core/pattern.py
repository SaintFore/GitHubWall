import json
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Pattern:
    name: str
    data: List[List[int]]

    def __post_init__(self):
        self.validate()

    @property
    def width(self) -> int:
        return len(self.data[0]) if self.data else 0

    @property
    def height(self) -> int:
        return len(self.data)

    def validate(self) -> bool:
        if self.height != 7:
            raise ValueError(f"Height must be 7, got {self.height}")

        for row_idx, row in enumerate(self.data):
            if len(row) != self.width:
                raise ValueError(f"Row {row_idx} has inconsistent width")
            for col_idx, value in enumerate(row):
                if not 0 <= value <= 4:
                    raise ValueError(
                        f"Invalid level {value} at ({row_idx}, {col_idx}). Must be 0-4"
                    )
        return True


def load_pattern(file_path: str) -> Pattern:
    """Load a Pattern from a JSON file.

    The JSON file must contain at minimum a 'name' (str) and 'data' (list of
    list of int) field. Optional 'width' and 'height' keys are accepted but
    ignored -- they are derived from the data itself.

    Raises FileNotFoundError when the path does not exist, and
    json.JSONDecodeError when the file is not valid JSON.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return Pattern(name=data["name"], data=data["data"])


def generate_random(width: int = 52, density: float = 0.5) -> Pattern:
    """Generate a random pattern with configurable width and density.

    Args:
        width: Number of columns (default 52, one per week of the year).
        density: Probability (0.0-1.0) that any given cell is non-zero.

    Returns:
        A Pattern with name "random" and 7 rows of random levels.
    """
    data = []
    for _ in range(7):
        row = []
        for _ in range(width):
            if random.random() < density:
                level = random.choices([1, 2, 3, 4], weights=[4, 3, 2, 1])[0]
            else:
                level = 0
            row.append(level)
        data.append(row)
    return Pattern(name="random", data=data)


def generate_fill_all(width: int = 52, level: int = 2, vary: bool = False) -> Pattern:
    """Generate a pattern that fills every day.

    Args:
        width: Number of columns (default 52).
        level: Fixed level (1-4) for all cells when vary=False.
        vary: If True, randomly vary levels between 1-4 for a natural look.

    Returns:
        A Pattern with all cells filled.
    """
    data = []
    for _ in range(7):
        row = []
        for _ in range(width):
            if vary:
                row.append(random.choices([1, 2, 3, 4], weights=[2, 3, 3, 2])[0])
            else:
                row.append(level)
        data.append(row)
    return Pattern(name="fill_all", data=data)
