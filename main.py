'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from pixArray import *
from pixRow import *
from multiprocessing import Process, Queue
import pickle

# Setup Defaults
#getcontext().prec = 10
# Mandelbrot World Parameters
xMin = -2.5
xMax = 1.5
yMin = -1.125
yMax = 1.125
xRange = abs(xMin) + abs(xMax)
yRange = abs(yMin) + abs(yMax)

imgWidth = 500
imgHeight = int(imgWidth*(yRange/xRange))
scaleFactor = float(imgWidth/xRange) 

# Start with a 300x300 image

imgSource = pixArray(imgWidth,imgHeight)
imgSource2 = pixArray(imgWidth,imgHeight)

def pixToIm(pixel_X,pixel_Y):
    '''
    Convert a pixel's xy coordinate into
    a complex number with decimal coefficients
    '''
    img_X = float(pixel_X)/scaleFactor + xMin # Div by scaleFactor maps to range [0,xRange].
    img_Y = float(pixel_Y)/scaleFactor + yMin
    return Complex(img_X,img_Y)

def evaluate(complexNumber):
    z_n = Complex(0,0)
    count = 0
    for i in range(0,200):
        z_nSquared = z_n.square()
        z_n = Complex(z_nSquared.Re + complexNumber.Re, z_nSquared.Im + complexNumber.Im)
        mod = z_n.modulus()
        if z_n.modulus() > 4:
            return False, count
        count += 1
    # Assume in mandelbrot
    return True, count
            

# Now run main algorithm
def processChunk(rowWidth,jobQueue,chunkHeight):
    while True:
        currChnk = jobQueue.get()
        currChnkPos = currChnk*chunkHeight
        
        if(currChnk == "DONE"):
            break
        
        '''If we are on the last chunk then do something slightly different'''
        if currChnkPos + chunkHeight - 1 > imgHeight:
            chunkHeight = imgHeight - currChnkPos
            
        rowArray = pixArray(rowWidth,chunkHeight)
        for i in range(0,rowWidth):
            for j in range(currChnkPos,currChnkPos + chunkHeight):
                complexCoords = pixToIm(i, j)
                result = evaluate(complexCoords)
                if result[0] == True:
                    rowArray.setPixel(i,j-currChnkPos, 0, 0, 0)
                    #print "pixel" + str(i) + "," + str(j) + "In mandelbrot!"
                else:
                    rowArray.setPixel(i,j-currChnkPos, 255, 255, 255)
                    #print "Setting pixel", i, j
                    #print "pixel" + str(i) + "," + str(j) + "NOT In mandelbrot!"
        tmpfile = open("out__CHUNK"+str(currChnk)+".tmp",'wb')
        pickle.dump(rowArray.getRaw(),tmpfile)
                
if __name__ == "__main__":
    print "Final image Size: "+str(imgWidth)+"x"+str(imgHeight)
    
    processes = []
    
    rowQ = Queue()
    '''list of 16 chunks + 1 potentially'''
    if(imgHeight % 16 == 0):
        for i in range(0,imgHeight/16):
            rowQ.put(i)
    else:
        '''account for the extra smaller chunk'''
        for i in range(0,imgHeight/16 + 1):
            rowQ.put(i)
    for i in range(0,8):
        rowQ.put("DONE")
    p1 = Process(target=processChunk,args=(imgWidth,rowQ,16))
    p2 = Process(target=processChunk,args=(imgWidth,rowQ,16))
    p1.daemon = True
    p2.daemon = True
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print "DONE!"
    

#png.from_array(imgSource.getRaw(), 'RGB').save('test.png')
# def evaluatePixel(xCoord,yCoord):
#     curr_zn_ = 0 # The variable that will be looped through the formula
#     count = 0 # No. of iterations
#     while curr_zn <=4:
#         
# def iterateMandelbrot(zn):
#     
# def squareComplex(re,im):