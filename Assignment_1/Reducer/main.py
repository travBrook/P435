import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
#import rpyc


def main() :

    #print("Howdy from reducer!" + redID)
    '''
    FOR STARTING REMOTELY
    rpc = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/rpyc_classic.py',
    ("-p "+ str(remoteReceiverPort))])
    '''
    

    rcvr = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/dataReceiver.py',
    receiverHost, str(receiverPort), redID, numberOfMappers])

    time.sleep(4)

    if rcvr.poll() is None : 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/sender.py',
        startingHost, startingPort, redID, receiverHost, str(receiverPort)])
    else : 
        print("Reducer" + str(redID) + "had trouble starting")
        sys.exit(1)



if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <id> <numberOfMappers>")
    sys.exit(1)

startingHost = sys.argv[1]
startingPort = sys.argv[2]
redID = sys.argv[3]
numberOfMappers = sys.argv[4]

receiverHost = startingHost[0:len(startingHost)-1]
receiverHost += str(int(redID)+2)
receiverPort = int(startingPort) + int(redID) + 1

#For starting remotely
'''
remoteReceiverHost = startingHost[0:len(startingHost)-1]
remoteReceiverHost += str(int(mapID)+1)
remoteReceiverPort = int(startingPort) - int(mapID) - 50
'''

main()

