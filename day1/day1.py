from pathlib import Path
from typing import List

def larger_than_last_measurement_count(sonar_file: Path) -> int:
    with sonar_file.open('r', encoding='utf-8') as sonar_fp:
        last_measurement: int = int(next(sonar_fp))
        count: int = 0
        for line in sonar_fp:
            sonar_measurement = int(line)
            if sonar_measurement > last_measurement:
                count += 1
            last_measurement = sonar_measurement
        return count

def sliding_window_measurement_comparison(sonar_file: Path,
                                          window_size: int = 3) -> int:
    with sonar_file.open('r', encoding='utf-8') as sonar_fp:
        sliding_window: List[int] = [int(next(sonar_fp)) for _ in range(window_size)]
        last_window: int = sum(sliding_window)
        count: int = 0
        for line in sonar_fp:
            sliding_window.pop(0)
            sliding_window.append(int(line))
            current_window = sum(sliding_window)
            if current_window > last_window:
                count += 1
            last_window = current_window
        return count

if __name__ == '__main__':
    sonar_input_data = Path(__file__, '..', 'sonar_input_data.txt').resolve()
    count = larger_than_last_measurement_count(sonar_input_data)
    print(f'Number of measurements larger than the last {count}')

    window_size = 3
    window_count = sliding_window_measurement_comparison(sonar_input_data,
                                                         window_size=window_size)
    print('Number of measurements larger than the last based on a sliding '
          f'window of {window_size} is: {window_count}')