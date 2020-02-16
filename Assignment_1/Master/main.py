import subprocess
import sys
import selectors
from psutil import process_iter
from signal import SIGTERM


clusterID = 0
startingHost = "127.0.0.1"
startingPort = "65431"


sel = selectors.DefaultSelector()

notReady = False

def init_Clusters():

    '''
    Start master server
    Start mappers, reducers, spawn Master OKServers

    '''

    ok = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Master/okReceiver.py', 
    startingHost, startingPort, numberOfMappers, numberOfReducers])

    #subprocess.Popen(['echo' , '%cd%'], cwd='../', shell=True)
    
    
    
    for i in range(0, numberOfMappers): 
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/main.py', startingHost, startingPort])

    for i in range(0, numberOfReducers):
        subprocess.Popen(['python.exe', 
        'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/main.py', startingHost, startingPort])
    
    #while notReady : 
    #    pass

    status = ok.wait(timeout=10)
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
    Before intitializing, clear ports we want to use...
'''
'''
for proc in process_iter():
    for conns in proc.connections(kind='inet'):
        if conns.laddr.port == 65431:
            proc.send_signal(SIGTERM)
'''


'''
for proc in process_iter():
    for conns in proc.connections(kind='inet'):
        if conns.laddr.port == 65433:
            proc.send_signal(SIGTERM)
'''

init_Clusters()