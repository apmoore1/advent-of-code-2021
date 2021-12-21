from pathlib import Path
from typing import List


def power_consumption_report(diagnostic_report: Path) -> int:
    with diagnostic_report.open('r', encoding='utf-8') as diagnostic_fp:
        binary_columns: List[List[int]] = []
        number_lines = 0
        for line in diagnostic_fp:
            line = line.strip()
            for index, value in enumerate(line):
                if len(binary_columns) < index + 1:
                    binary_columns.append([])
                binary_columns[index].append(int(value))
            number_lines += 1
        
        most_common_column_values: List[str] = []
        second_most_common_column_values: List[str] = []
        for column in binary_columns:
            most_common_column_value = '0'
            second_most_common_column_value = '1'
            if sum(column) < (number_lines / 2):
                most_common_column_value = '1'
                second_most_common_column_value = '0'
            most_common_column_values.append(most_common_column_value)
            second_most_common_column_values.append(second_most_common_column_value)
        gamma_rate_binary = ''.join(most_common_column_values)
        epsilon_rate_binary = ''.join(second_most_common_column_values)
            
                
            
        gamma_rate = int(gamma_rate_binary, 2)
        epsilon_rate = int(epsilon_rate_binary, 2)
        power_consumption = gamma_rate * epsilon_rate
        return power_consumption

def life_support_rating_report(diagnostic_report: Path) -> int:
    def most_common_value_in_binary_column(binary_column: List[int]) -> int:
        column_sum = sum(binary_column)
        number_values = len(binary_column)
        most_common_value = 1
        if column_sum < (number_values / 2):
            most_common_value = 0
        return most_common_value

    def index_of_most_column_value(binary_column: List[int],
                                   most_common_value: int) -> List[int]:
        indexes: List[int] = []
        for index, value in binary_column:
            if value == most_common_value:
                indexes.append(index)
        return indexes
    
    def filter_columns_by_most_common_value_in_index(binary_columns: List[List[int]],
                                                     index: int) -> List[List[int]]:
        binary_column = binary_columns[index]
        common_value = most_common_value_in_binary_column(binary_column)
        common_value_indexes = index_of_most_column_value(binary_column,
                                                          common_value)
        filtered_columns: List[List[int]] = []
        for index in common_value_indexes:
            for column in binary_columns:
                if 
                column[index]
    with diagnostic_report.open('r', encoding='utf-8') as diagnostic_fp:
        binary_columns: List[List[int]] = []
        for line in diagnostic_fp:
            line = line.strip()
            for index, value in enumerate(line):
                if len(binary_columns) < index + 1:
                    binary_columns.append([])
                binary_columns[index].append(int(value))
        


if __name__ == '__main__':
    data_file = Path(__file__, '..', 'diagnostic_report.txt').resolve()
    power_consumption = power_consumption_report(data_file)
    print(f'Power consumption: {power_consumption}')

    life_support_rating = life_support_rating_report(data_file)
    print(f'Life support rating: {life_support_rating}')