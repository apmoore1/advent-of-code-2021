import argparse
from pathlib import Path
from typing import List
from collections import Counter

import numpy as np

def get_intial_state(data_file: Path) -> List[int]:
    with data_file.open('r', encoding='utf-8') as data_fp:
        line = data_fp.readlines()
        assert 1 == len(line)
        return [int(value) for value in line[0].strip().split(',')]

def first_version(data_file: Path, number_days: int) -> int:
    '''
    This version was my first attempt that completes task 1 but is too slow for
    task 2.
    '''
    
    intial_state = np.array(get_intial_state(data_file))
    for day in range(number_days):
        zero_indices = np.nonzero(intial_state == 0)
        intial_state -= 1
        intial_state[zero_indices] = 6
        number_to_add = zero_indices[0].size
        state_to_add = np.array([8] * number_to_add)
        intial_state = np.concatenate((intial_state, state_to_add))
    return intial_state.size

def second_version(data_file: Path, number_days: int) -> int:
    '''
    This version can do both task 1 and task 2 and therefore is much quicker than
    the first version. However this version only came about after a hint to use
    a Counter/Dictionary, therefore is not completely my own solution.
    '''
    old_state_counter = Counter(get_intial_state(data_file))
    for _ in range(number_days):
        number_zero = old_state_counter.get(0, 0)
        current_state_counter = Counter()
        for count, value in old_state_counter.items():
            current_state_counter[count - 1] = value
        current_state_counter[8] += number_zero
        current_state_counter[6] += current_state_counter[-1]
        del current_state_counter[-1]
        old_state_counter = current_state_counter
    return sum(old_state_counter.values())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('number_days', type=int)
    args = parser.parse_args()
    data_file = Path(__file__, '..', 'lantern_fish_data.txt')
    if args.test:
        data_file = Path(__file__, '..', 'test_data.txt')
    data_file = data_file.resolve()
    number_days: int = args.number_days
    print(second_version(data_file, number_days))