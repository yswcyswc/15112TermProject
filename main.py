from cmu_graphics import *

from PIL import Image

import random

from DFSmaze import *

from primsMaze import *

from printMaze import * 

"""
This file involves everything related to drawing the page (including drawing the 
lobby, the buttons, win page...) and small features that increase user experience.
"""

def onAppStart(app):
    app.size = 7
    app.twoplayer = False
    app.mode = 1
    reset(app)

def drawInstructions(app):
    '''Draws out everything related to the instructions page.'''
    drawRect(0, 0, app.width, app.height, fill = 'bisque')
    drawRect(10, app.height // 7, app.width // 2 - app.height // 20, 
             app.height // 4 * 3, fill = None, border = 'black', borderWidth = 2)
    drawRect(app.width // 2 + 10, app.height // 7, app.width // 2 - app.height // 20, 
             app.height // 4 * 3, fill = None, border = 'black', borderWidth = 2)
    keyL = ['↑ ↓ to move up, down', 
            '← → to move left, right',
            'r - restart the game',
            'm - back to menu page',
            'b - break walls', 
            'h - instructions',
            '= - increase maze size',
            '- - decrease maze size',
            'v - view the full maze',
            '2 - two player mode',
            '1 - one player mode',
            'WASD - move 2nd duck', 
            '3 - hide the ducks']
    context = [ 'Baby ducks are stuck', 
                'in the maze! Control',
                'mother duck to collect',
                'the baby ducks before', 
                'daylight comes! p.s.',
                'You have special powers', 
                'to break through walls',
                'Mode 1: standard (DFS)',
                "Mode 2: Prim's - harder",
                "with more dead ends"]
    
    drawImage(app.babyDuckImg, app.width // 4 * 3, 0, 
                  width=app.height // 6, height=app.height // 6)
    drawLabel('Instructions', app.width // 2, 
              app.height // 10, align = 'center', size = 25, 
              font = 'monospace', bold = True)
    drawLabel('Key commands: ', app.width // 4 * 3, 
              app.height // 10 * 2, align = 'center', size = 18, 
              font = 'monospace', bold = True)
    drawLabel('Context: ', app.width // 4 * 1, 
              app.height // 10 * 2, align = 'center', size = 18, 
              font = 'monospace', bold = True)

    
    for msgI in range(len(keyL)):
        drawKeys(app, keyL[msgI], 3, (msgI + 1) * 0.5)

    for contextI in range(len(context)):
        drawKeys(app, context[contextI], 1, (contextI + 1) * 0.5)

    drawBottom(app)

def drawLobby(app):
    drawImage(app.lobbyCover, app.width // 2, app.height // 2.2, 
              width=app.width + 50, height=app.width + 50,
              align = 'center')
    drawBottom(app)

def drawBottom(app):
    """Draws the bottom bar"""
    messages = ['Help', 'Mode 1', 'Mode 2', 'Start']
    if app.displayInstructions:
        messages = ['', 'Mode 1', 'Mode 2', 'Start']
        drawButtons(app, app.colourPal, messages)
        for i in range(3):
            drawImage(app.babyDuckImg, app.width // 35 + app.width // 15 * i, app.height - app.height // 12, 
                    width=30, height=30)
        
    if app.displayMenu:
        messages = ['Help', 'Mode 1', 'Mode 2', 'Start']
        drawButtons(app, app.colourPal, messages)
    
def drawButtons(app, colourPal, messages):
    for buttonIndex in range(len(messages)):
        colour = colourPal[buttonIndex]
        intervals = app.width // len(messages)
        drawRect(buttonIndex * intervals, app.height - app.height // 10, 
                app.width // 4, app.height // 10, fill = colour)
        drawLabel(messages[buttonIndex], 
                buttonIndex * intervals + app.width // 5 // 2, 
                app.height - app.height // 16, size = 20, font = 'monospace',
                bold = True)
        
def drawProgress(app):
    '''draws the progress bar'''
    drawRect(0, 0, app.width, app.height // 9, fill = 'peru')
    labelWidth = app.width // 3 * 2

    if app.maxDuckCount == app.duckCount1:
        bigRectColour = 'orange'
    else:
        bigRectColour = 'white'

    drawRect(app.width // 6, app.height // 15, labelWidth, app.height // 12,
             fill = bigRectColour, border = 'orange', align = 'left')
    
    startRect = (app.width - app.width // 3 * 2)

    barWidth = labelWidth // app.maxDuckCount * app.duckCount1

    if barWidth:
        drawRect(app.width // 6, app.height // 15, barWidth, app.height // 12,
                fill = 'orange', align = 'left')
        
    drawLabel(f'Ducks collected: {app.duckCount1}/{app.maxDuckCount}', 
              app.width // 2 + 30, app.height // 15, size=app.duckLabelFontSize, 
              align = 'right', font = 'monospace', bold = True)
    
    drawLabel(f'{app.breakCount}', app.width - 30, 30, size = 30,
              font = 'monospace', bold = True)
    
def drawKeys(app, msg, x, y):
    drawLabel(msg, app.width // 4 * x, app.height // 4.5 + app.height // 10 * y, 
              align = 'center', size = 15, font = 'monospace', bold = True)

def drawWin(app, msg):
    drawRect(0,0, app.width, app.height, fill = 'black', opacity = 70)
    drawRect(0, app.height // 2, app.width, app.height // 3, fill = 'brown', 
             align = 'left', opacity = 80)
    drawLabel(msg, app.width // 2, app.height // 2, align = 'center', 
              font = 'monospace', bold = True, size = app.height // 10)
    if not app.win:
        drawImage(app.motherduck.deadDuck, app.width / 3, app.height // 5 * 3,
                  width = app.width // 3, height = app.width // 3)
    
def redrawAll(app):
    if app.displayMenu:
        drawLobby(app)

    elif app.displayInstructions:
        drawInstructions(app)

    elif not app.gameOver and app.displayGame:
        if not app.visible:
            drawRect(0, 0, app.width, app.height, fill = 'black')
        drawVisCircle(app)
        drawBabyDuck(app)
        drawBoard(app)
        drawMotherDuck(app)
        drawProgress(app)
        if app.win: 
            drawWin(app, 'You won :)')
        if app.lose:
            drawWin(app, 'Game Over :(')

def main():
    runApp(width = 500, height = 550)

main()