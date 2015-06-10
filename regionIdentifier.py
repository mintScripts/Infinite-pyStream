__author__ = 'ryanberg'


import math

def getDistanceBetween(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

bin0 = list()

xPosition = 0
yPosition = 0



file = open('hard-test-case100x100.txt', 'r')

maxX = int(file.read(4).splitlines()[0])

maxY = int(file.read(4).splitlines()[0])

currentValue = -1

for index in xrange(maxX*maxY):

    currentValue = int(file.read(2).splitlines()[0])

    if currentValue is 1:
        bin0.append(list([xPosition, yPosition]))

    xPosition += 1

    if xPosition > maxX:
        yPosition += 1
        xPosition = 0

print(bin0)