from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Optional, List

import numpy as np

@dataclass
class coordinate:
    x: int
    y: int

class line:

    def __init__(self, start: coordinate, end: coordinate) -> None:
        self.start = start
        self.end = end
        self.min_x = min(self.start.x, self.end.x)
        self.max_x = max(self.start.x, self.end.x)
        self.min_y = min(self.start.y, self.end.y)
        self.max_y = max(self.start.y, self.end.y)

    def coordinates_on_lines(self, incl_diagonal: bool = False
                             ) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        '''
        Returns a Tuple of length two, 1. an array of row indices, and 2. an array
        of column indices. These indices can be used to find a vertical or horizontal
        line given the coordinates of the line. If the line is not horizontal or vertical
        it returns None.

        It can take into account diagonal lines with `incl_diagonal=True`
        '''
        def get_range_values(value_1: int, value_2: int) -> List[int]:
            range_start = min(value_1, value_2) + 1
            range_end = max(value_1, value_2)
            return list(range(range_start, range_end))

        # Vertical line
        vertical_indices: List[int] = [self.start.y, self.end.y]
        horizontal_indices: List[int] = [self.start.x, self.end.x]
        if self.start.x == self.end.x:
            vertical_range = get_range_values(self.start.y, self.end.y)
            vertical_indices.extend(vertical_range)
            horizontal_indices.extend([self.start.x] * len(vertical_range))
        # Horizontal line
        elif self.start.y == self.end.y:
            horizontal_range = get_range_values(self.start.x, self.end.x)
            horizontal_indices.extend(horizontal_range)
            vertical_indices.extend([self.start.y] * len(horizontal_range))
        elif incl_diagonal:
            start_x = self.start.x
            start_y = self.start.y
            end_x = self.end.x
            end_y = self.end.y
            if self.min_x == self.end.x:
                start_x = self.end.x
                start_y = self.end.y
                end_x = self.start.x
                end_y = self.start.y
            increasing_y = True
            if start_y > end_y:
                increasing_y = False
            while start_x != end_x:
                start_x += 1
                if increasing_y:
                    start_y += 1
                else:
                    start_y -= 1
                horizontal_indices.append(start_x)
                vertical_indices.append(start_y)
            if not (start_x == end_x and start_y == end_y):
                return None
        else:
            return None
        return (np.array(vertical_indices, dtype=np.int32), np.array(horizontal_indices, dtype=np.int32))

class LineContainer:

    def __init__(self, lines: List[line]) -> None:
        self.lines = lines

    def min_x(self) -> int:
        return min([a_line.min_x for a_line in self.lines])
    
    def min_y(self) -> int:
        return min([a_line.min_y for a_line in self.lines])

    def max_x(self) -> int:
        return max([a_line.max_x for a_line in self.lines]) + 1

    def max_y(self) -> int:
        return max([a_line.max_y for a_line in self.lines]) + 1

def read_vent_data() -> List[line]:
    lines: List[line] = []
    def create_coordinate(coordinate_str: str) -> coordinate:
        x, y = coordinate_str.split(',')
        return coordinate(int(x), int(y))
    with Path(__file__, '..', 'vent_data.txt').resolve().open('r', encoding='utf-8') as vent_data_fp:
        for a_line in vent_data_fp:
            a_line = a_line.strip()
            if a_line:
                start_line, _, end_line = a_line.split()
                lines.append(line(create_coordinate(start_line),
                                  create_coordinate(end_line)))
    return lines

def lines_that_overlap(incl_diagonal: bool = False) -> int:
    lines = LineContainer(read_vent_data())
    max_x, max_y = lines.max_x(), lines.max_y()
    board = np.zeros((max_x, max_y))
    for a_line in lines.lines:
        line_indices = a_line.coordinates_on_lines(incl_diagonal=incl_diagonal)
        if line_indices is not None:
            board[line_indices] += 1
    return (board > 1).sum()

if __name__ == '__main__':
    print('Number of horizontal and vertical lines that overlap: '
          f'{lines_that_overlap()}')
    print('Number of horizontal, vertical, and diagonal lines that overlap: '
          f'{lines_that_overlap(True)}')

