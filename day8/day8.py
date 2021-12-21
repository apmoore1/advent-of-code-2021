from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Iterator, Tuple, List, Dict, Set

def load_data(data_file: Path) -> Iterator[Tuple[List[str], List[str]]]:
    with data_file.open('r', encoding='utf-8') as data_fp:
        for line in data_fp:
            line = line.strip()
            if line:
                signal_pattern, output_pattern = line.split('|')
                signal_patterns = signal_pattern.split()
                output_patterns = output_pattern.split()
                yield signal_patterns, output_patterns

def get_occurrence_of_known_patterns(known_patterns: Dict[int, int],
                                     data_file: Path) -> int:
    reverse_known_patterns = {v: k for k, v in known_patterns.items()}
    occurrence_count = Counter()
    for _, output_pattern in load_data(data_file):
        output_pattern_lengths = [len(pattern) for pattern in output_pattern]
        occurrence_count.update(output_pattern_lengths)
    return sum([count for length, count in occurrence_count.items() if length in reverse_known_patterns])

def get_known_patterns(known_patterns: Dict[int, int],
                       data_file: Path) -> List[List[int]]:
    pattern_occurred = []
    for signal_pattern, output_pattern in load_data(data_file):
        both_patterns = signal_pattern + output_pattern
        both_patterns_lengths = set([len(pattern) for pattern in both_patterns])
        occurrences = []
        for digit, length in known_patterns.items():
            if length in both_patterns_lengths:
                occurrences.append(digit)
        assert 4 == len(occurrences)
        pattern_occurred.append(occurrences)
    return pattern_occurred

#def letter_e(value_for_8: Set, value_for_4: Set) -> Set:
#    value_for_8.diff(value_for_4)

def letter_a_1(value_for_7: Set[str], value_for_1: Set[str]) -> str:
    diff = value_for_7.difference(value_for_1)
    assert 1 == len(diff)
    return diff.pop()

def letter_a_2(value_for_7: Set[str], value_for_4: Set[str]) -> str:
    similarities = value_for_7.intersection(value_for_4)
    diff = value_for_7.difference(similarities)
    assert 1 == len(diff)
    return diff.pop()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    current_dir = Path(__file__, '..').resolve()
    data_file = Path(current_dir, 'display_data.txt')
    if args.test:
        data_file = Path(current_dir, 'test.txt')
    
    known_patterns = {8: 7, 7: 3, 4: 4, 1: 2}
    known_patterns_occur = get_occurrence_of_known_patterns(known_patterns, data_file)
    print(f'Number of times the known patterns occur: {known_patterns_occur}')
    
    patterns = {0: {'a', 'b', 'c', 'e', 'f', 'g'},
                1: {'c', 'f'},
                2: {'a', 'c', 'd', 'e', 'g'},
                3: {'a', 'c', 'd', 'f', 'g'},
                4: {'b', 'c', 'd', 'f'},
                5: {'a', 'b', 'd', 'f', 'g'},
                6: {'a', 'b', 'd', 'e', 'f', 'g'},
                7: {'a', 'c', 'f'},
                8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
                9: {'a', 'b', 'c', 'd', 'f', 'g'}}
    pattern_lengths = {digit: len(segments) for digit, segments in patterns.items()}
    get_known_patterns(known_patterns, data_file)