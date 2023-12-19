from cmu_graphics import *

from PIL import Image

import random

import math

from DFSmaze import *

from primsMaze import *

from duckClasses import *

"""
This file involves everything related to drawing the maze and drawing the ducks.
It converting the maze information (which is made up of a series of True and 
False values) to an actual maze that the user can easily navigate. 
This is done through setting up a board and assigning the False
values as the wall and True value as the empty path. 
"""

def reset(app):
    app.rows, app.cols = app.size, app.size
    if app.mode == 1:
        app.map = generateMaze(app.size)
        app.boardWidth = app.width // 2.3
        app.boardHeight = app.boardWidth
        app.boardLeft = (app.width - app.boardWidth * 2 - getCellSize(app)[0]) // 2
    elif app.mode == 2:
        app.map = generateMazePrims(app.size * 2 + 5)
        app.boardWidth = app.width / 3
        app.boardHeight = app.boardWidth
        app.boardLeft = (app.width - app.boardWidth * 2 - getCellSize(app)[0]) // 4
    app.boardHeight = app.boardWidth
    app.stepsPerSecond = 12
    app.cellBorderWidth = 0
    app.maxDuckCount = app.size + 3
    app.duckHeight = app.height / 10
    app.duckLabelFontSize = app.width / 33
    app.boardTop = (app.height - app.duckHeight)  // 6
    app.stepSize = 2 
    app.breakCount = 3
    app.babyChoices = generateBabyDuckCoordinates(app)
    app.visible = False

    app.motherduck = Duck(app, 1, 1, 1)
    if app.mode == 1:
        app.motherduck2 = Duck(app, app.size * 2 - 1, app.size * 2 - 1, 2)
    else:
        app.motherduck2 = Duck(app, app.size * 2 + 3, app.size * 2 + 3, 2)

    # Game Controls
    app.displayMenu = True
    app.displayGame = False
    app.gameOver = False
    app.paused = False
    app.displayInstructions = False
    app.win, app.lose = False, False
    app.selecting = False
    app.onHold = False
    app.counter = 0
    app.duckHint = True


    # Images
    # CITATION: I got Baby duck.png from https://pngtree.com
    app.babyDuckImg = CMUImage(Image.open('bbduck.png'))
    # CITATION: I generated 'coverImg.jpg' using Bing's OpenAI’s GPT-4 Model
    app.lobbyCover = CMUImage(Image.open('coverImg.jpg'))
    
    app.colourPal = ['sienna', 'burlyWood', 'sienna', 'burlyWood']

def getPathCoords(app, mazeMap):
    '''Gets the exact coordinates of the wall and returns values that the mother
    duck is not able to walk on after checking mother duck's intersection with 
    these areas'''
    pathCoords = []
    rows, cols = len(mazeMap), len(mazeMap[0])
    cellSize = getCellSize(app)[0]

    for row in range(rows):
        for col in range(cols):
            if not mazeMap[row][col]:
                wallL, wallT = getCellLeftTop(app, row, col)
                wallW, wallH = getCellSize(app)
                wallR, wallB = wallL + wallW, wallT + wallH

                pathCoords.append([wallL + cellSize / 10, 
                                   wallT + cellSize / 10, 
                                   wallR - cellSize / 10, 
                                   wallB - cellSize / 10]) 

    return pathCoords

def drawMotherDuck(app):
    app.motherduck.drawMotherDuck()
    if app.twoplayer:
        app.motherduck2.drawMotherDuck()

def drawVisCircle(app):
    if app.motherduck.visCircleR > 0:
        app.motherduck.drawVisCircle(app)
    if app.twoplayer:
        if app.motherduck2.visCircleR > 0:
            app.motherduck2.drawVisCircle(app)

def drawBabyDuck(app):
    '''Ensure that for the mode without baby duck hints, the ducks are only
    generated within the range of visibility'''
    if app.duckHint or app.visible:
        for babyDucks in app.babyChoices:
            drawImage(app.babyDuckImg, babyDucks.x, babyDucks.y, 
                    width=babyDucks.size, height=babyDucks.size)
    else:
        for babyDucks in app.babyChoices:
            if babyDucks.withinVisibilityRangeBaby(app, babyDucks.x, babyDucks.y, 
                                                app.motherduck.visCircleR):
                drawImage(app.babyDuckImg, babyDucks.x, babyDucks.y, 
                        width=babyDucks.size, height=babyDucks.size)

def onKeyHold(app, keys):
    app.onHold = True
    duckSize = getCellSize(app)[0]
    duck1C = [app.motherduck.x, app.motherduck.y, 
                   app.motherduck.x + duckSize, app.motherduck.y + duckSize]
    duck2C = [app.motherduck2.x, app.motherduck2.y,
                   app.motherduck2.x + duckSize, app.motherduck2.y + duckSize]
    
    if not app.paused and not app.win and not app.lose:
        if 'up' in keys:
            # Determining the direction of app.motherduck so that the correct sprite
            # can be chosen
            app.motherduck.right = False 
            app.motherduck.left = False
            app.motherduck.updown = True
            if canWalkThrough(duck1C[0], duck1C[1] - app.stepSize,  
                            duck1C[2], duck1C[3] - app.stepSize, app):
                app.motherduck.y -= app.stepSize 
                
        if 'down' in keys:
            app.motherduck.right = False 
            app.motherduck.left = False
            app.motherduck.updown = True
            if canWalkThrough(duck1C[0], duck1C[1] + app.stepSize,  
                            duck1C[2], duck1C[3] + app.stepSize, app):
                app.motherduck.y += app.stepSize                

        if 'left' in keys:
            app.motherduck.left = True
            app.motherduck.right = False
            app.motherduck.updown = False
            if canWalkThrough(duck1C[0] - app.stepSize, duck1C[1], 
                              duck1C[2] - app.stepSize, duck1C[3], app):
                app.motherduck.x -= app.stepSize

        if 'right' in keys:
            app.motherduck.right = True 
            app.motherduck.left = False
            app.motherduck.updown = False
            if canWalkThrough(duck1C[0] + app.stepSize, duck1C[1],
                              duck1C[2] + app.stepSize, duck1C[3], app):
                app.motherduck.x += app.stepSize 
        
        # Commands for the second duck
        if 'w' in keys:
            app.motherduck2.right = False 
            app.motherduck2.left = False
            app.motherduck2.updown = True
            if canWalkThrough(duck2C[0], duck2C[1] - app.stepSize,  
                            duck2C[2], duck2C[3] - app.stepSize, app):
                app.motherduck2.y -= app.stepSize 
                
        if 's' in keys:
            app.motherduck2.right = False 
            app.motherduck2.left = False
            app.motherduck2.updown = True
            if canWalkThrough(duck2C[0], duck2C[1] + app.stepSize,  
                            duck2C[2], duck2C[3] + app.stepSize, app):
                app.motherduck2.y += app.stepSize                

        if 'a' in keys:
            app.motherduck2.left = True
            app.motherduck2.right = False
            app.motherduck2.updown = False
            if canWalkThrough(duck2C[0] - app.stepSize, duck2C[1], 
                              duck2C[2] - app.stepSize, duck2C[3], app):
                app.motherduck2.x -= app.stepSize

        if 'd' in keys:
            app.motherduck2.right = True 
            app.motherduck2.left = False
            app.motherduck2.updown = False
            if canWalkThrough(duck2C[0] + app.stepSize, duck2C[1],
                              duck2C[2] + app.stepSize, duck2C[3], app):
                app.motherduck2.x += app.stepSize 

        if 'v' in keys:
            app.visible = True
    
    checkIntersection(app)

    if app.duckCount1 == app.maxDuckCount:
        app.win = True

    original = app.motherduck2.visCircleR

def canWalkThrough(x1, y1, x2, y2, app):
    '''After retrieving the possible coordinates in the form of 
    [topX, topY, bottomX, bottomY], this function checks the intersection between
    the motherduck and these 'forbidden' zones'''
    pathCoords = getPathCoords(app, app.map)
    left0, top0 = x1, y1
    right0, bottom0 = x2, y2
    
    for i in pathCoords:

        left1, top1 = i[0], i[1]
        right1, bottom1 = i[2], i[3]

        # Check whether the duck's 4 corners intersect with any of the walls
        if ((right0 > left1) and (right1 > left0) and (bottom0 > top1) 
            and (bottom1 > top0)):
            return False
    return True

def generateBabyDuckCoordinates(app):
    coordList = []

    for row in range(len(app.map)):
        for col in range(len(app.map[0])):

            # Avoiding two possibilities that the ducks are generated 
            # at the place where the mother duck is spawn
            if (app.map[row][col] and ((row, col) != (1, 1))
                and ((row, col) != (app.size * 2 - 1, app.size * 2 - 1))):
                coordList.append(BabyDuck(app, row, col))

    # CITATION: I learnt the method random.shuffle from https://www.w3schools.com/python/ref_random_shuffle.asp
    random.shuffle(coordList)
    return coordList[:app.maxDuckCount]

def onMouseMove(app, mouseX, mouseY):

    # check if the mouse is hovering on the start button
    if (mouseX > (app.width - app.width // 4) and (mouseX < app.width) and
        mouseY <= app.height and mouseY >= (app.height - app.height // 10)):
        app.colourPal[3] = 'peru'
    else:
        app.colourPal[3] = 'burlyWood'

    # check if the mouse is hovering on the help button
    if ((mouseX > 0) and (mouseX < app.width // 4) and 
        (mouseY > app.height - app.height // 10) and mouseY < app.height):
        app.colourPal[0] = 'peru'
    else:
        app.colourPal[0] = 'sienna'
        
def onMousePress(app, mouseX, mouseY):
    
    if app.displayInstructions or app.displayMenu:
        # Checks if the mouse is pressing the start button
        if (mouseX > (app.width - app.width // 4) and 
            mouseY <= app.height and mouseY >= (app.height - app.height // 10)):
            app.displayMenu = False
            app.displayGame = True
            app.displayInstructions = False
            app.paused = False

        # Checks if the mouse is pressing the help button
        if ((mouseX > 0) and (mouseX < app.width // 4) and 
            (mouseY > app.height - app.height // 10) and mouseY < app.height):
            if app.displayInstructions:
                app.displayMenu = True
                app.displayGame = False
                app.displayInstructions = False
            else:
                app.displayMenu = False
                app.displayGame = False
                app.displayInstructions = True
            
            # check if the mouse is pressing the mode1 button
        if ((mouseX > app.width // 4) and (mouseX < app.width // 4 * 2) and 
            (mouseY > app.height - app.height // 10) and mouseY < app.height):
            app.mode = 1
            reset(app)
            app.colourPal[1] = 'lemonChiffon'
            app.colourPal[2] = 'sienna'

        # check if the mouse is pressing the mode2 button
        if ((mouseX > app.width // 4 * 2) and (mouseX < app.width // 4 * 3) and 
            (mouseY > app.height - app.height // 10) and mouseY < app.height):
            app.mode = 2
            reset(app)
            app.colourPal[2] = 'lemonChiffon'
            app.colourPal[1] = 'burlywood'
    
    if app.selecting:
        breakWall(app, mouseX, mouseY)
      
def breakWall(app, x, y):
    
    solution = app.map

    for row in range(len(solution)):
        for col in range(len(solution[row])):
                
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                
                # Ensuring that the grey wall is within the range of visibility
                # since the maze is drawn on top of the black background
                if (x > cellLeft and x < cellLeft + cellWidth 
                    and y > cellTop and y < cellTop + cellHeight and
                    not app.map[row][col]): 

                    app.map[row][col] = 'grey'
                    app.breakCount -= 1
                    app.paused = False 
                    app.selecting = False
                    
def checkIntersection(app):
    '''Checks intersection of mother duck and baby duck'''
    for babyDucks in app.babyChoices:
        if babyDucks.checkIntersection(app, app.motherduck.x, app.motherduck.y):
            app.babyChoices.remove(babyDucks)
            app.duckCount1 += 1
        if babyDucks.checkIntersection(app, app.motherduck2.x, app.motherduck2.y):
            app.babyChoices.remove(babyDucks)
            app.duckCount1 += 1

def drawBoard(app):
    '''This function draws the entire maze's walls by calling the drawWalls 
    function for every True/False value it encountered'''
    solution = app.map
    for row in range(len(solution)):
        for col in range(len(solution[row])):
            if solution[row][col] == 'grey':
                # CITATION: colour from https://academy.cs.cmu.edu/docs/builtInColors
                if app.motherduck.withinVisibilityRange(app, row, col):
                    # If it is not within visibility range, hide it from the canvas (otherwise will appear)
                    colour = 'gainsboro'
                else:
                    colour = None
                drawWalls(app, row, col, colour, 'modifiedPath')
            elif solution[row][col]:
                colour = None
                drawWalls(app, row, col, colour, 'path')
            else:
                colour = 'black'
                drawWalls(app, row, col, colour, 'wall')

def drawWalls(app, row, col, colour, info):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=colour, border=None,
                borderWidth=app.cellBorderWidth)

def onKeyPress(app, key):
    app.paused = False
    if key == 'm':
        reset(app)
    elif app.displayGame and key == 'r':
        reset(app)
        app.displayMenu = False
        app.displayGame = True
    elif key == '2':
        reset(app)
        app.twoplayer = True
        app.displayMenu = False
        app.displayGame = True
    
    elif key == '1':
        reset(app)
        app.twoplayer = False
        app.displayMenu = False
        app.displayGame = True
    
    if key == 'h':
        app.displayInstructions = True
        app.paused = True
    
    if app.breakCount > 0:
        if key == 'b':
            app.paused = True
            app.selecting = True

    if key == '=':
        if app.size < 12:
            app.size += 1
        reset(app)
        app.displayMenu = False
        app.displayGame = True
    elif key == '-':
        if app.size > 7:
            app.size -= 1
        reset(app)
        app.displayMenu = False
        app.displayGame = True
    
    if key == '3':
        app.duckHint = not app.duckHint

def onStep(app):
    app.onHold = False
    app.visible = False
    if (not app.gameOver and app.displayGame and not app.paused 
        and not app.win and not app.lose):
        app.counter += 1
        if app.counter == 10:
            app.counter = 0
            if not app.twoplayer:
                app.motherduck.visCircleR += 2
                app.motherduck2.visCircleR += 2
            else:
                # The visibility circle's radius changes at a higher rate for
                # two player mode, otherwise it is too easy
                app.motherduck.visCircleR += 6
                app.motherduck2.visCircleR += 6
        
        if (entireVisible(app, app.motherduck.x, app.motherduck.y) 
            or entireVisible(app, app.motherduck2.x, app.motherduck2.y)):
            app.lose = True

        app.spriteCounter = (1 + app.spriteCounter) % len(app.motherduck.runningDuck)

def entireVisible(app, x, y):
    # checks the distance between the centre of the circle and the four edge
    # If it is greater than the radius, then the player loses the game
    r = app.motherduck.visCircleR
    d1TL = distance(x, y, 0, 0)
    d1TR = distance(x, y, app.width, 0)
    d1BL = distance(x, y, 0, app.height)
    d1BR = distance(x, y, app.width, app.height)
    return d1TL < r and d1TR < r and d1BL < r and d1BR < r

def distance(x0, y0, x1, y1):
    return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

