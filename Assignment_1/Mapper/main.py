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
    receiverHost, str(receiverPort), mapID])

    time.sleep(4)

    if rcvr.poll() is None : 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/sender.py',
        startingHost, startingPort, mapID, receiverHost, str(receiverPort)])
    else :
        print("Mapper" + str(mapID) + "had trouble starting")
        sys.exit(1)


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