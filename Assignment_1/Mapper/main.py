import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM


def main() :

    print("Howdy from mapper!" + mapID)
    subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/sender.py', startingHost, startingPort, mapID])


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <id>")
    sys.exit(1)

startingHost = sys.argv[1]
startingPort = sys.argv[2]
mapID = sys.argv[3]

main()