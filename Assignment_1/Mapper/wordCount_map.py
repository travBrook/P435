import sys
import string

def mapChunk(chunk):
    pass
    for char in string.punctuation:
        #print(char)
        chunk = chunk.replace(char, '')
    theWords = chunk.split(" ")
    words = []
    for word in theWords:
        words.append((word, 1)) 

    return words

chunk = sys.stdin.readline()

mappedChunk = sorted(mapChunk(chunk))

print(mappedChunk)