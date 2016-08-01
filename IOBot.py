#IOBot is a bot that can read the screen, and also move the mouse to do things on the screen
#it will communicate with a go AI to automatically play games
#TODO: it will also be able to do other trivial things like collect boxes and automatically play the challenge
#when it is avalible

from pynput.mouse import Button, Controller
from PIL import Image
from PIL import ImageGrab
import numpy as np
import time

mouse = Controller()

#temporary hack TODO: deal with this better
bgwNone = (493680,493680,493680)
bgbNone = (379456,379456,379456)

#a global for the size of the squares on the chess board in pixels just like everything else
sqSize = 60

#for some reason, in pynput, release and press are switched around, when I tested it out. Annoying but easy to deal with
pressMouse = mouse.release
releaseMouse = mouse.press

#when init is run, this is a 8x8 list of lists
board = []

def initBoard():
    for i in range(8):
        board.append([]) #adds a row
        for j in range(8):
            board[i].append(0) #fill them in with empty spaces

#index = piece id, value = tuple of its rgb sum
pieceImgData = []

#index = piece id, value = name
pieceNames = []

def initPieceData():
    with open("piece-data.txt") as f:
        for line in f:

            #if we dont have the rgbsum data, the length of the split line will be two

            if(len(line.split()) > 2):
                RGBSum = (int(line.split()[2]),int(line.split()[3]),int(line.split()[4]))
            else:
                RGBSum = (-1,-1,-1) #indicates that we have not yet got the rgbsum data for the piece

            pieceImgData.append(RGBSum)
            pieceNames.append(line.split()[1])

#takes in a greyscale numpy array of the screen and returns the width, height, x and y of the game screen
#This will get documentation eventually about how it works
def findGame(shotData):
    #iterate over every pixel in the screen, searching for the grey pixel in the top right of the game screen
    for i in range(shotData.shape[0]):
        for j in range(shotData.shape[1]):

            if shotData[i][j] == 95:
                #iterates over black pixels horizantally
                wideI = 1
                while shotData[i][j+wideI] == 0:
                    wideI=wideI+1
                #iterates over black pixels vertically
                highI = 1
                while shotData[i+highI][j] == 0:
                    highI=highI+1

                #match grey pixels
                if wideI>120 and highI>70 and shotData[i+highI][j]==31 and shotData[i][j+wideI]==95:
                    print("Game Found at X: " + str(j) + " Y: " + str(i) + " Width: " + str(wideI+1) + " Height " + str(highI+1) + '\n')
                    return j, i, wideI+1, highI+1

    print("Game screen unable to be found. Make sure the whole screen is visible, " +
    "or take a screenshot of your screen and report this as a bug. Also, make sure a menu that darkens the screen isn't" +
    " open, eg when you are selecting between challenge, ranked, or practice mode. Zoom must be at 100%")
    exit()

#take image data and sums its RGB. Is used for fast image recognition
def sumRGBofImg(imD):
    r = 0
    g = 0
    b = 0
    for i in range(imD.shape[0]):
        for j in range(imD.shape[1]):
            r = r+imD[i][j][0]
            g = g+imD[i][j][1]
            b = b+imD[i][j][2]
    return r,g,b

def getSquare(x,y,bX,bY):
    pad = 8 #cut out 8 pixels from each side to get rid of the grey borders on squares
    sqImg = ImageGrab.grab(( bX + sqSize*x + pad, bY + sqSize*y + pad, bX + sqSize*(x+1) - pad, bY + sqSize*(y+1) - pad))
    sqImgData = np.array(sqImg)

    return sqImgData

#takes the x y of a square and returns id,name
def readSquare(x,y,bX,bY):
    #first, read the square and get its rgb sum
    imData = getSquare(x,y,bX,bY)
    r,g,b = sumRGBofImg(imData)
    RGBSum = (r,g,b) #change it to tuple because the data is a tuple

    #print()

    if RGBSum == bgbNone or RGBSum == bgwNone:
        return 0,'none'

    #enumerate allows us to use index and value. index is the piece id for now
    for pId,value in enumerate(pieceImgData):
        #print("Checking " + str(RGBSum) + " against " + pieceNames[pId] + ": " + str(value))
        if RGBSum == value:
            return pId,pieceNames[pId]

    return -1,"unknown"



def readBoard(gameX,gameY):
    boardX, boardY = gameX+260, gameY+85

    #grab only the image of the board
    boardImg = ImageGrab.grab((boardX,boardY,boardX + sqSize*8,boardY + sqSize*8))
    boardImgData = np.array(boardImg)

    #loop each square and read the piece in that square
    for i in range(8):
        print("-------")
        for j in range(8):
            #print the name of each square
            print(readSquare(j,i,boardX,boardY)[1])


#drag mouse to the specified position slowly. In a game where speed matters, we wouldnt waste time moving, but this makes the bot feel smoother
def dragMouse(x,y):
    pressMouse(Button.left)
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
    releaseMouse(Button.left)

#TODO: make this work, with a tuple argument instead of a file. It used to work
#but it will require a trivial amount of modification and perferablly some other features
'''
def makeMove(moveFileName):
    move = open(moveFileName)
    moveStr = move.read()
    piece1x,piece1y,piece2x,piece2y = moveStr.split()

    piece1x,piece1y,piece2x,piece2y = int(piece1x),int(piece1y),int(piece2x),int(piece2y)

    print(piece1x,piece1y,piece2x,piece2y)

    moveMouse(GAME_X+BOARD_X+(piece1x*SQUARE_SIZE),GAME_Y+BOARD_Y+(piece1y*SQUARE_SIZE))
    dragMouse(GAME_X+BOARD_X+(piece2x*SQUARE_SIZE),GAME_Y+BOARD_Y+(piece2y*SQUARE_SIZE))
'''

def main():
    initBoard()
    initPieceData()

    #take a grayscale screenshot and make it a numpy array so we can read pixels from it
    im = ImageGrab.grab().convert('L')
    wholeGreyScreen = np.array(im)

    #must have 1920x1080 as of now, because images and pretty much anything about reading the screen is messed up in other resolutions
    #we can add other resolutions later
    #TODO: add Alex's resolution, whatever it ends up being
    resolution = wholeGreyScreen.shape
    if resolution!=(1080,1920):
        print(resolution)
        print("Currently, the only supported resolution is 1920x1080. Get a better monitor or request that your resolution be supported.")
        quit()

    #find game screen and put them into variables we can use.
    #TODO: make these globals somehow
    print("Finding Game Screen...")
    gameX,gameY,gameWidth,gameHeight = findGame(wholeGreyScreen)

    #change the board from its current default values to the values on the screen
    print("Reading Chess Board...")
    readBoard(gameX,gameY)


    #makeMove('testMoveData.txt')


if __name__ == '__main__':
    main()
