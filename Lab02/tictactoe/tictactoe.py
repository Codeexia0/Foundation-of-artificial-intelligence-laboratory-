"""
Tic Tac Toe Player
"""

import math
import copy # for deep copy

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
    countX =0
    countO = 0
    
    for row in range(len(board)):
        for col in range(len(board[0])): # 3
            if board[row][col] ==  X:
                countX += 1
            if  board[row][col] == O:
                countO += 1
                
    if countX > countO:
        return O
    else:
        return  X
            
            


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    allPossibleActions = set()
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if  board[row][col] == EMPTY:
                allPossibleActions.add((row,col))
            
    return allPossibleActions
                


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not valid action!")
    
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return  board_copy
    
def checkRow(board, player):
    for row in range(len(board)):
        if board[row][0] == player and  board[row][1] == player and board[row][2] == player:
            return True
    return False

def  checkCol(board, player):
    for col in range(len(board[0])):
        if  board[0][col] == player and  board[1][col] == player and board[2][col] ==  player:
            return  True
    return False

'''
def check_diagonals(board, player):

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True  
    return False
'''

def checkFirstDig(board,player):
    count = 0
    for row in range (len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                count += 1
    if count == 3:
         return True
    else:
         return False
     
     
def checkSecondDig(board, player):
    count = 0
    for row in range(len(board)):
        for col in range(len(board [row])):
            if (len(board) - row - 1) == col and board[row][col] == player:
                count += 1
    if count == 3:
        return True
    else:
        return False



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if checkRow(board, X) or checkCol(board, X) or checkFirstDig(board, X) or checkSecondDig(board, X):
        return X
    if checkRow(board, O) or checkCol(board, O) or checkFirstDig(board, O) or checkSecondDig(board, O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if  board[row][col] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        else:
            return 0

def max_value(board):
    v = - math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v




       
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Case of player is X (max_player)
    elif player(board) == X:
        plays = []
        for action in actions(board):   # Loop over the possible actions           
            # Add in plays list a tupple with the min_value and the action that results to its value
            plays.append([min_value(result(board,action)),action])     
        # Reverse sort for the plays list and get the action that should take
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1] # key=lambda x: x[0] tells sorted() to sort by the first element of each sublist in plays
        # By default, sorted() sorts in ascending order. Since reverse=True, it will sort in descending order
        # [0][1] returns the second element of the first sublist in plays
    # Case of player is O (min_player)
    elif player(board) == O:
        plays = []
        for action in actions(board):          
            plays.append([max_value(result(board,action)),action])     
        return sorted(plays, key=lambda x: x[0])[0][1]

