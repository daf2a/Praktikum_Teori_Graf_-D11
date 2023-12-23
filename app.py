from flask import Flask, render_template, request
import copy
from typing import List
import random

app = Flask(__name__)

# -------------------- LARGEST INCREASING SUBSEQUENCE ALGORITHM ------------------------------

def find_lis(arr):# -> tuple[int, list]:
    n = len(arr)
    lis = [1] * n
    previous_indices = [-1] * n 

    for i in range(1, n):
        for j in range(0, i):
            if arr[i] > arr[j] and lis[i] < lis[j] + 1:
                lis[i] = lis[j] + 1
                previous_indices[i] = j

    max_length = max(lis)
    max_index = lis.index(max_length)

    lis_sequence = []
    while max_index >= 0:
        lis_sequence.append(arr[max_index])
        max_index = previous_indices[max_index]

    lis_sequence.reverse()
    return max_length, lis_sequence

# -------------------- KNIGHT'S TOUR ALGORITHM ------------------------------

class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
def knightsTour(board: List[List[int]], krow: int, kcol: int, isClosed: int) -> List[List[int]]:
    N = 8
    cx = [1, 1, 2, 2, -1, -1, -2, -2]
    cy = [2, -2, 1, -1, 2, -2, 1, -1]

    result_summary = []

    def limits(x, y):# -> Any:
        return ((x >= 0 and y >= 0) and (x < N and y < N))

    def isempty(a, x, y):
        return (limits(x, y)) and (a[y * N + x] < 0)

    def getDegree(a, x, y) -> int:
        count = 0
        for i in range(N):
            if isempty(a, (x + cx[i]), (y + cy[i])):
                count += 1
        return count

    def nextMove(a, cell):# -> Any | None:
        min_deg_idx = -1
        c = 0
        min_deg = (N + 1)
        nx = 0
        ny = 0

        start = random.randint(0, 1000) % N
        for count in range(0, N):
            i = (start + count) % N
            nx = cell.x + cx[i]
            ny = cell.y + cy[i]
            c = getDegree(a, nx, ny)
            if ((isempty(a, nx, ny)) and c < min_deg):
                min_deg_idx = i
                min_deg = c

        if (min_deg_idx == -1):
            return None

        nx = cell.x + cx[min_deg_idx]
        ny = cell.y + cy[min_deg_idx]

        a[ny * N + nx] = a[(cell.y) * N + (cell.x)] + 1

        cell.x = nx
        cell.y = ny

        return cell

    def boardSummary(a) -> None:
        for i in range(N):
            for j in range(N):
                result_summary.append((a[j * N + i], j, i))

    def isTourClosed(x, y, xx, yy) -> bool:
        for i in range(N):
            if ((x + cx[i]) == xx) and ((y + cy[i]) == yy):
                return True
        return False

    def findTour() -> bool:
        a = [-1] * N * N

        cell = Cell(kcol, krow)

        a[cell.y * N + cell.x] = 1

        ret = None
        for i in range(N * N - 1):
            ret = nextMove(a, cell)
            if ret == None:
                return False

        if(isClosed):
            if not isTourClosed(ret.x, ret.y, kcol, krow):
                return False
        boardSummary(a)
        return True

    
    while not findTour():
        pass

    return result_summary

# -------------------- CREATING CHESS BOARD ------------------------------

def create_board(steps, isClosed):
    board_size = 8
    result_boards = []

    first_row = steps[0][1]
    first_col = steps[0][2]

    last_row = steps[-1][1]
    last_col = steps[-1][2]

    for step in steps:
        board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        for s in steps[:steps.index(step) + 1]:
            board[s[1]][s[2]] = 1 if s != step else 2
            if s != step:
                board[first_row][first_col] = 3

        result_boards.append(copy.deepcopy(board))
    
    if(isClosed):
        board[last_row][last_col] = 1
        board[first_row][first_col] = 4
        result_boards.append(copy.deepcopy(board))
    else:
        result_boards.pop()
        board[last_row][last_col] = 4
        result_boards.append(copy.deepcopy(board))
    return result_boards

# -------------------- RENDERING PAGES ------------------------------

@app.route('/', methods=['GET', 'POST'])
def homepage() -> str:
    return render_template('home.html')

@app.route('/lis', methods=['GET', 'POST'])
def lis_route() -> str:
    lis_length = None
    lis_elements = None

    if request.method == 'POST':
        input_array = request.form.get('input_array')
        arr = list(map(int, input_array.split(',')))
        lis_length, lis_elements = find_lis(arr)
        
    return render_template('lis.html', lis_length=lis_length, lis_elements=lis_elements)

@app.route('/knight_tour', methods=['GET', 'POST'])
def knight_tour() -> str:
    start_position = request.form['start_position']

    tour_type = request.form['tour_type']
    board: List[List[int]] = [[0] * 8 for _ in range(8)]

    pos: List[int] = list(map(int, start_position.split(',')))

    if tour_type == '0':
        steps = knightsTour(board, pos[0], pos[1], 0)
        sorted_steps = sorted(steps, key=lambda x: x[0])
        result = create_board(sorted_steps, 0)
        summary = [(t[1], t[2]) for t in sorted_steps]
        summary_board = [(t[0]) for t in steps]
    else:
        steps = knightsTour(board, pos[0], pos[1], 1)
        sorted_steps = sorted(steps, key=lambda x: x[0])
        result = create_board(sorted_steps, 1)
        summary = [(t[1], t[2]) for t in sorted_steps]
        summary_board = [(t[0]) for t in steps]

    return render_template('knightstour.html', result=result, summary=summary, tour_type=tour_type, summary_board=summary_board)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')