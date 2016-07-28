from PIL import Image
from PIL import ImageGrab
import time
import math

def screenGrab():
    im = ImageGrab.grab((305,370,1305,1020))
    im.save("shots/Screenshot"+str( math.floor( time.time() ) )+".png")

def main():
    screenGrab()

if __name__ == '__main__':
    main()
