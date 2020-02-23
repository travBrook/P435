import sys
import string

def reduceChunk(chunk):
    pass
    theList = eval(chunk)
    #print("THE LIST IS : \n", theList)
    wordMap = {}
    for word in theList:
        if word[0] in wordMap.keys():
            #print(word[0]+ " is in the keys") 
            wordMap[word[0]] = wordMap[word[0]].append(word[1])
        else:
            wordMap[word[0]] = [word[1]]  
    return wordMap

chunk = sys.stdin.readline()

reducedChunk = reduceChunk(chunk)

print(reducedChunk)