from typing import Tuple
from pathlib import Path

def get_horizontal_depth_position(position_file: Path) -> Tuple[int, int]:
    with position_file.open('r', encoding='utf-8') as position_fp:
        horizontal_position = 0
        depth_position = 0
        for line in position_fp:
            command: str
            str_unit: str
            unit: int
            command, str_unit = line.split()
            unit = int(str_unit)
            if command == 'forward':
                horizontal_position += unit
            elif command == 'down':
                depth_position += unit
            elif command == 'up':
                depth_position -= unit
        return horizontal_position, depth_position

def get_horizontal_depth_position_with_aim(position_file: Path) -> Tuple[int, int]:
    with position_file.open('r', encoding='utf-8') as position_fp:
        horizontal_position = 0
        depth_position = 0
        aim = 0
        for line in position_fp:
            command: str
            str_unit: str
            unit: int
            command, str_unit = line.split()
            unit = int(str_unit)
            if command == 'forward':
                horizontal_position += unit
                depth_position += (aim * unit)
            elif command == 'down':
                aim += unit
            elif command == 'up':
                aim -= unit
        return horizontal_position, depth_position

if __name__ == '__main__':
    position_file = Path(__file__, '..', 'position_data.txt').resolve()
    horizontal, depth = get_horizontal_depth_position(position_file)
    multiplied_together = horizontal * depth
    print(f'Horizontal: {horizontal} and Depth: {depth} position. These two multipied '
          f'is {multiplied_together}')

    horizontal, depth = get_horizontal_depth_position_with_aim(position_file)
    multiplied_together = horizontal * depth
    print('Taking into account the aim, the new horizontal and depth position is:'
          f' {horizontal} {depth} respectively. These two multipied is'
          f' {multiplied_together}')