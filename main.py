'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from decimal import *
from pixArray import *
from multiprocessing import Process, Queue

# Setup Defaults
#getcontext().prec = 10
# Mandelbrot World Parameters
xMin = -2.5
xMax = 1.5
yMin = -1.125
yMax = 1.125
xRange = abs(xMin) + abs(xMax)
yRange = abs(yMin) + abs(yMax)

imgWidth = 45
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
def mainAlgo(imgSrc,resultQueue):
    for i in range(0,imgWidth):
        for j in range(0,imgHeight):
            complexCoords = pixToIm(i, j)
            result = evaluate(complexCoords)
            if result[0] == True:
                imgSrc.setPixel(i, j, 0, 0, 0)
                #print "pixel" + str(i) + "," + str(j) + "In mandelbrot!"
            else:
                imgSrc.setPixel(i, j, 255, 255, 255)
                #print "pixel" + str(i) + "," + str(j) + "NOT In mandelbrot!"
    print "adding to queue!"
    result = imgSrc.getRaw()
    resultQueue.put(result)
                
if __name__ == "__main__":
    rowQ = Queue()
    for i in range(0,imgHeight):
        rowQ.add(i)
    rowQ.add("DONE")
    p1 = Process(target=mainAlgo,args=(imgSource,q,))
    #p2 = Process(target=mainAlgo,args=(imgSource2,q,))
    #q.put(imgSource)
    p1.daemon = True
    #p2.daemon = True
    p1.start()
    #p2.start()
    p1.join()
    #p2.join()
    res = q.get()
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