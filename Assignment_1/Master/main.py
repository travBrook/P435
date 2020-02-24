import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
from threading import Thread 
import select
import collections
import os

path = os.getcwd()

clusterID = 0
startingHost = "127.0.0.1"
startingPort = "65431"

rosterDict = {}
numberOfMappers = 0
numberOfReducers = 0

###FOR ME : For path issues, consider local variable (could even be read off of file), then concat

def runMapRed(inputData, mapFn, redFn, outputLoc) : 
    global path
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
        Spawn master dataRelayers for each mapper.  
        give these traders the data, mapper host/port, 
        and the corrsponding reducer host/port
    '''

    ###This first part outfits the reducers with their information to give to the mappers
    relayers = []
    reducers = []
    ranges = int(25/numberOfReducers)
    prev = 0
    for i in range(0, numberOfReducers):
        pass
        if i == numberOfReducers-1:
            reducerInfo = rosterDict["Reducer" + str(i)]
            reducer = list(reducerInfo[0:len(reducerInfo)])
            reducer.append((chr(65 + prev+1), chr(65+25)))
        else:        
            reducerInfo = rosterDict["Reducer" + str(i)]
            reducer = list(reducerInfo[0:len(reducerInfo)])
            reducer.append((chr(65 + prev), chr(65 + prev+ranges)))

        prev += ranges
        reducers.append(reducer)

    print("[Master] sending data to mappers...")
    ###We start by distributing the mappers to the different reducers    
    for i in range(0, numberOfMappers):
        mapperHost, mapperPort = rosterDict["Mapper" + str(i)]
        ###Start a relayer 
        relayer = subprocess.Popen(['python.exe', 
        path+'/Master/dataRelayer.py',
        mapperHost, mapperPort, str(reducers), mapFn + " " + redFn],  
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
        if output != "Delivered":
            print("[Master] Relayer(s) to a mapper failed us! Exitting...")
        
            
    print("[Master] Relayers have delivered. Contacting Reducers in 4 seconds")


    '''
        Now we try to relay data back from the 
        reducer dataReceivers to compile the final result
    '''
    time.sleep(4)
    ###FIRST spawn relayers
    relayers2 = []
    numRelayers = len(relayers)
    for i in range(0, numberOfReducers):
        pass
        reducerHost, reducerPort = rosterDict["Reducer" + str(i)]
        relayer = subprocess.Popen(['python.exe', 
        path+'/Master/dataRelayer.py',
        reducerHost, reducerPort, str(reducers), mapFn], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        relayer.stdin.write((bytes("SERVER " + str(numberOfMappers), encoding='utf8')))
        relayers2.append(relayer)
        numRelayers =- 1

    ###THEN talk to them to get their outputs
    finalOutput = {}
    for relayer in relayers2 : 
        outs, status = relayer.communicate(timeout=10)
        output = repr(outs)[2:len(repr(outs))-1] 
        output = output.replace('\\r', '')
        output = output.replace('\\n', '')
        ini_dict = [finalOutput, eval(output)]
        counter = collections.Counter() 
        for d in ini_dict:  
            counter.update(d) 
        finalOutput = dict(counter)
    
    #print(str(finalOutput))

    outputData(str(finalOutput))


'''
    Writes the finalOutput to a file
'''

def outputData(finalOutput):

    f = open(os.path.join(path, outputFile), "+a")    
    f.write(finalOutput)
    f.close()

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
        mapOrRed = ''.join([i for i in key if not i.isdigit()]) #<----
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

inputFile = os.path.join(path, "MapRedDataSets", sys.argv[1]) 
mapFn = sys.argv[2]
redFn = sys.argv[3]
outputFile = os.path.join(path, sys.argv[4])
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
