__author__ = 'Ryan Berg <rberg2@hotmail.com>'

# -Synopsis-
#  This algorithm is designed to find the largest connected region of bits based on the Moore neighborhood rules.
#  The algorithm performs reasonably well, finding the largest region of a 100 by 100 array in less than a tenth of a second.
#  Under heavier load the algorithm is not fully optimized but completes a 1000 by 1000 array in 8.5 seconds.

#  Each bit is placed into a 2D array with a corresponding flag.
#  The flag is set to 1 when the walker has traversed the bit and copied the bit into a new array.

import time

def floodFill(node, nodeX, nodeY):
    if node[0] is not 1:
        return

    fillArray = list()
    fillArray.append(list([nodeX, nodeY]))

    i = 0
    while i < len(fillArray):
        #the bits position in the 2D array
        xPos = fillArray[i][0]
        yPos = fillArray[i][1]

        #mark node as done by changing its bit value
        imageBin[xPos][yPos][0] = 0

        #the try exception is in case the walker goes beyond the bounds of the image
        try:
            #East
            if imageBin[xPos +1][yPos][0] is 1 and imageBin[xPos +1][yPos][1] is 0:

                #append to array for the walker to later traverse
                fillArray.append(list([xPos +1, yPos]))

                #flag the bit as appended to fillArray
                imageBin[xPos +1][yPos][1] = 1
        except:
            pass

        try:
            #Southeast
            if imageBin[xPos +1][yPos +1][0] is 1 and imageBin[xPos +1][yPos +1][1] is 0:
                fillArray.append(list([xPos +1, yPos +1]))
                imageBin[xPos +1][yPos +1][1] = 1
        except:
            pass

        try:
            #South
            if imageBin[xPos][yPos +1][0] == 1 and imageBin[xPos][yPos +1][1] == 0:
                fillArray.append(list([xPos, yPos +1]))
                imageBin[xPos][yPos +1][1] = 1
        except:
            pass

        try:
            #Southwest
            if xPos -1 > -1 and imageBin[xPos -1][yPos +1][0] == 1 and imageBin[xPos -1][yPos +1][1] == 0:
                fillArray.append(list([xPos -1, yPos +1]))
                imageBin[xPos -1][yPos +1][1] = 1
        except:
            pass

        try:
            #West
            if xPos -1 > -1 and imageBin[xPos -1][yPos][0] == 1 and imageBin[xPos -1][yPos][1] == 0:
                fillArray.append(list([xPos -1, yPos]))
                imageBin[xPos -1][yPos][1] = 1
        except:
            pass

        try:
            #Northwest
            if xPos -1 > -1 and yPos -1 > -1 and imageBin[xPos -1][yPos -1][0] is 1 and imageBin[xPos -1][yPos -1][1] is 0:
                fillArray.append(list([xPos -1, yPos -1]))
                imageBin[xPos -1][yPos -1][1] = 1
        except:
            pass

        try:
            #North
            if yPos -1 > -1 and imageBin[xPos][yPos -1][0] is 1 and imageBin[xPos][yPos -1][1] is 0:
                fillArray.append(list([xPos, yPos -1]))
                imageBin[xPos][yPos -1][1] = 1
        except:
            pass

        try:
            #Northeast
            if yPos -1 > -1 and imageBin[xPos +1][yPos -1][0] is 1 and imageBin[xPos +1][yPos -1][1] is 0:
                fillArray.append(list([xPos +1, yPos -1]))
                imageBin[xPos +1][yPos -1][1] = 1
        except:
            pass

        i += 1

    return len(fillArray)
#  End floodFill  #


largestRegion = 0

xPosition = 0
yPosition = 0


file = open(raw_input(), 'r')

startTime = time.time()

maxY = int(file.readline())
maxX = int(file.readline())

imageBin = [[0 for rows in range(maxY)] for columns in range(maxX)]


for index in xrange(maxX*maxY):

    currentValue = file.read(2).strip()

    if currentValue is '':
        currentValue = file.read(2).strip()

    currentValue = int(currentValue)

    #place bit in 2D array with flag set to 0
    imageBin[xPosition][yPosition] = list([currentValue, 0])

    xPosition += 1

    if xPosition > maxX - 1:
        yPosition += 1
        xPosition = 0


for y in xrange(maxY):
    for x in xrange(maxX):
        floodFillRegionSize = floodFill(imageBin[x][y], x, y)
        if floodFillRegionSize > largestRegion:
            largestRegion = floodFillRegionSize

print largestRegion
print time.time() - startTime, "seconds"