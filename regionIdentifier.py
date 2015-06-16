__author__ = 'Ryan Berg <rberg2@hotmail.com>'

# Usage:
#
# The program finds the largest region of adjacent bits. Takes any file as an argument.
# Optionally specify the number of columns per row.
# Users can expect it to take 10 seconds per megabyte.

from collections import deque
import thread
import time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("fileUrl", help="set the file url")
parser.add_argument("--columns", help="set the number of columns per row [defaults to 128 bits]", type=int)
args = parser.parse_args()

END_OF_READSTREAM = -1
END_OF_ROW = -2

NO_MATCHING_REGION = -3
NO_POINTER = -4

PREVIOUS_ROW = 0
CURRENT_ROW = 1

WORD_LENGTH = 128
if args.columns:
    WORD_LENGTH = args.columns

#Northwest, North, Northeast
directionLookupTable = list([-1, 0, 1])

def bitProcessor(bitLocation, previousRow, currentRow):
    bitRegion = NO_MATCHING_REGION
    pointer = NO_POINTER
    for direction in directionLookupTable:
        if bitLocation + direction in previousRow:
            if bitRegion == NO_MATCHING_REGION:
                bitRegion = previousRow[bitLocation + direction]
            elif bitRegion != previousRow[bitLocation + direction]:
                pointer = previousRow[bitLocation + direction]
    if bitLocation - 1 in currentRow:
        if bitRegion == NO_MATCHING_REGION:
            bitRegion = currentRow[bitLocation - 1]
        elif bitRegion != currentRow[bitLocation - 1]:
            pointer = currentRow[bitLocation - 1]
    return {'bitRegion': bitRegion, 'pointer': pointer}

def consumer(readStream):
    q = deque([{-2: 0}, {-2: 0}])
    counter = list([0])

    while True:
        if readStream:
            bitLocation = readStream.popleft()
            if bitLocation == END_OF_READSTREAM:
                break
            if bitLocation != END_OF_ROW:
                bitData = bitProcessor(bitLocation, q[PREVIOUS_ROW], q[CURRENT_ROW])
                # print 'bd', bitData
                if bitData['bitRegion'] == NO_MATCHING_REGION:
                    bitData['bitRegion'] = len(counter)

                if bitData['bitRegion'] < len(counter):
                    # print 'counter', counter
                    if counter[bitData['bitRegion']] > -1:
                        counter[bitData['bitRegion']] += 1
                    else:
                        counter[counter[bitData['bitRegion']] * -1] += 1
                else:
                    counter.append(1)

                if bitData['pointer'] != NO_POINTER and counter[bitData['pointer']] > 0 and counter[bitData['bitRegion']] > 0:
                    counter[bitData['bitRegion']] += counter[bitData['pointer']]
                    counter[bitData['pointer']] = bitData['bitRegion'] * -1
                q[CURRENT_ROW][bitLocation] = bitData['bitRegion']
            else:
                q.popleft()
                q.append({-2: 0})

    # print counter
    return max(counter)

def producer(idNumber, readStream):

    inputFile = open(args.fileUrl, 'rb')

    i = 0
    while True:
        bit = inputFile.read(1)
        if bit == '':
            readStream.append(END_OF_READSTREAM)
            break
        try:
            bit = int(bit.strip())
            if bit == 1 or bit == 0:
                if bit == 1:
                    readStream.append(i)
                i += 1
            if i == WORD_LENGTH:
                i = 0
                readStream.append(END_OF_ROW)
        except ValueError:
            pass
    return

if __name__ == '__main__':

    # infinite stream
    readStream = deque()

    startTime = time.time()

    thread.start_new_thread(producer, (1, readStream))
    print 'crunching data...'
    maxCount = (consumer(readStream))
    print 'Largest Region:', maxCount, 'Running Time:', round(time.time() - startTime, 2), 'seconds'