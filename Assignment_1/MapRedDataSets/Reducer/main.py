import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time
import rpyc


def main() :

    #print("Howdy from reducer!" + redID)

    rcvr = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/dataReceiver.py', receiverHost, str(receiverPort), redID])

    time.sleep(4)

    if rcvr.poll() is None : 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/sender.py', startingHost, startingPort, redID])
    else : sys.exit(1)


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <id>")
    sys.exit(1)

startingHost = sys.argv[1]
startingPort = sys.argv[2]
redID = sys.argv[3]

receiverHost = startingHost[0:len(startingHost)-1]
receiverHost += str(int(redID)+2)
receiverPort = int(startingPort) + int(redID) + 1

main()

conn = rpyc.classic.connect("localhost")
conn.execute("print('Hello from Tutorialspoint')")