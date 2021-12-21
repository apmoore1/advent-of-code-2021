import argparse
from pathlib import Path
from typing import Callable, Tuple

import numpy as np

def load_data(data_path: Path) -> np.ndarray:
    with data_path.open('r', encoding='utf-8') as data_fp:
        lines = data_fp.readlines()
        assert 1 == len(lines)
        line = lines[0].strip()
        return np.array(line.split(','), np.int32)

def cost_horizontal_position(position: int, crab_positions: np.ndarray) -> int:
    if position < 0:
        raise ValueError('This function assumes the position is positive.')
    return np.sum(np.absolute(crab_positions - position))

def cost_horizontal_position_summed(position: int, crab_positions: np.ndarray) -> int:
    if position < 0:
        raise ValueError('This function assumes the position is positive.')

    def sum_factorial(value) -> int:
        return np.sum(np.arange(value + 1))

    vectorized_sum_factorial = np.vectorize(sum_factorial)
    return np.sum(vectorized_sum_factorial(np.absolute(crab_positions - position)))

def get_least_cost(cost_func: Callable[[int, np.ndarray], int], data: np.ndarray) -> Tuple[int, int]:
    minimum_value = np.amin(data)
    maximum_value = np.amax(data)
    least_cost_position = maximum_value
    least_cost = cost_func(maximum_value, data)
    for position_value in range(minimum_value, maximum_value):
        position_cost = cost_func(position_value, data)
        if position_cost < least_cost:
            least_cost = position_cost
            least_cost_position = position_value
    return (least_cost, least_cost_position)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    data_file = Path(__file__, '..', 'horizontal_positions_data.txt').resolve()
    if args.test:
        data_file = Path(__file__, '..', 'test.txt').resolve()
    data = load_data(data_file)

    cost, position = get_least_cost(cost_horizontal_position, data)
    print(f'Solution 1: least cost: {cost} position: {position}')

    cost, position = get_least_cost(cost_horizontal_position_summed, data)
    print(f'Solution 2: least cost: {cost} position: {position}')

    
        
    