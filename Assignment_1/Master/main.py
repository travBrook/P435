import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM
import time


clusterID = 0
startingHost = "127.0.0.1"
startingPort = "65431"


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
    startingHost, startingPort, str(numberOfMappers), str(numberOfReducers)])

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
        Wait 10 seconds for response from everyone
    '''
    status = ok.wait(timeout=10)
    time.sleep(3)
    if status == 0:
        print("READY!")
        return clusterID + 1
    else :   
        print("OUCH!")



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

for i in range(0,numberOfMappers) : 
    
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == (65432+i):
                proc.send_signal(SIGTERM)



'''
    Ready the troops
'''
aCluster = init_Clusters()


'''
    Prompt for user input to get input file/output location, and map/red functions
'''