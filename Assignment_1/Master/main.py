import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time

clusterID = 0
startingHost = "127.0.0.1"
startingPort = "65431"

rosterDict = {}
numberOfMappers = 0
numberOfReducers = 0

###FOR ME : For path issues, consider local variable (could even be read off of file), then concat

def runMapRed(inputData, mapFn, redFn, outputLoc) : 

    '''
        Retrieve the data and split it up evenly for the 
        amount of mappers. 
        Just going to split by the number of lines for now.
        A bit of a bottleNeck, but less file access needed
    '''
    try:
        pass
        f = open(inputData, "r", encoding="utf8")
        lines = f.readlines()
        f.close()
    except IOError:
        pass
        print("The file doesn't exist friend...")
        sys.exit(1)

    n = len(lines)
    mappersShare = int(n/numberOfMappers)

    chunks = []
    for i in range(0, numberOfMappers):
        pass
        thisChunk = ""
        for j in range(0, mappersShare):
            line = lines.pop(0).replace("\n", " ")
            thisChunk = thisChunk + line
        chunks.append(thisChunk)


    '''
        Spawn the master receiver to receive okays from 
        completed mappers. Master will respond with host/ports 
        of reducers and the function
    '''
    '''
    ok = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/okReceiver.py', 
    startingHost, startingPort, str(numberOfMappers), str(numberOfReducers)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    '''

    '''
        Spawn master dataTraders for each mapper.  
        give these traders the data, mapper host/port, 
        and the corrsponding reducer host/port
    '''
    
    for i in range(0, numberOfMappers):
        mapperHost, mapperPort = rosterDict["Mapper" + str(i)]
        if i >= numberOfReducers : 
            reducerHost, reducerPort = rosterDict["Reducer" + str(i-numberOfReducers)]
        else: 
            reducerHost, reducerPort = rosterDict["Reducer" + str(i)]

        
        relayers = subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/dataRelayer.py',
        mapperHost, mapperPort, "chunks[i]", reducerHost, reducerPort, mapFn], stdin=subprocess.PIPE)

        outs = relayers.communicate(input=bytes(chunks[i], encoding='utf8'),timeout=15)[0]

    '''
        ef
    '''


'''
    Gets the roster from the text file created
    by the initialization given the cluster id.
'''
def initRoster() :
    pass
    f = open("clusters.txt", "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        clusID = int(line[0:2])
        if clusID == clusterID:
            theLine = line[2:len(line)]
            return eval(theLine)
            
'''
    Counts the number of mappers/reducers on the 
    roster.
'''
def countEm():
    pass
    numberOfMappers = 0
    numberOfReducers = 0
    for key in rosterDict.keys():
        #taken from stack exchange https://stackoverflow.com/questions/12851791/removing-numbers-from-string
        mapOrRed = ''.join([i for i in key if not i.isdigit()]) 
        if mapOrRed == "Mapper" :
            numberOfMappers += 1
        if mapOrRed == "Reducer" :
            numberOfReducers += 1
    return (numberOfMappers, numberOfReducers)


'''
    Initilization of vars
'''
if len(sys.argv) != 6:
    print("usage:", sys.argv[0], "<inputFileLoc> <map fn> <red fn> <outputFileLoc> <cluster id>")
    sys.exit(1)

inputFile = sys.argv[1]
mapFn = sys.argv[2]
redFn = sys.argv[3]
outputFile = sys.argv[4]
clusterID = int(sys.argv[5])


'''
    First we get the roster
    Count the amount of mappers/reducers 
'''
rosterDict = initRoster()
numberOfMappers, numberOfReducers = countEm()


'''
    Give it a spin!
'''
runMapRed(inputFile, mapFn, redFn, outputFile)
