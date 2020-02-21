import sys
import string

def mapChunk(chunk):
    pass
    for char in string.punctuation:
        chunk = chunk.replace(char, '')

    theWords = chunk.split(" ")
    words = []
    for word in theWords:
        if word != '':
            words.append((word.upper(), 1)) 

    return words

chunk = sys.stdin.readline()

mappedChunk = sorted(mapChunk(chunk))

print(mappedChunk)