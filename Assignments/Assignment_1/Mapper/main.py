import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
import os
path = os.getcwd()


def main() :

    #print("Howdy from mapper!" + mapID)
    '''
    FOR STARTING REMOTELY (unfinished)
    rpc = subprocess.Popen(['python.exe', 
    path+'/Mapper/rpyc_classic.py',
    ("-p "+ str(remoteReceiverPort))])
    '''

    '''
        Spawn the mappers receiver.
        Then send back to the master okreceiver
        if the process is running 
    ''' 
    
    rcvr = subprocess.Popen(['python.exe', 
    path+'/Mapper/dataReceiver.py', 
    receiverHost, str(receiverPort), mapID], stdout=subprocess.PIPE)

    time.sleep(1)

    if rcvr.poll() is None : 
        sender = subprocess.Popen(['python.exe', 
        path+'/Mapper/sender.py',
        startingHost, startingPort, mapID, receiverHost, str(receiverPort), "placeholder"], stdin=subprocess.PIPE)
        time.sleep(2)
        sender.communicate((bytes("", encoding='utf8')))    
    else :
        print("Mapper" + str(mapID) + "had trouble starting")
        sys.exit(1)

    print("[Mapper " + mapID + "] awaiting data...")

    ###Get the data from the mapper receiver to send to reducers
    outs, errs = rcvr.communicate(timeout=40)
    #rcvr.wait()
    
    everything = repr(outs)[2:len(repr(outs))-1].replace('\\n', '')
    theGoods = everything.replace('\\r', '').split('vxyxv')
    theData = eval(theGoods[0])
    reducers = eval(theGoods[1])
    
    print("[Mapper "+ mapID + "] has finished its task... sending to reducers")

    '''
        Once we have the mappedData, we create senders to send
        this data to the reducer servers
    '''
    n = len(theData)
    for reducer in reducers:
        theReducersJob = []
        reducerStartRange = reducer[1][1]
        reducerEndRange = reducer[1][4]
        for i in range(0, n):
            startOfWord = ord(theData[i][0][0:1])
            if startOfWord <= ord(reducerEndRange) and startOfWord >= ord(reducerStartRange): 
                theReducersJob.append(theData[i])
        reducerHost = reducer[0][0]
        reducerPort = reducer[0][1]
        reducerFn = reducer[0][2]
        sender = subprocess.Popen(['python.exe', 
            path+'/Mapper/sender.py',
            reducerHost, reducerPort, mapID, reducerStartRange, reducerEndRange, reducerFn], stdin=subprocess.PIPE)

        sender.communicate(bytes(str(theReducersJob), encoding='utf8'))

    print("[Mapper " + mapID + "] has sent data to reducers")
    

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <id>")
    sys.exit(1)


startingHost = sys.argv[1]
startingPort = sys.argv[2]
mapID = sys.argv[3]


receiverHost = startingHost[0:len(startingHost)-1]
receiverHost += str(int(mapID)+10)
receiverPort = int(startingPort) - int(mapID) - 1

remoteReceiverHost = startingHost[0:len(startingHost)-1]
remoteReceiverHost += str(int(mapID)+1)
remoteReceiverPort = int(startingPort) - int(mapID) - 50

main()