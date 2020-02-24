import sys
import string

def mapChunk(chunk):
    pass

    for char in (string.punctuation+'\n'):
        if char == '\n':
            chunk = chunk.replace(char, ' ')
        else:
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