from PIL import Image
from PIL import ImageGrab
import numpy as np
import time

#this was what I used to change piece-names to piece-data
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

def getSquare(x,y):
    sqImg = ImageGrab.grab((bX+sqSize*x,bY+sqSize*y,bX+sqSize*(x+1),bY+sqSize*(y+1)))
    sqImgData = np.array(sqImg)
    sqImg.save("shots/sq"+str(np.floor( time.time() ))+str(x+y)+".png")
    return sqImgData

def main():
    getSquare(0,3)

if __name__ == '__main__':
    main()
