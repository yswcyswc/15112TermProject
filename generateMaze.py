from cmu_graphics import *
import random

'''
Online pseudocode
The depth-first search algorithm of maze generation is frequently implemented using backtracking. 
This can be described with a following recursive routine:

Given a current cell as a parameter
Mark the current cell as visited
While the current cell has any unvisited neighbour cells
    Choose one of the unvisited neighbours
    Remove the wall between the current cell and the chosen cell
    Invoke the routine recursively for the chosen cell
which is invoked once for any initial cell in the area.
'''
def generateMaze(size):
    '''
    Using DFS to generate all of the paths connected to a particular point. 
    Every point is stored at the key of a dictionary, and the paths connected to 
    it is stored as the value of the dictionary, in a list. 
    '''
    maze = {}
    prevCoord = (0, 0)
    nextCoord = (0, 1)
    generateMazeHelper(nextCoord, prevCoord, size, maze, count=0)
    return maze
    while True:
        solvedMaze = generateMazeHelper(nextCoord, prevCoord, size, maze, count=0)
        if solveMaze(size, solvedMaze, x=0, y=0):
            return maze

def generateMazeHelper(nextCoord, prevCoord, size, maze, count):

    # Base case: checks whether every cell in the maze is being mapped to
    if len(maze) == size ** 2 and nextCoord == (size - 1, size - 1):
        print('yes')
        return maze
    
    # recursive case
    else:

        # first check if the coordinates generated from the last round is legal
        if not isLegal(nextCoord[0], nextCoord[1], size, maze):
            return None
        
        # mark the current cell as visited
        if prevCoord in maze:
            maze[prevCoord].append(nextCoord)
        else:
            maze[prevCoord] = [nextCoord]

        currPosX, currPosY = (nextCoord[0], nextCoord[1])

        # choose one of the unvisted neighbours
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        random.shuffle(directions)

        # choosing one of the unvisited neighbours
        for (x, y) in directions:
            newPosX, newPosY = currPosX + x, currPosY + y

            # updating the values for prevCorod and nextCoord
            newPrevCoord = nextCoord
            newNextCoord = (newPosX, newPosY)
            count += 1

            # recursively calling the helper function to check the next neighbours
            solution = generateMazeHelper(newNextCoord, newPrevCoord, size, maze, count)
            if solution != None:
                return solution
            
        return generateMazeHelper(nextCoord, prevCoord, size, maze, count-1)     

def isLegal(row, col, n, maze):
    if isInBound(row, col, n) and isinMaze(row, col, maze):
        return True
    return False
    
def isInBound(row, col, n):
    if row <= n - 1 and row >= 0 and col <= n - 1 and col >= 0:
        return True 
    return False

def isinMaze(row, col, maze):
    for k in maze:
        if (row, col) == k or (row, col) in maze[k]:
            return False
    return True

def solveMaze(size, maze, x, y):
    print(size)
    if (x, y) == (size - 1, size - 1):
        return True
    else:    
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for i in directions:
            newX, newY = x + i[0], x + i[1]
            if ((newX + 1 <= size - 1 or newX - 1 >= 0 or newY + 1 <= size - 1 
                 or newY - 1 <= 0) and isinMaze(newX, newY, maze)):
                return solveMaze(size, maze, newX, newY)
            else:
                return solveMaze(size, maze, x, y)
    return False

