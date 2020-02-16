import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM


def main() :

    print("Howdy from reducer!" + redID)
    subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/sender.py', startingHost, startingPort, redID])


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <id>")
    sys.exit(1)

startingHost = sys.argv[1]
startingPort = sys.argv[2]
redID = sys.argv[3]

main()