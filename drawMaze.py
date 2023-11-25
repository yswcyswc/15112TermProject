from cmu_graphics import *
from generateMaze import *

def onAppStart(app):
    reset(app)

def reset(app):
    app.currMaze = {}
    app.mazeGenerateN = 10
    app.mazeMap = generateMaze(app.mazeGenerateN)
    print(app.mazeMap)
    app.removeWallsList = findWallsToRemove(app.mazeMap, [], [])
    print("removeWallsList", app.removeWallsList)
    app.marginX = app.width / app.mazeGenerateN / 2
    app.marginY = app.height / app.mazeGenerateN / 2
    app.rows = app.mazeGenerateN
    app.cols = app.mazeGenerateN
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = app.mazeGenerateN / 4
    pass 

def findWallsToRemove(mazeMap, rowList, colList):
    for (x0, y0) in mazeMap:
        for (x1, y1) in mazeMap[(x0, y0)]:
            if y1 - y0 != 0:
                colList.append((x1, y1))
            elif x1 - x0 != 0:
                rowList.append((x1, y1))
    return (rowList, colList)


def addWallToDict(coord, dir, d):
    if coord not in d:
        d[coord] = ['dir']
    else:
        d[coord].append('dir')
    return d

def redrawAll(app):
    # drawMaze(app, app.mazeMap)
    drawBoard(app)
    drawBoardBorder(app)
    drawNumbers(app)

def drawNumbers(app): # for debugging purposes
    for i in range(app.mazeGenerateN):
        for x in range(app.mazeGenerateN):
            (a, b) = getCellLeftTop(app, i, x)
            drawLabel(f'({i}, {x})', a + 10, b + 10, size = 8)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
#             for i in app.mazeMap:
                # print(app.mazeMap)
                drawWalls(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='red',
           borderWidth=app.cellBorderWidth)

def drawWalls(app, row, col):
    if (row, col) not in app.removeWallsList[1]:
        cellLeft, cellTop = getCellLeftTop(app, row, col)
        cellWidth, cellHeight = getCellSize(app)
        drawLine(cellLeft, cellTop, cellLeft, cellTop + cellHeight, fill = 'red', lineWidth = app.mazeGenerateN / 4)
    if (row, col) not in app.removeWallsList[0]:
        cellLeft, cellTop = getCellLeftTop(app, row, col)
        cellWidth, cellHeight = getCellSize(app)
        drawLine(cellLeft, cellTop, cellLeft + cellWidth, cellTop, fill = 'red', lineWidth = app.mazeGenerateN / 4)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def drawMaze(app, mazeMap):
    for coord in mazeMap:
        for neighbour in mazeMap[coord]: 
            x1, y1 = coord 
            x2, y2 = neighbour
            connectLines(app, x1, y1, x2, y2)

def connectLines(app, x1, y1, x2, y2, n=10):
    startX = app.width / n * x1 + app.marginX
    startY = app.height / n * y1 + app.marginY
    endX = app.width / n * x2 + app.marginX
    endY = app.height / n * y2 + app.marginY
    drawLine(startX, startY, endX, endY)
def onKeyPress(app, key):
    if key == 'r':
        reset(app)
runApp()

