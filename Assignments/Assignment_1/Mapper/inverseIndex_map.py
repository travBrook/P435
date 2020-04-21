import sys
import string

def mapChunk(chunk):
    pass
    
    theLines = chunk.split("\\n")

    for line in theLines:
        for char in string.punctuation+'\n':
            if char == '\n':
                chunk = chunk.replace(char, ' ')
            else:
                chunk = chunk.replace(char, '')
    words = []
    #i is the line , j is the pos in the line
    for i in range(0, len(theLines)):
        line = theLines[i].split(" ")
        for j in range(0, len(line)):
            if line[j] != '':
                words.append((line[j], (i, j)))

    return words

chunk = sys.stdin.readline()

mappedChunk = sorted(mapChunk(chunk))

print(mappedChunk)