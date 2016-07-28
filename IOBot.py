from pynput.mouse import Button, Controller
import time

mouse = Controller()

#Measurements of the game interface relative to the whole screen. Hard coded in microsoft edge
#TODO: use image recognizer to find these variables so the bot isn't so fragile
GAME_WIDTH = 1000
GAME_HEIGHT = 650
GAME_X = 305
GAME_Y = 370

#measurements of the board relative to the game screen
BOARD_X = 285
BOARD_Y = 115

#size of a single square of the board
SQUARE_SIZE = 60

#when init is run, this is a 8x8 list of lists
board = []

def initBoard():
    for i in range(8):
        board.append([]) #adds a row
        for j in range(8):
            board[i].append(i+j) #fill them in with empty spaces

#piece names, initualized with the data in piece data
pieceNames = []

def initPieceNames():
    data = open('piece-data.txt')
    for line in data:
        index, value = line.split()
        pieceNames.append(value)

#move or drag mouse to the specified position slowly
#TODO: do it based on a sigmoid
def dragMouse(x,y):
    mouse.release(Button.left)
    currentX = float(mouse.position[0])
    currentY = float(mouse.position[1])

    xStep = -(currentX - x)/100
    yStep = -(currentY - y)/100
    #print(xStep,yStep)
    for i in range(100):
        currentX += xStep
        currentY += yStep
        mouse.position = (int(currentX),int(currentY))
        time.sleep(0.004)
    mouse.press(Button.left)

def moveMouse(x,y):
    currentX = float(mouse.position[0])
    currentY = float(mouse.position[1])

    xStep = -(currentX - x)/100
    yStep = -(currentY - y)/100
    #print(xStep,yStep)
    for i in range(100):
        currentX += xStep
        currentY += yStep
        mouse.position = (int(currentX),int(currentY))
        time.sleep(0.004)

def makeMove(moveFileName):
    move = open(moveFileName)
    moveStr = move.read()
    piece1x,piece1y,piece2x,piece2y = moveStr.split()

    piece1x,piece1y,piece2x,piece2y = int(piece1x),int(piece1y),int(piece2x),int(piece2y)

    print(piece1x,piece1y,piece2x,piece2y)

    moveMouse(GAME_X+BOARD_X+(piece1x*SQUARE_SIZE),GAME_Y+BOARD_Y+(piece1y*SQUARE_SIZE))
    dragMouse(GAME_X+BOARD_X+(piece2x*SQUARE_SIZE),GAME_Y+BOARD_Y+(piece2y*SQUARE_SIZE))


def main():
    initBoard()
    initPieceNames()
    #print(pieceNames)
    #print(pieceNames[board[7][2]])
    makeMove('testMoveData.txt')
    #mouse.position = (600,400)
    #dragMouse(100,100)

if __name__ == '__main__':
    main()
