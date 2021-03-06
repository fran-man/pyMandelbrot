'''
Created on 22 Oct 2013

@author: George
'''

import png
from complex import *
from pixArray import *
from multiprocessing import Process, Queue, process
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

imgWidth = 600
imgHeight = int(imgWidth*(yRange/xRange))
scaleFactor = float(imgWidth/xRange) 

# Start with a 300x300 image

#imgSource = pixArray(imgWidth,imgHeight)
#imgSource2 = pixArray(imgWidth,imgHeight)

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
                    # This point is in the mandelbrot set
                    rowArray.setPixel(i,j-currChnkPos, 0, 0, 0)
                else:
                    pixelColour = 255/((result[1] % 3)+2)
                    rowArray.setPixel(i,j-currChnkPos, pixelColour, pixelColour, 255)
        tmpfile = open("out__CHUNK"+str(currChnk)+".tmp",'wb')
        pickle.dump(rowArray.getRaw(),tmpfile)
        tmpfile.close() #if we don't do this we get weird errors!
                        #when trying to read

def retrieveChunks(chunkCount):
    finalArray = []
    for i in range(0,chunkCount):
        tmpfile = open("out__CHUNK"+str(i)+".tmp","rb")
        chunkArray = pickle.load(tmpfile)
        tmpfile.close()
        
        for row in chunkArray:
            finalArray.append(row)
    return finalArray
                
if __name__ == "__main__":
    print "Final image Size: "+str(imgWidth)+"x"+str(imgHeight)
    
    processes = []
    chunkCount = 0
    
    rowQ = Queue()
    '''list of 16 chunks + 1 potentially'''
    if(imgHeight % 16 == 0):
        for i in range(0,imgHeight/16):
            rowQ.put(i)
        chunkCount = imgHeight/16
    else:
        '''account for the extra smaller chunk'''
        for i in range(0,imgHeight/16 + 1):
            rowQ.put(i)
        chunkCount = imgHeight/16 + 1
    for i in range(0,8):
        rowQ.put("DONE")
    
    for i in range(0,8):
        p = Process(target=processChunk,args=(imgWidth, rowQ, 16,))
        p.daemon = True
        processes.append(p)
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    '''
    Now read back in!
    '''
    imgArrayFinal = retrieveChunks(chunkCount)
    #Save
    png.from_array(imgArrayFinal, 'RGB').save('test.png')
    

#png.from_array(imgSource.getRaw(), 'RGB').save('test.png')
# def evaluatePixel(xCoord,yCoord):
#     curr_zn_ = 0 # The variable that will be looped through the formula
#     count = 0 # No. of iterations
#     while curr_zn <=4:
#         
# def iterateMandelbrot(zn):
#     
# def squareComplex(re,im):