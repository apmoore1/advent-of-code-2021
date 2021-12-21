from typing import Iterator, List
from pathlib import Path

import numpy as np

def draw_number() -> Iterator[int]:
    bingo_input_file = Path(__file__, '..', 'bingo_input.txt').resolve()
    with bingo_input_file.open('r', encoding='utf-8') as bingo_input_fp:
        
        for string_number in bingo_input_fp.readline().strip().split(','):
            yield int(string_number)

def get_bingo_boards() -> List[np.ndarray]:
    bingo_input_file = Path(__file__, '..', 'bingo_input.txt').resolve()
    with bingo_input_file.open('r', encoding='utf-8') as bingo_input_fp:
        # ignore first line
        next(bingo_input_fp)
        board_lines: List[List[int]] = []
        boards: List[np.ndarray] = []
        for line in bingo_input_fp:
            line = line.strip()
            if not line and board_lines:
                boards.append(np.array(board_lines))
                board_lines = []
            if line:
                board_lines.append([int(value) for value in line.split()])
        if board_lines:
            boards.append(np.array(board_lines))
        return boards

def create_update_boards(boards=List[np.ndarray]) -> List[np.ndarray]:
    update_boards: List[np.ndarray] = []
    for board in boards:
        update_boards.append(np.zeros(board.shape))
    return update_boards

def update_board(bingo_boards: List[np.ndarray],
                 update_boards: List[np.ndarray],
                 drawn_number: int) -> List[np.ndarray]:
    for bingo_board, update_board in zip(bingo_boards, update_boards):
        update_board += (bingo_board == drawn_number).astype(int)
        update_board = (update_board > 0).astype(int)
    return update_boards

def check_winner(update_boards: List[np.ndarray]) -> int:
    winner_index = -1
    for index, board in enumerate(update_boards):
        board_row_size, board_column_size = board.shape
        column_sum = board.sum(axis=0)
        if (column_sum == board_column_size).sum() > 0:
            return index
        row_sum = board.sum(axis=1)
        if (row_sum == board_row_size).sum() > 0:
            return index
    return winner_index

def winning_score(bingo_board: np.ndarray, update_board: np.ndarray,
                  drawn_number: int) -> int:
    return sum(bingo_board[update_board == 0]) * drawn_number

def get_winning_board() -> int:
    bingo_boards = get_bingo_boards()
    update_boards = create_update_boards(bingo_boards)
    for number in draw_number():
        update_board(bingo_boards, update_boards, number)
        winning_board_index = check_winner(update_boards)
        if winning_board_index != -1:
            winning_board = bingo_boards[winning_board_index]
            winning_update_board = update_boards[winning_board_index]
            return winning_score(winning_board, winning_update_board, number)
    return -1

def get_last_winning_board() -> int:
    bingo_boards = get_bingo_boards()
    update_boards = create_update_boards(bingo_boards)
    for number in draw_number():
        update_board(bingo_boards, update_boards, number)
        broke_early = False
        while check_winner(update_boards) != -1:
            if len(bingo_boards) == 1:
                broke_early = True
                break
            winning_board_index = check_winner(update_boards)
            del bingo_boards[winning_board_index]
            del update_boards[winning_board_index]
        if len(bingo_boards) == 1 and broke_early:
            break
    return winning_score(bingo_boards[0], update_boards[0], number)

if __name__ == '__main__':
    print(f'Final score: {get_winning_board()}')
    print(f'Final score for the last winning bingo board: {get_last_winning_board()}')