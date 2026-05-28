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
