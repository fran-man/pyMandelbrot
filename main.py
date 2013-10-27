'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from decimal import *
from pixArray import *

# Setup Defaults
getcontext().prec = 10
# Mandelbrot World Parameters
xMin = -2
xMax = 1
yMin = -0.845
yMax = 0.845
xRange = abs(xMin) + abs(xMax)
yRange = abs(yMin) + abs(yMax)

imgWidth = 40
imgHeight = int(imgWidth*(yRange/xRange))
scaleFactor = imgWidth/xRange 

# Start with a 300x300 image

imgSource = pixArray(imgWidth,imgHeight)

def pixToIm(pixel_X,pixel_Y):
    '''
    Convert a pixel's xy coordinate into
    a complex number with decimal coefficients
    '''
    img_X = Decimal(pixel_X/scaleFactor + xMin) # Div by scaleFactor maps to range [0,xRange].
    img_Y = Decimal(pixel_Y/scaleFactor + yMin)
    return Complex(img_X,img_Y)

def evaluate(complexNumber):
    z_n = Complex(0,0)
    count = 0
    for i in range(0,200):
        z_nSquared = z_n.square()
        z_n = Complex(z_nSquared.Re + complexNumber.Re, z_nSquared.Im + complexNumber.Im)
        if z_n.modulus() > Decimal(4):
            return False, count
        count += 1
    # Assume in mandelbrot
    return True, count
            

# Now run main algorithm
for i in range(0,imgWidth):
    for j in range(0,imgHeight):
        complexCoords = pixToIm(i, j)
        result = evaluate(complexCoords)
        if result[0] == True:
            imgSource.setPixel(i, j, 0, 0, 0)
            print "pixel" + str(i) + "," + str(j) + "In mandelbrot!"
        else:
            imgSource.setPixel(i, j, 255, 255, 255)
            #print "pixel" + str(i) + "," + str(j) + "NOT In mandelbrot!"

png.from_array(imgSource.getRaw(), 'RGB').save('test.png')
# def evaluatePixel(xCoord,yCoord):
#     curr_zn_ = 0 # The variable that will be looped through the formula
#     count = 0 # No. of iterations
#     while curr_zn <=4:
#         
# def iterateMandelbrot(zn):
#     
# def squareComplex(re,im):