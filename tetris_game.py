# Tetris Game

###################################
#Game desgin functions
###################################

#this helper function works for translate GRB code into colors
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

#set the customerized game dimensions
def gameDimensions(rows= 15, cols = 10, cellSize = 30, margin =35):
    dimension = (rows, cols, cellSize, margin)
    return dimension

#calculate window size based on game dimensions
def playTeris(dimension):
    width = dimension[1] * dimension[2] + 2 * dimension[3]
    height = dimension[0] * dimension[2] + 2 * dimension[3]
    run(width, height)

#define types of falling pieces
# Seven "standard" pieces (tetrominoes)
iPiece = [
         [  True,  True,  True,  True ]]

jPiece = [
         [  True, False, False ],
         [  True,  True,  True ]]

lPiece = [
         [ False, False,  True ],
         [  True,  True,  True ]]

oPiece = [
         [  True,  True ],
         [  True,  True ]]

sPiece = [
         [ False,  True,  True ],
         [  True,  True, False ]]

tPiece = [
         [ False,  True, False ],
         [  True,  True,  True ]]

zPiece = [
         [  True,  True, False ],
         [ False,  True,  True ]]

tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

#define falling pieces colors
tetrisPieceColors = [rgbString(226, 225, 228),rgbString(252, 211, 55), rgbString(173, 101, 152),
                     rgbString(67, 178, 68), rgbString(192, 44, 56), rgbString(205, 98, 39),rgbString(126, 22, 113)]

#randomly create new falling pieces
def newFallingPiece(data):
    import random
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = tetrisPieces[randomIndex]
    data.fallingPieceColor = tetrisPieceColors[randomIndex]
    data.fallingPieceCol = (data.cols - len(data.fallingPiece)) // 2
    data.fallingPieceRow = 0

#change falling piece position
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if fallingPieceIsLegal(data) == False: # if not legal, undo the change
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

#test whether or not the position of a falling piece is legal
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            rowNum = data.fallingPieceRow + row
            colNum = data.fallingPieceCol + col
            if data.fallingPiece[row][col] == True:
                if 0 <= rowNum < data.rows and 0<= colNum < data.cols and data.board[rowNum][colNum] == data.emptyColor:
                    continue
                else:
                    return False
    return True


#Below functions works for rotating the falling piece

def translateDimensions(oldDimensions):
    newRows = oldDimensions[1]
    newCols = oldDimensions[0]
    newDimensions = [newRows, newCols]
    return newDimensions

def translateLoaction(oldLocation, newDimensions):
    newRow = int(oldLocation[0]  + newDimensions[1] // 2 - newDimensions[0] //2)
    newCol = int(oldLocation[1] + newDimensions[0] // 2 - newDimensions[1] // 2)
    newLocation = [newRow, newCol]
    return newLocation

def translateFallingPiece(oldFallingPiece,newDimensions):
    emptyPiece = [([None] * newDimensions[1]) for i in range(newDimensions[0])]
    for row in range(len(oldFallingPiece)):
        for col in range(len(oldFallingPiece[0])):
            newCol = row
            newRow = len(oldFallingPiece[0]) - col - 1
            emptyPiece[newRow][newCol] = oldFallingPiece[row][col]
    newFallingPiece = emptyPiece
    return newFallingPiece

def rotateFallingPiece(data):
    import copy
    oldDimensions = [len(data.fallingPiece), len(data.fallingPiece[0])]
    oldLocation = [data.fallingPieceRow, data.fallingPieceCol]
    oldFallingPiece = copy.deepcopy(data.fallingPiece)
    newDimensions = translateDimensions(oldDimensions)
    newLocation = translateLoaction(oldLocation, newDimensions)
    newFallingPiece = translateFallingPiece(oldFallingPiece, newDimensions)
    data.fallingPiece = newFallingPiece
    data.fallingPieceRow = newLocation[0]
    data.fallingPieceCol = newLocation[1]
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = oldFallingPiece
        data.fallingPieceRow = oldLocation[0]
        data.fallingPieceCol = oldLocation[1]

#Below functions check for full rows and remove full rows
def isFullRows(data, row):
    for col in range(data.cols):
        if data.board[row][col] == data.emptyColor:
            return False
    return True

def removeFullRows(data):
    newBoard = []
    removeRows = 0
    import copy
    for row in range(data.rows):
        if isFullRows(data,row) == False:
            newBoard.append(data.board[row])
        else:
            removeRows += 1
    if len(newBoard) < data.rows:
        i = 0
        while i < (data.rows - len(newBoard)):
            newBoard.insert(0, data.emptyRow)
            i += 1
    data.board = copy.deepcopy(newBoard)
    #calculate scores:
    if removeRows == 1:
        data.fullRows += 1
    else:
        data.fullRows += (removeRows * 2)

###################################
#Animation functions
###################################

from tkinter import *

def init(data):
    data.timerDelay = 300
    dimension = gameDimensions()
    data.rows = dimension[0]
    data.cols = dimension[1]
    data.cellSize = dimension[2]
    data.margin = dimension[3]
    data.emptyColor = [rgbString(39, 117, 182)]
    data.emptyRow = [data.emptyColor] * data.cols
    data.backGround = [rgbString(254, 215, 26)]
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    #define falling piece shape and color
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors
    #initial data setting
    data.fallingPiece = [[]]
    data.fallingPieceRow = 0
    data.fallingPieceCol = 0
    data.isGameOver = False
    data.fullRows = 0


def drawCell(canvas,data,row,col):
    cellX = data.margin + col * data.cellSize
    cellY = data.margin + row * data.cellSize
    canvas.create_rectangle((cellX,cellY), (cellX + data.cellSize, cellY + data.cellSize),
                            width = 4, fill = data.board[row][col])

#draw cell that used for falling pieces
def drawFallingCell(canvas, data, row, col):
    cellX = data.margin + col * data.cellSize
    cellY = data.margin + row * data.cellSize
    canvas.create_rectangle((cellX, cellY), (cellX + data.cellSize, cellY + data.cellSize),
                            width = 4, fill = data.fallingPieceColor)

#draw the board by calling drawCell function repeatedly
def drawBoard(canvas, data):
    canvas.create_rectangle((0,0), (data.width, data.height), width = 0, fill = data.backGround)
    rows = data.rows
    cols = data.cols
    for row in range(rows):
        for col in range(cols):
            drawCell(canvas, data, row, col)
#draw game over message
    if data.isGameOver == True:
        canvas.create_rectangle((data.margin, data.margin + 2 * data.cellSize),
                                (data.width - data.margin, data.margin + 4 * data.cellSize), fill = 'black')
        canvas.create_text((data.width/2, data.margin + 3 * data.cellSize), text = 'Game Over!',
                           font = 'Helvetica 40 bold', fill = 'yellow')

def drawScore(canvas, data):
    canvas.create_text((data.width / 2, data.margin / 2), fill = rgbString(212, 37, 23),
                       text = 'Score: ' + str(data.fullRows), font = 'Helvetica 20 bold')

def drawFallingPiece(canvas,data):
    fallingPieceHeight = len(data.fallingPiece)
    fallingPieceWidth = len(data.fallingPiece[0])
    for col in range(fallingPieceWidth):
        for row in range(fallingPieceHeight):
            if data.fallingPiece[row][col]:
                rowNum = data.fallingPieceRow + row
                colNum = data.fallingPieceCol + col
                drawFallingCell(canvas, data, rowNum, colNum)
            else:
                continue

def placeFallingPiece(data):
    fallingPieceHeight = len(data.fallingPiece)
    fallingPieceWidth = len(data.fallingPiece[0])
    for col in range(fallingPieceWidth):
        for row in range(fallingPieceHeight):
            if data.fallingPiece[row][col]:
                rowNum = data.fallingPieceRow + row
                colNum = data.fallingPieceCol + col
                data.board[rowNum][colNum] = data.fallingPieceColor
    removeFullRows(data)


def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == 's':
        if data.isGameOver == False:
            newFallingPiece(data)
    elif event.keysym == 'Down':
        if data.isGameOver == False:
            moveFallingPiece(data, 1, 0)
    elif event.keysym == 'Up':
        if data.isGameOver == False:
            rotateFallingPiece(data)
    elif event.keysym == 'Left':
        if data.isGameOver == False:
            moveFallingPiece(data, 0, -1)
    elif event.keysym == 'Right':
        if data.isGameOver == False:
            moveFallingPiece(data, 0, 1)
    elif event.keysym == 'r':
        init(data)
        newFallingPiece(data)

def timerFired(data):
    if data.isGameOver == False:
        moveFallingPiece(data, 1, 0)
        if moveFallingPiece(data, 1, 0) == False:
            placeFallingPiece(data)
            newFallingPiece(data)
    #check the condition for when the game is over
    if fallingPieceIsLegal(data) == False:
        data.isGameOver = True


def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawScore(canvas, data)
    drawFallingPiece(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


playTeris(gameDimensions())

###########################
#Test functions
###########################

def testGameDimensions():
    print('Testing gameDimensions(): ', end = '')
    assert(gameDimensions() == (15, 10, 30, 35))
    assert (gameDimensions(30,10) == (30, 10, 30, 35))
    print('Passed.')
    return
'''
def testPlayTeris():
    print('Testing playTeris(): ', end ='')
    playTeris(gameDimensions(30,10))
    print('Passed.')
    return
'''
#################################################
# Hw6 Main
#################################################

def testAll():
    testGameDimensions()
    #testPlayTeris()

def main():
    testAll()

if __name__ == '__main__':
    main()