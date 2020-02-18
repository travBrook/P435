import sys


def mapChunk(chunk):
    pass
    theWords = chunk.split(" ")
    words = []
    for word in theWords:
        words.append((word, 1)) 

    return words

if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<chunk>(str)")
    sys.exit(1)

chunk = sys.argv[2]

mappedChunk = sort(mapChunk(chunk))

print(mappedChunk)