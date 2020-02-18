import selectors
import socket
import types
import sys
import comms_pb2


sel = selectors.DefaultSelector()

#roster = [] #The roster holds the mappers/reducers that haven't checked in yet

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
            sendBack = mapData(recv_data)
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

def mapData(s):

    theMapOrRedMessage = comms_pb2.AMessage()
    theMapOrRedMessage.ParseFromString(s)
    print(theMapOrRedMessage)
    return bytes("Thank you, i'll handle this, master", encoding='utf8')

'''
def createRoster() : 

    for i in range(0, numberOfMappers):
        roster.append("Mapper" + str(i))

    for i in range(0, numberOfReducers): 
        roster.append("Reducer" + str(i))
'''

'''
    Receives notice from Mapper or Reducer and removes from roster

def takeAttendance(s):
    
    theMapOrRedMessage = comms_pb2.AMessage()
    theMapOrRedMessage.ParseFromString(s)

    senderName = theMapOrRedMessage.theSender.name
    rcvrHost = theMapOrRedMessage.theFriend.host
    rcvrPort = theMapOrRedMessage.theFriend.port

    print(senderName + " " + rcvrHost + " " + rcvrPort + " ") ### prints to stdout where it is piped to parent

    if senderName is None :
        return bytes("OW!", encoding='utf8')
    roster.remove(senderName)
    return bytes("Thank you, " + senderName, encoding='utf8')
'''

'''
    Getting the parameters and setting up the roster
'''
if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <id> <mapFn>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
#numberOfMappers = int(sys.argv[3])
#numberOfReducers = int(sys.argv[4])
#createRoster()

'''
    Socket set up
'''
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("[MDRecvr] listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


'''
    We only terminate when everyone on the roster has been checked off
'''
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("[MDRecvr] caught keyboard interrupt, exiting")
finally:
    #print("[OKServer] FINALLY")
    #print(repr(sys.stdin))
    #print(sys.stdin.readline())
    sel.close()