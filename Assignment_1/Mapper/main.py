import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time


def main() :

    #print("Howdy from mapper!" + mapID)
    '''
    FOR STARTING REMOTELY
    rpc = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/rpyc_classic.py',
    ("-p "+ str(remoteReceiverPort))])
    '''
    
    rcvr = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/dataReceiver.py', 
    receiverHost, str(receiverPort), mapID], stdout=subprocess.PIPE)

    time.sleep(1)

    if rcvr.poll() is None : 
        sender = subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/sender.py',
        startingHost, startingPort, mapID, receiverHost, str(receiverPort)], stdin=subprocess.PIPE)
        time.sleep(2)
        sender.communicate((bytes("", encoding='utf8')))    
    else :
        print("Mapper" + str(mapID) + "had trouble starting")
        sys.exit(1)

    outs, errs = rcvr.communicate(timeout=45)
    #rcvr.wait()
    
    #print(repr(outs))
    everything = repr(outs)[2:len(repr(outs))-1].replace('\\n', '')
    theGoods = everything.replace('\\r', '').split('vxyxv')
    #print(theGoods)
    #mappedData = eval(theGoods[0][1:len(theGoods[0])-1])
    reducerServer = theGoods[1]
    reducerHost = theGoods[2]


    '''
        Once we have the mappedData, we create senders to send
        this data to the reducer servers
    '''
    sender = subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/sender.py',
        reducerServer, reducerHost, mapID, receiverHost, str(receiverPort)], stdin=subprocess.PIPE)

    sender.communicate(bytes(theGoods[0][1:len(theGoods[0])-1], encoding='utf8'))
    

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