import selectors
import socket
import types
import sys
import subprocess
import comms_pb2
import collections


sel = selectors.DefaultSelector()

isReduced = ['blah']
numberOfMappers = 0
roster = [] #"Mapper0", "Mapper1"
endResult = {}
isReady = False

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    #print('[MDReceiver] accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sendBack = bytes("Welcome", encoding='utf8')
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            sendBack = reduceData(recv_data)
            data.outb += recv_data
        else:
            #print('[MDReceiver] closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if (b'Welcome' != sendBack):
                sent = sock.send(sendBack)  # Should be ready to write
                #print("[MDReceiver] Current absentees on roster : ", roster)
                data.outb = data.outb[sent:]

def reduceData(s):

    mapperMessage = comms_pb2.AMessage()
    mapperMessage.ParseFromString(s)
    global endResult 
    global roster
    global isReady

    print("HAAAAAAAH", mapperMessage.data[0:6])

    #Check if the sender is 
    if mapperMessage.data[0:6] == "SERVER":
        print("NICE")
        if isReady:
            toMasterMessage = comms_pb2.AMessage()
            toMasterMessage.data = str(endResult)
            isReduced.pop(0)
            print("MADE IT!!\n")
            return toMasterMessage.SerializeToString()
        else:
            print("NOT READY!")
            return bytes("NOT READY", encoding='utf8')

    else:

        aReduction = subprocess.Popen(['python.exe', 
            "C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Reducer/inverseIndex_red.py"], 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        aReduction.stdin.write(bytes(mapperMessage.data, encoding='utf8'))
        outs, errs = aReduction.communicate(timeout=10)

        theData = repr(outs)[2:len(repr(outs))-1].replace('\\n', '')
        theData = theData.replace('\\r', '')
        theMapper = mapperMessage.theSender.name
        print(theMapper)
        roster.remove(theMapper)
        if len(roster) == 0:
            isReady = True
        print("MAP MES DATA :\n", mapperMessage.data)
        print("MY REDUCER ID IS : ", redID)
        print("END RESULT:\n",endResult)
        print("TheData:\n",eval(theData))
        ini_dict = [endResult, eval(theData)]
        counter = collections.Counter() 
        for d in ini_dict:  
            counter.update(d) 
        endResult = dict(counter)
        #print(endResult)
        return bytes("Thanks", encoding='utf8')

    print("Where ya goin?")
    return bytes("Thank you, i'll handle this, master", encoding='utf8')

def createRoster() : 
    global roster
    for i in range(0, numberOfMappers):
        roster.append("Mapper" + str(i))

'''
    Getting the parameters and setting up the roster
'''
if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <id> <numberOfMappers>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
redID = sys.argv[3]
numberOfMappers = int(sys.argv[4])
createRoster()

'''
    Socket set up
'''
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
#print("[MDRecvr] listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)



'''
    We only terminate when everyone on the roster has been checked off
'''
try:
    while len(isReduced) != 0: ###CHANGE TO isReduced
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("[MDRecvr] caught keyboard interrupt, exiting")
finally:
    #print("[MDRecvr] FINALLY")
    #print(repr(sys.stdin))
    #print(sys.stdin.readline())
    sel.close()