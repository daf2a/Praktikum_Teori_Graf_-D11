from flask import Flask, render_template, request
import os
import sys
from colorama import init, Fore
from time import sleep
import curses
import heapq
import copy
from typing import List, Tuple
from utils.input import print_dummy_board, clear, validate
from utils.board import print_board, update_board

app = Flask(__name__)

def find_lis(arr):
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

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@app.route('/lis', methods=['GET', 'POST'])
def lis_route():
    lis_length = None
    lis_elements = None

    if request.method == 'POST':
        input_array = request.form.get('input_array')
        arr = list(map(int, input_array.split(',')))
        lis_length, lis_elements = find_lis(arr)
        
    return render_template('lis.html', lis_length=lis_length, lis_elements=lis_elements)

def algorithmOpenTour(board: List[List[int]], krow: int, kcol: int) -> List[List[int]]:
    dx: List[int] = [1, 2, 2, 1, -1, -2, -2, -1]
    dy: List[int] = [-2, -1, 1, 2, 2, 1, -1, -2]

    result_steps = []
    result_summary = []

    board[krow][kcol] = 2
    result_steps.append(copy.deepcopy(board))
    result_summary.append((krow, kcol))
    
    for _ in range(64):
        board[krow][kcol] = 1
        pq: List[Tuple[int, int]] = [] 

        for i in range(8):
            nrow: int = krow + dx[i]
            ncol: int = kcol + dy[i]

            if 0 <= nrow <= 7 and 0 <= ncol <= 7 and board[nrow][ncol] == 0:
                count = 0
                for j in range(8):
                    nnrow: int = nrow + dx[j]
                    nncol: int = ncol + dy[j]

                    if 0 <= nnrow <= 7 and 0 <= nncol <= 7 and board[nnrow][nncol] == 0:
                        count += 1
                heapq.heappush(pq, (count, i))

        if len(pq) > 0:
            (p, m) = heapq.heappop(pq)
            krow += dx[m]
            kcol += dy[m]
            board[krow][kcol] = 2
            result_steps.append(copy.deepcopy(board))
            result_summary.append((krow, kcol))
        else:
            board[krow][kcol] = 1
            result_steps.append(copy.deepcopy(board))

    return result_steps, result_summary

# def algorithmClosedTour 

@app.route('/knight_tour', methods=['GET', 'POST'])
def knight_tour():
    start_position = request.form['start_position']
    #open tour 0 closed tour 1
    tour_type = request.form['tour_type']

    if not validate(start_position):
        return "Invalid input. Please enter position in the format 'row,col'."

    board: List[List[int]] = [[0] * 8 for _ in range(8)]

    pos: List[int] = list(map(int, start_position.split(',')))

    if tour_type == '0':
        result, summary = algorithmOpenTour(board, pos[0], pos[1])
    else:
        # ganti algoritma closed tour
        result, summary = algorithmOpenTour(board, pos[0], pos[1])

    return render_template('knightstour.html', result=result, summary=summary, tour_type=tour_type)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')