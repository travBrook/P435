import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
#import rpyc

#conn = rpyc.classic.connect("localhost")


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
        Spawn the master receiver  
    '''
    ok = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/okReceiver.py', 
    startingHost, startingPort, str(numberOfMappers), str(numberOfReducers)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    time.sleep(3)

    #subprocess.Popen(['echo' , '%cd%'], cwd='../', shell=True)

    
    '''
        Spawn the mappers and reducers
    '''    
    for i in range(0, numberOfMappers): 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/main.py', startingHost, startingPort, str(i)])

    for i in range(0, numberOfReducers):
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/main.py', startingHost, startingPort, str(i)])


    '''
        Get mapping of ips and ports (wait 10 seconds until fail)
    '''
    outs = ok.communicate(input=bytes("Hewoah", encoding='utf8'),timeout=10)[0]
    output = repr(outs)[2:len(repr(outs))-1]
    output = output.replace('\\r', '')
    output = output.replace('\\n', '')
    output = output[0:len(output)-1]


    newMapReds = output.split(" ")

    while len(newMapReds) != 0:
        name = newMapReds.pop(0)
        ip = newMapReds.pop(0)
        portNum = newMapReds.pop(0)
        rosterDict[name] = (ip, portNum)

    print("The roster is : " + str(rosterDict))


    status = ok.wait(timeout=10)



    #Sleep not necessary, but keeps output clean
    #time.sleep(3)

    if status == 0:
        print("READY!")
        return clusterID + 1
    else :   
        print("OUCH!")


def runMapRed(inputData, mapFn, redFn, outputLoc) : 

    print("Howdy doody")

def initRoster():

    for i in range(0,numberOfMappers): 
        pass
        rosterDict["Mapper" + str(i)] = ''

    for i in range(0,numberOfReducers):
        pass
        rosterDict["Reducer" + str(i)] = ''

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
aCluster = init_Clusters()


'''
    Prompt for user input to get input file/output location, and map/red functions
'''

