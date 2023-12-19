from cmu_graphics import *

from PIL import Image

import random

from DFSmaze import *

from primsMaze import *

"""
This file involves drawing mother duck and baby duck using methods created 
through OOP.
"""

class Duck:
    def __init__(self, app, x, y, num):
        (x, y) = getCellLeftTop(app, x, y)
        self.size = getCellSize(app)[0]
        self.x = x
        self.y = y
        self.right = True 
        self.left = False
        self.updown = False
        self.still = False
        self.visCircleR = app.width // 8
        # Creating the two different colours for the ducks in two player mode
        if num == 1:
            self.visCircleColour = 'white'
        else:
            self.visCircleColour = 'lightCyan'
        self.duckNum = num
        app.duckCount1 = 0
        app.duckCount2 = 0


        # CITATION: I learnt how to open images and animate sprites from 15112 Lectures and the piazza demo file
        # CITATION: These sprite sheets are from https://opengameart.org/content/character-spritesheet-duck 
        if self.duckNum == 1:
            self.runningDuck = [CMUImage(Image.open('run1.png')),
                                CMUImage(Image.open('run2.png'))]
            self.runningDuck2 = [CMUImage(Image.open('run3.png')),
                                CMUImage(Image.open('run4.png'))]
            self.runningDuck3 = [CMUImage(Image.open('stand.png')),
                                CMUImage(Image.open('crouch.png'))]
            self.stillDuck = CMUImage(Image.open('still.png'))
        
        self.deadDuck = CMUImage(Image.open('dead.png'))

        # CITATION: Used pixel editing tools to change the above 4 images to blue and created the second duck's positions
        if self.duckNum == 2: 
            self.runningDuck = [CMUImage(Image.open('run1 - 2.png')),
                                CMUImage(Image.open('run2 - 2.png'))]
            self.runningDuck2 = [CMUImage(Image.open('run3 - 2.png')),
                                 CMUImage(Image.open('run4 - 2.png'))]
            self.runningDuck3 = [CMUImage(Image.open('stand - 2.png')),
                                CMUImage(Image.open('crouch - 2.png'))]
            self.stillDuck = CMUImage(Image.open('still - 2.png'))
        

        self.currDuckPos = self.stillDuck 
    
    app.spriteCounter = 0

    def drawMotherDuck(self):
        if not app.onHold:
            self.currDuckPos = self.stillDuck
        elif self.right:
            self.currDuckPos = self.runningDuck[app.spriteCounter]
        elif self.left:
            self.currDuckPos = self.runningDuck2[app.spriteCounter]
        elif self.updown:
            self.currDuckPos = self.runningDuck3[app.spriteCounter]
        duckSize = getCellSize(app)[0]
        drawImage(self.currDuckPos, self.x, self.y, 
                  width = duckSize, height=duckSize)

    def drawVisCircle(self, app): 
        if not app.visible:
            drawCircle(self.x, self.y, self.visCircleR, 
                        fill = self.visCircleColour)
            
    def withinVisibilityRange(self, app, row, col):
        cellLeft, cellTop = getCellLeftTop(app, row, col)
        cellSize = getCellSize(app)[0]
        (rectCX, rectCY) = (cellLeft + cellSize / 2, cellTop + cellSize / 2)
        # To ensure that the baby duck seen is within the visibility circle 
        # after hint mode is turned off
        if distance(rectCX, rectCY, app.motherduck.x, app.motherduck.y) < self.visCircleR:
            return True
        return False
                
    def __repr__(self):
        return f'{self.x}, {self.y}'
    
class BabyDuck:
    def __init__(self, app, x, y):
        (x, y) = getCellLeftTop(app, x, y)
        self.size = getCellSize(app)[0]
        self.x = x
        self.y = y

    def checkIntersection(self, app, otherX, otherY):
        size = app.motherduck.size
        size -= size / 3

        left0, top0 = otherX, otherY
        right0, bottom0 = otherX + size, otherY + size

        left1, top1 = self.x, self.y
        right1, bottom1 = self.x + size, self.y + size

        if ((right0 >= left1) and (right1 >= left0) and (bottom0 >= top1) 
            and (bottom1 >= top0)):
            return True
        return False
    
    def withinVisibilityRangeBaby(self, app, x, y, r):
        cellSize = getCellSize(app)[0]
        (rectCX, rectCY) = (x + cellSize / 2, y + cellSize / 2)
        if distance(rectCX, rectCY, app.motherduck.x, app.motherduck.y) <= r:
            return True
        return False
    
def getCellLeftTop(app, row, col):
    '''Converting the row, col index into the left and top coordinates'''
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth // app.cols
    cellHeight = app.boardHeight // app.rows
    return (cellWidth, cellHeight)