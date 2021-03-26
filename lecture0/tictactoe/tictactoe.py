"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCounter = 0
    oCounter = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1

    if xCounter > oCounter:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    h = check_horizontally(board)
    v = check_vertically(board)
    d = check_diagonally(board)
    if v != None or d != None or h != None:
        if h == X or v == X or d == X:
            return X
        elif h == O or v == O or d == O:
            return O
        else:
            return None
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None or not any(EMPTY in sublist for sublist in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    curr_player = player(board)
    if terminal(board):
        return None
    else:
        if curr_player == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None
    curr_best = float('-inf')
    optimalMove = None
    for action in actions(board):
        v, garbageVal = min_value(result(board, action))
        if v > curr_best:
            curr_best = v
            optimalMove = action
            if curr_best == 1:
                return curr_best, optimalMove

    return curr_best, optimalMove


def min_value(board):
    if terminal(board):
        return utility(board), None

    curr_best = float('inf')
    optimalMove = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        v, garbageVal = max_value(result(board, action))
        if v < curr_best:
            curr_best = v
            optimalMove = action
            if v == -1:
                return v, optimalMove

    return curr_best, optimalMove
    
def check_horizontally(board):
    """
    Checks for any three-in-a-row horizontally on a board, if there is a winner, return it, otherwise, return None.
    """
    for i in board:
        if i[0] == i[1] and i[1] == i[2] and i[0] != EMPTY:
            if i[0] == X:
                return X
            else:
                return O
    
    return None

def check_vertically(board):
    """
    Checks for any three-in-a-row vertically on a board, if there is a winner, return it, otherwise, return None.
    """
    
    k = 0
    i = 0
    for k in range(3):
        if board[0][k] == board[1][k] == board[2][k] and board[0][k] != EMPTY:
            if board[i][k] == X:
                return X
            else:
                return O
    return None

def check_diagonally(board):
    """
    Checks for any three-in-a-row diagonally on a board, if there is a winner, return it, otherwise, return None.
    """
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        if board[0][0] == X:
            return X
        else:
            return O
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        if board[0][2] == X:
            return X
        else:
            return O
     return None
