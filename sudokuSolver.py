import numpy as np

board = np.array([[0,0,7,1,5,0,9,0,0],
                  [0,0,9,4,3,0,0,0,0],
                  [5,0,0,0,0,2,0,1,3],
                  [0,0,6,5,0,4,0,2,9],
                  [4,3,0,0,8,0,0,5,7],
                  [9,7,0,3,0,1,4,0,0],
                  [7,6,0,2,0,0,0,0,5],
                  [0,0,0,0,9,6,2,0,0],
                  [0,0,3,0,4,5,6,0,0]])

def solve(board):
    if isBoardFull(board):
        return True

    row, column = nextZeroPos(board)
    possibleMoves = possibleNumbers(board, row, column)

    if not possibleMoves:
        return False

    else:
        for move in possibleMoves:
            board[row][column] = move
            if solve(board):
                return True
            board[row][column] = 0

def isBoardFull(board):
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return False

    return True

def nextZeroPos(board):
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return (row, column)

def possibleNumbers(board, row, column):
    possibleNumOnRow = possibleNumbersOnRow(board, row)
    possibleNumOnColumn = possibleNumbersOnColumn(board, column)
    possibleNumOnSquares = possibleNumbersOnSquares(board, row, column)

    return intersectPossibilities(possibleNumOnRow, possibleNumOnColumn, possibleNumOnSquares)

def possibleNumbersOnRow(board, row):
    possibilities = [1,2,3,4,5,6,7,8,9]

    for column in range(9):
        num = board[row][column]

        if num != 0 and num in possibilities:
            possibilities.remove(num)

    return possibilities

def possibleNumbersOnColumn(board, column):
    possibilities = [1,2,3,4,5,6,7,8,9]

    for row in range(9):
        num = board[row][column]

        if num != 0 and num in possibilities:
            possibilities.remove(num)

    return possibilities

def possibleNumbersOnSquares(board, row, column):
    possibilities = [1,2,3,4,5,6,7,8,9]

    startRow = row - (row % 3)
    startColumn = column - (column % 3)

    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            num = board[i][j]

            if num != 0 and num in possibilities:
                possibilities.remove(num)

    return possibilities

#Try to write without using intersection()
def intersectPossibilities(*args):
    unionList = []

    for value in args:
        unionList.append(set(value))

    return list(unionList[0].intersection(*unionList))


