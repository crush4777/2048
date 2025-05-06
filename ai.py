import os
import tensorflow as tf
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

def move_row(row):
    new_row = []
    prev = None
    score = 0
    for num in row:
        if num != 0:
            if prev is None:
                prev = num
            else:
                if prev == num:
                    new_row.append(prev * 2)
                    score += prev * 2
                    prev = None
                else:
                    new_row.append(prev)
                    prev = num
    if prev is not None:
        new_row.append(prev)
    new_row += [0] * (4 - len(new_row))
    return new_row, score


def move_left(board):
    new_board = []
    total_score = 0
    for row in board:
        moved_row, s = move_row(row)
        new_board.append(moved_row)
        total_score += s
    return new_board, total_score


def move_right(board):
    new_board = []
    total_score = 0
    for row in board:
        reversed_row = row[::-1]
        moved_row, s = move_row(reversed_row)
        new_board.append(moved_row[::-1])
        total_score += s
    return new_board, total_score


def move_up(board):
    transposed = list(zip(*board))
    new_transposed = []
    total_score = 0
    for row in transposed:
        moved_row, s = move_row(list(row))
        new_transposed.append(moved_row)
        total_score += s
    new_board = list(zip(*new_transposed))
    return [list(r) for r in new_board], total_score


def move_down(board):
    transposed = list(zip(*board))
    new_transposed = []
    total_score = 0
    for row in transposed:
        reversed_row = list(row)[::-1]
        moved_row, s = move_row(reversed_row)
        new_transposed.append(moved_row[::-1])
        total_score += s
    new_board = list(zip(*new_transposed))
    return [list(r) for r in new_board], total_score


def is_move_valid(original, new_board):
    for i in range(4):
        for j in range(4):
            if original[i][j] != new_board[i][j]:
                return True
    return False


def simulate_move(board, direction):
    original = [row.copy() for row in board]
    if direction == 'left':
        new_board, score = move_left(original)
    elif direction == 'right':
        new_board, score = move_right(original)
    elif direction == 'up':
        new_board, score = move_up(original)
    elif direction == 'down':
        new_board, score = move_down(original)
    else:
        return None, 0, False
    valid = is_move_valid(original, new_board)
    return new_board, score, valid


def count_empty(board):
    return sum(row.count(0) for row in board)


def calculate_smoothness(board):
    smooth = 0
    for i in range(4):
        for j in range(4):
            if j < 3:
                smooth += abs(board[i][j] - board[i][j + 1])
            if i < 3:
                smooth += abs(board[i][j] - board[i + 1][j])
    return smooth


def calculate_monotonicity(board):
    mono_score = 0
    for row in board:
        inc = dec = True
        for i in range(3):
            if row[i] > row[i + 1]:
                inc = False
            if row[i] < row[i + 1]:
                dec = False
        if inc or dec:
            mono_score += max(row)
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        inc = dec = True
        for i in range(3):
            if column[i] > column[i + 1]:
                inc = False
            if column[i] < column[i + 1]:
                dec = False
        if inc or dec:
            mono_score += max(column)
    return mono_score


def is_max_in_corner(board):
    max_tile = max(max(row) for row in board)
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    for i in range(4):
        for j in range(4):
            if board[i][j] == max_tile and (i, j) in corners:
                return True
    return False


def evaluate_board(board):
    empty = count_empty(board)
    smooth = calculate_smoothness(board)
    mono = calculate_monotonicity(board)
    max_corner = 100 if is_max_in_corner(board) else 0
    return empty * 10 + mono * 2 - smooth + max_corner


def analyze_moves(chess_nums):
    directions = ['left', 'right', 'up', 'down']
    valid_moves = []

    for dir in directions:
        new_board, score, valid = simulate_move(chess_nums, dir)
        if valid:
            empty = count_empty(new_board)
            eval_value = evaluate_board(new_board)
            valid_moves.append({
                'direction': dir,
                'score': score,
                'empty': empty,
                'eval': eval_value
            })

    if not valid_moves:
        return "No valid move"

    algo1 = max(valid_moves, key=lambda x: x['score'], default=None)
    algo2 = max(valid_moves, key=lambda x: x['empty'], default=None)
    algo3 = max(valid_moves, key=lambda x: x['eval'], default=None)

    result = [
        f"Greedy: {algo1['direction']}\n",
        f"Maximum: {algo2['direction']}\n",
        f"Comprehensive: {algo3['direction']}",
    ]
    return algo1['direction'], algo2['direction'], algo3['direction'], result






def rl_analyze_moves(chess_nums):
    chess_nums = np.array(chess_nums).reshape(1, 4, 4, 1)
    model = tf.keras.models.load_model(r'D:\2048V2\2048\RL\models\2048_model_final.h5',
                                       custom_objects={'custom_loss': 'categorical_crossentropy'})
    predictions = model.predict(chess_nums, verbose=0)[0]
    print('model.predict(state, verbose=0)', model.predict(chess_nums, verbose=0))
    print('predictions:', predictions)

    moves = ['up', 'down', 'left', 'right']
    move_probs = list(zip(moves, predictions))
    move_probs.sort(key=lambda x: x[1], reverse=True)

    # Try moves in order of confidence until a valid one is found
    for move, prob in move_probs:
        print('move, prob:', move, prob)
            #return move, prob
    move_probs_dict = dict(move_probs)
    print('move_probs_dict:', move_probs_dict)
    move_probs_dict = {key: round(float(value), 2) for key, value in move_probs_dict.items()}
    print(move_probs_dict)
    return move_probs_dict