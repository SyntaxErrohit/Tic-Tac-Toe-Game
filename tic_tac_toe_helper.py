def bestMove(board):
    bestVal, pos = -3, 0
    for i in range(9):
        if board[i] == '_':
            board[i] = 'O'
            val = myAlgorithm(False, board)
            board[i] = '_'
            if val > bestVal:
                bestVal, pos = val, i
    return pos

def myAlgorithm(state, board):
    for i in range(1, 8, 3):
        if board[i-1] == board[i] == board[i+1] != '_':
            return [-1,1][board[i]=='O']
    for i in range(3, 6, 1):
        if board[i-3] == board[i] == board[i+3] != '_':
            return [-1,1][board[i]=='O']
    if board[0] == board[4] == board[8] != '_':
        return [-1,1][board[4]=='O']
    if board[2] == board[4] == board[6] != '_':
        return [-1,1][board[4]=='O']
    if '_' not in board:
        return 0
    bestVal = [3, -3][state]
    for i in range(9):
        if board[i] == '_':
            board[i] = 'XO'[state]
            val = myAlgorithm(not state, board)
            board[i] = '_'
            bestVal = [min(val, bestVal), max(val, bestVal)][state]
    return bestVal