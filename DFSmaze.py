import random

"""
This file involves maze generation that uses Depth First Search Algorithm 
and is based on the pseudocode and explanations provided by 
https://en.wikipedia.org/wiki/Maze_generation_algorithm under the 
"recursive implementation" section header and the 112 TP guide "Fundamentals
of Maze generation" cs.cmu.edu/~112/notes/student-tp-guides/Mazes.pdf. 
"""

def generateMaze(n):
    boardInfoDict = {}
    # initialising boardInfoDict
    for row in range(n):
        for col in range(n):
            # Information of each (row, col) - the keys
            # - Index 0 is whether it has been visited. 
            # - Index 1 records whether there are walls on its left, right, up
            #   down directions. 
            boardInfoDict[(row, col)] = [False, [True, True, True, True]]
    startingPos = (0, 0)
    boardInfoDict = generateMazeHelper(startingPos, boardInfoDict, n)
    outputMaze = printMaze(n, boardInfoDict)
    return outputMaze

def generateMazeHelper(currentPos, boardInfoDict, n):
    boardInfoDict[currentPos][0] = True
    # find the potential next steps of the current position
    neighbours = findNeighbours(currentPos[0], currentPos[1], n, boardInfoDict)
    if allVisited(boardInfoDict):
        return boardInfoDict
    else:
        if neighbours:
            # CITATION: I learnt the method random.shuffle 
            # from https://www.w3schools.com/python/ref_random_shuffle.asp
            random.shuffle(neighbours)
            randomNext = neighbours[0]
            carvePath(currentPos, randomNext, boardInfoDict)
            solution = generateMazeHelper(randomNext, boardInfoDict, n)
            if solution != None:
                return solution
            else:
                solution = generateMazeHelper(currentPos, boardInfoDict, n)
                return solution

def allVisited(boardInfoDict):
    for key in boardInfoDict:
        if not boardInfoDict[key][0]:
            return False 
    return True 

def findNeighbours(row, col, n, infoDict):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbours = []
    for (x, y) in directions:
        targetRow, targetCol = row + x, col + y
        if isInBoard(targetRow, targetCol, n):
            isVisited = infoDict[(targetRow, targetCol)][0]
            # records the rowPos and colPos of the connected cell
            if not isVisited:
                neighbours.append((targetRow, targetCol))
    return neighbours
 
def carvePath(current, randomNext, board):
    currentRow, currentCol = current[0], current[1]
    nextRow, nextCol = randomNext[0], randomNext[1]
    if nextCol > currentCol:
        board[(current)][1][1] = False
        board[(randomNext)][1][0] = False 
    if nextCol < currentCol:
        board[(current)][1][0] = False
        board[(randomNext)][1][1] = False
    if nextRow < currentRow:
        board[(current)][1][2] = False
        board[(randomNext)][1][3] = False
    if nextRow > currentRow:
        board[(current)][1][3] = False
        board[(randomNext)][1][2] = False 
        
def printMaze(n, boardInfoDict):
    outputBoard = printInitialMaze(n)
    outputBoard = addWall(outputBoard, boardInfoDict, n)
    return outputBoard

def printInitialMaze(n):
    outputBoard = []
    # creating paths and walls that before removing and adding the walls
    # Since every cell = the empty path itself + the wall on the right, we need
    # 2n + 1 cells 
    numCol = 2 * n + 1
    for row in range(numCol):
        if row % 2 == 0:
            currentRow = []
            for col in range(numCol):
                if row % 2 == 0:
                    if col % 2 == 0:
                        currentRow.append(False)
                    else:
                        currentRow.append(True)
            outputBoard.append(currentRow)
        else:
            outputBoard.append([True] * numCol)
    return outputBoard

def addWall(outputBoard, infoDict, n):
    count = 0
    for rowI in range(n):
        for colI in range(n):
            count += 1
            for wallInstructions in range(len(infoDict[(rowI, colI)][1])):
                if infoDict[(rowI, colI)][1][wallInstructions]:
                    if wallInstructions == 0:
                        outputBoard[rowI * 2 + 1][colI * 2] = False
                    if wallInstructions == 1:
                        outputBoard[rowI * 2 + 1][colI * 2 + 2] = False
                    if wallInstructions == 2:
                        outputBoard[rowI * 2][colI * 2 + 1] = False
                    if wallInstructions == 3:
                        outputBoard[rowI * 2 + 2][colI * 2 + 1] = False
    return outputBoard

def isInBoard(targetRow, targetCol, n):
    return (targetRow < n and targetRow >= 0 
            and targetCol < n and targetCol >= 0)