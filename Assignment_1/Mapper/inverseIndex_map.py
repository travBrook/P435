import sys
import string

def mapChunk(chunk):
    pass
    
    theLines = chunk.split("\n")

    for line in theLines:
        for char in string.punctuation:
            line = line.replace(char, '')

    words = []
    #i is the line , j is the pos in the line
    for i in range(0, len(theLines)):
        line = theLines[i].split(" ")
        for j in (0, len(line)):
            if word != '':
                words.append((word, i, j))

    return words

chunk = sys.stdin.readline()

mappedChunk = sorted(mapChunk(chunk))

print(mappedChunk)