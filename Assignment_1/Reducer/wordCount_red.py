import sys
import string

def reduceChunk(chunk):
    pass
    theList = eval(chunk)
    wordMap = {}
    for word in theList:
        if word in wordMap.keys():
            wordMap[word] = 1
        else:
            wordMap[word] =+ 1  
    return wordMap

chunk = sys.stdin.readline()

reducedChunk = reduceChunk(chunk)

print(reducedChunk)