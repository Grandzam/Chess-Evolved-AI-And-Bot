from PIL import Image
from PIL import ImageGrab
import numpy as np
import time
import sys

#this was what I used to change piece-names to piece-data, and a modification of this to add bgw and bgb
'''
with open("piece-data.txt", "r+") as f:
    newFile = ""
    currentNum = 1
    for line in f:
        newFile = newFile + str(currentNum)  + ' w_' + line.split()[1] + '\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' w_' + line.split()[1] + '+\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' w_' + line.split()[1] + '++\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' w_' + line.split()[1] + '+++\n'
        currentNum = currentNum+1

        newFile = newFile + str(currentNum)  + ' b_' + line.split()[1] + '\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' b_' + line.split()[1] + '+\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' b_' + line.split()[1] + '++\n'
        currentNum = currentNum+1
        newFile = newFile + str(currentNum)  + ' b_' + line.split()[1] + '+++\n'
        currentNum = currentNum+1

    f.write(newFile)
'''

#this is a temporary script I will use to help me figure out how to get IOBot to read pieces on the board
bX, bY = 303+260,368+85
sqSize = 60

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

def getSquare(x,y):
    pad = 8 #cut out 8 pixels from each side to get rid of the grey borders on squares
    sqImg = ImageGrab.grab(( bX + sqSize*x + pad, bY + sqSize*y + pad, bX + sqSize*(x+1) - pad, bY + sqSize*(y+1) - pad))
    sqImgData = np.array(sqImg)
    sqImg.save("shots/sq"+str(np.floor( time.time() ))+str(x+y)+".png")
    return sqImgData

#use commandline arguments to find the image of a piece add add it to piece data

#you must type "TempScript.py [piece name] [x] [y]"
#in order to add the image data of a black enemy pawn on their leftmost square(which is black), you would type:
#TempScript.py bgb_b_pawn 0 1
def addPieceRGBSumData():
    pieceName = sys.argv[1]
    x,y = int(sys.argv[2]),int(sys.argv[3])

    #get the image data for the piece
    imData = getSquare(x,y)

    r,g,b = sumRGBofImg(imData)
    
    #this is slow but it doesnt matter so much. It basically reads each line to see if it contains the name we are looking for
    #if it does, it adds the image data to that line
    #if not, it adds the line to the string and moves on

    with open("piece-data.txt", "r+") as f:
        newFile = ""
        for line in f:
            if line.split()[1] == pieceName:
                newFile = newFile + line.split()[0] + " " + pieceName + " " + str(r) + " " + str(g) + " " + str(b) + '\n'

            else:
                newFile = newFile + line


        #place pointer at beginning of the file so we overwrite it
        f.seek(0, 0);
        f.write(newFile)


def main():
    #imData = getSquare(0,0)
    #print(sumRGBofImg(imData))
    addPieceRGBSumData()

if __name__ == '__main__':
    main()
