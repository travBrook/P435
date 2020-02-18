import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
#import rpyc

#conn = rpyc.classic.connect("localhost")


'''
    Get new clusterID
'''

clusterID = 0
startingHost = "127.0.0.1"
startingPort = "65431"

rosterDict = {}


sel = selectors.DefaultSelector()

notReady = False

def init_Clusters():


    '''
        DO A CHECK THAT EVERYONE IS RESPONDING 
    '''
    
    '''
        Spawn a master receiver  
        This receiver receives messages from Mapper and Reducer
        senders that will signal the mapper and reducer servers 
        are awaiting action.
    '''
    ok = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/okReceiver.py', 
    startingHost, startingPort, str(numberOfMappers), str(numberOfReducers)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    
    #time.sleep(3)
    
    '''
        Spawn the mappers and reducers
        This is the only part that currently doesn't use 
        network based communications -- this is because
        it is easier to test locally. 
    '''    
    for i in range(0, numberOfMappers): 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/main.py', startingHost, startingPort, str(i)])

    for i in range(0, numberOfReducers):
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/main.py', startingHost, startingPort, str(i)])


    '''
        Get mapping of ips and ports (wait 10 seconds until fail)
        We communicate to the master reciever process that we spawned
        above. Its stdout is piped to the communicate() method.
        Once the server is done collecting data from the Mappers/Reducers,
        we are allowed to continue
    '''
    outs = ok.communicate(input=bytes("Hello buddy", encoding='utf8'),timeout=15)[0]
    #Stripping and splitting below ... 
    output = repr(outs)[2:len(repr(outs))-1] 
    output = output.replace('\\r', '')
    output = output.replace('\\n', '')
    output = output[0:len(output)-1]
    newMapReds = output.split(" ")
    #Put the clean data into the dictionary
    while len(newMapReds) != 0:
        name = newMapReds.pop(0)
        ip = newMapReds.pop(0)
        portNum = newMapReds.pop(0)
        rosterDict[name] = (ip, portNum)

    print("The roster is : " + str(rosterDict))

    status = ok.wait(timeout=15)

    #If everything went according to plan, we signal we're ready.
    if status == 0:
        print("READY!")
        return clusterID + 1
    else :   
        print("OUCH!")

'''
    This function writes the roster of mappers and reducers to a local file
'''
def reportRoster():

    f = open("clusters.txt", "+a")    
    clusterString = str(clusterID) + " " + str(rosterDict) + "\n"
    f.write(clusterString)
    f.close()


'''
    This function inializes the roster dictionary
'''
def initRoster():

    for i in range(0,numberOfMappers): 
        pass
        rosterDict["Mapper" + str(i)] = ''

    for i in range(0,numberOfReducers):
        pass
        rosterDict["Reducer" + str(i)] = ''

'''
    Gets cluster id. -- based on the previously highest clusterid.
'''
def getClusterID():
    
    f = open("clusters.txt", "r")
    lines = f.readlines()
    f.close()
    high = 0
    for line in lines:
        clusID = int(line[0:2])
        if clusID > high:
            high = clusID
    
    return high


'''
    Get command line args and assign
'''
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<number of mappers> <number of reducers>")
    sys.exit(1)

numberOfMappers = int(sys.argv[1])
numberOfReducers = int(sys.argv[2])

'''
    FOR LOCAL USE
    Before intitializing, clear ports we want to use...
'''

for i in range(0,numberOfMappers) : 
    
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == (65430-i):
                proc.send_signal(SIGTERM)

for i in range(0,numberOfReducers) : 
    
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == (65432+i):
                proc.send_signal(SIGTERM)



'''
    Ready the troops
'''
initRoster()
init_Clusters()
clusterID = getClusterID()+1

'''
    Write to roster to local file and tell user which cluster to use.
'''
reportRoster()
print("Please use cluster ID : " + str(clusterID))









