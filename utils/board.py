from typing import List
from time import sleep

def get_progress(board: List[List[int]]) -> str:
    '''
    returns the progress of the algorithm
    '''
    visited_cell_count = sum(row.count(1) for row in board)
    total_cell_count = 64
    progress = (visited_cell_count / total_cell_count) * 100
    return f'{progress}%'

def update_board(board: List[List[int]]) -> None:
    '''
    print the updated board
    '''
    print_board(board, progress=True)

def print_board(board: List[List[int]], progress: bool = False, initialize: bool = False) -> None:
    '''
    print the board representation
    '''
    horizontal_line = '-' * 29
    vertical_line = '|' + ' ' * 29 + '|'

    board_representation = []
    board_representation.append(horizontal_line)

    for row in range(8):
        if 0 < row <= 7:
            board_representation.append(vertical_line)

        row_str = '|'
        for col in range(8):
            if board[row][col] == 1:
                row_str += '1'
            elif board[row][col] == 2:
                row_str += '2'
            else:
                row_str += '0'
            
            if col != 7:
                row_str += '   '

        row_str += '|'
        board_representation.append(row_str)
        
    board_representation.append(horizontal_line)

    if progress:
        board_representation.append(f'Completed: {get_progress(board)}')

    if initialize:
        board_representation.append('Initializing......')

    print('\n'.join(board_representation))
    sleep(0.1)