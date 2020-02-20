import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
from threading import Thread 
import select

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

        #The last mapper might take a few extra lines....
        if i == numberOfMappers-1:
            for line in lines :
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
        Spawn master dataRelayers for each mapper.  
        give these traders the data, mapper host/port, 
        and the corrsponding reducer host/port
    '''

    relayers = []

    ###We start by distributing the mappers to the different reducers    
    for i in range(0, numberOfMappers):
        mapperHost, mapperPort = rosterDict["Mapper" + str(i)]
        if i >= numberOfReducers : 
            reducerHost, reducerPort = rosterDict["Reducer" + str(i-numberOfReducers)]
        else: 
            reducerHost, reducerPort = rosterDict["Reducer" + str(i)]
        ###Start a relayer 
        relayer = subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/dataRelayer.py',
        mapperHost, mapperPort, reducerHost, reducerPort, mapFn], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        ###Send the chunk to them
        relayer.stdin.write((bytes(chunks[i], encoding='utf8')))
        ###Keep track of the relayers to see if all finished
        relayers.append(relayer)


    #We'll wait 5 seconds to hear back from each relayer
    for relayer in relayers : 
        outs, status = relayer.communicate(timeout=5)
        output = repr(outs)[2:len(repr(outs))-1] 
        output = output.replace('\\r', '')
        output = output.replace('\\n', '')
        if output == "Ready":
            print("READY!")
        else :   
            print("[Master_Main] Relayer(s) to a mapper failed us! Exitting...")




    '''
        JUST SEND TO REDUCER SERVER 
        but when?! perhaps just set a timeout for 45 seconds?
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
