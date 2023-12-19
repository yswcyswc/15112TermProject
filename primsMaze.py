import random

"""
This file involves maze generation that uses Prim's Algorithm 
and is based on the explanations provided by 
https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm. 
I was also inspired by the pseudocode provided by https://medium.com/analytics-vidhya/maze-generations-algorithms-and-visualizations-9f5e88a3ae37#:~:text=Prim's%20Maze%20Generator%20is%20a,one%20to%20travel%20to%20next.
under section 4 'Prim's'
I also utilised the resource 112 TP guide "Fundamentals of Maze generation":
cs.cmu.edu/~112/notes/student-tp-guides/Mazes.pdf. 
"""

def generateMazePrims(size):
    infoDict = dict()

    # Creating the same width and height that aligns with the DFS generated algorithm
    # size = size * 2 - 1
    
    emptyPath = set() # recording all the potential cells that could be in the maze
    wallSet = set() # recording all 

    # Creating an empty board with 3x3 grids (one empty path in the centre
    # surrounded by walls) without any walls removed
    for row in range(size):
        for col in range(size):
            if (row == 0 or col == 0 or col == size - 1 or row == size - 1
                or row % 2 == 0 or col % 2 == 0):
                infoDict[(row, col)] = False
                wallSet.add((row, col))
            else:
                infoDict[(row, col)] = True
                emptyPath.add((row, col))
    
    mappedTo = set() # cells that have been mapped to by previous steps - they form the empty path

    infodict = generateMazeHelperPrims((1, 1), mappedTo, emptyPath, 
                                       wallSet, size, infoDict)
    
    outputboard = printMazePrims(infoDict, size)

    return outputboard

# A recursive implementation of Prim's algorithm
def generateMazeHelperPrims(currPos, mappedTo, emptyPath, wallSet, size, infoDict):
    
    wallsLeftUntouched = []

    mappedTo.add(currPos)

    for x in mappedTo:

        neighbours1 = findNeighboursPrims(x, size)
        neighbours2 = findMegaNeighboursPrims(x, size)
        neighboursList = []

        for i in range(len(neighbours1)):
            for x in range(len(neighbours2)):
                if i == x:
                    neighboursList.append((neighbours1[i], neighbours2[i]))
        
        for neighbour in neighboursList:

            neighbour1, neighbour2 = neighbour[0], neighbour[1]

            # Carving through paths
            # Scenario: If the current is a path, the neighbouring cell is a wall, 
            # and the 'mega' neighbour, which is the neighbouring cell of the 
            # neighbour cell at the same direction, is also a path (True), we
            # can remove the wall in between the cells 
            # Simply put: (True False True), then False can be changed to True

            # Storing cells that are not being confirmed as a wall (in the 
            # current wallSet), in the potential empty cells, and 
            # not being conirfed as an empty path
            if (neighbour1 in wallSet and ((neighbour2 in emptyPath) 
                and (neighbour2 not in mappedTo))):
                wallsLeftUntouched.append((neighbour1, neighbour2))
    
    # Base case of recusion: wallsLeftUntouched is the set of walls that 
    # are still in their intialised state, not being carved out. Hence, 
    # if the set is empty, the backtracking algorithm has covered the entire maze
    if len(wallsLeftUntouched) == 0:
        return infoDict

    else:
        random.shuffle(wallsLeftUntouched)
        newNeighbour1 = wallsLeftUntouched[0][0]
        infoDict[newNeighbour1] = True

        # accessing the nearest neighbour to mark it as mapped an empty cell 
        # and remove from the set of wall coordinates
        mappedTo.add(newNeighbour1)
        wallSet.remove(newNeighbour1)

        # accessing the 'mega neighbour' and marking it as mapped to
        newNeighbour2 = wallsLeftUntouched[0][1]
        mappedTo.add(newNeighbour2)

        # otherwise, recursively call the wrapper function to continue to 
        # find the neighborus of the 'mega neighbour'
        generateMazeHelperPrims(newNeighbour2, mappedTo, emptyPath, wallSet, 
                            size, infoDict)

def findNeighboursPrims(currPos, n):

    row, col = currPos
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbours = []

    for (x, y) in directions:
        targetRow, targetCol = row + x, col + y
        tr2, tc2 = row + x * 2, col + y * 2
        if isInBoardPrims(targetRow, targetCol, n) and isInBoardPrims(tr2, tc2, n):
            # records the rowPos and colPos of the connected cell
            neighbours.append((targetRow, targetCol))

    return neighbours

def findMegaNeighboursPrims(currPos, n):
    row, col = currPos
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbours = []

    for (x, y) in directions:
        targetRow, targetCol = row + x * 2, col + y * 2
        if isInBoardPrims(targetRow, targetCol, n):
            neighbours.append((targetRow, targetCol))

    return neighbours

def isInBoardPrims(targetRow, targetCol, n):
    return (targetRow < n and targetRow >= 0 
            and targetCol < n and targetCol >= 0)

def printMazePrims(infoDict, size):
    
    # Convert the dictionary to a list for output
    outputList = []

    for row in range(size):
        currRow = []
        for col in range(size):
            currRow.append(False)
        outputList.append(currRow)
    
    for row in range(len(outputList)):
        for col in range(len(outputList)):
            for (k1, k2) in infoDict:
                if (row, col) == (k1, k2) and infoDict[(k1, k2)]:
                    outputList[row][col] = infoDict[(k1, k2)]
    return outputList
