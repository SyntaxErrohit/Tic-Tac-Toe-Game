from tic_tac_toe_helper import bestMove

def printAdv():
    for i in range(0, 7, 3):
        print(*board[i:i+3])

def inputAdvHuman():
    pos = int(input('Enter position: '))-1
    if board[pos] == '_':
        print()
        board[pos] = 'X'
    else:
        print('Try again')
        inputAdvHuman()

def inputAdvComputer():
    if '_' in board:
        result = bestMove(board)
        board[result] = 'O'

def check():
    for i in range(1, 8, 3):
        if board[i-1] == board[i] == board[i+1] != '_':
            return board[i] + ' wins !!'
    for i in range(3, 6, 1):
        if board[i-3] == board[i] == board[i+3] != '_':
            return board[i] + ' wins !!'
    if board[0] == board[4] == board[8] != '_':
        return board[4] + ' wins !!'
    if board[2] == board[4] == board[6] != '_':
        return board[4] + ' wins !!'
    return 'NA' if '_' in board else 'Tie !!'

board = ['_']*9

while True:
    printAdv()
    inputAdvHuman()
    inputAdvComputer()
    result = check()
    if result != 'NA':
        print(result+'\n')
        printAdv()
        break