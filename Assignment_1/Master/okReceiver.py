import selectors
import socket
import types
import sys


sel = selectors.DefaultSelector()

roster = [] #The roster holds the mappers/reducers that haven't checked in yet

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('[OKServer] accepted connection from', addr)
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
            sendBack = takeAttendance(repr(recv_data))
            data.outb += recv_data
        else:
            print('[OKServer] closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if (b'Welcome' != sendBack):
                sent = sock.send(sendBack)  # Should be ready to write
                print("[OKServer] Current absentees on roster : ", roster)
                data.outb = data.outb[sent:]
                killMe = True


def createRoster() : 

    for i in range(0, numberOfMappers):
        roster.append("Mapper" + i)

    for i in range(0, numberOfReducers): 
        roster.append("Reducer" + i)


'''
    Receives notice from Mapper or Reducer and removes from roster
'''
def takeAttendance(s):
    
    theMapOrRed = s[2:len(s)-1]
    roster.pop(theMapOrRed)


    '''

    #If it is a get, return the value given the key or error message
    if theCommand.upper() == "GET":
        #Try to get the key value pair. If not found, return error
        try:
            theKey = command[1][0:(len(command[1])-1)].upper()
            theValue = keyValues[theKey]
            return bytes("The value for key [" + str(theKey) + "] is : " + str(theValue), encoding='utf8')
        except KeyError:
            return bytes("ERROR -- KEY NOT FOUND", encoding='utf8')            

    #If it is a store, store it in the dictionary
    if theCommand.upper() == "STORE":
        keyAndValue = command[1].split("=")
        #print("[Server] The keyAndValue term is : ", keyAndValue)
        #Try to store the given key value pair
        try:           
            keyValues[keyAndValue[0].upper()] = keyAndValue[1][0:len(keyAndValue[1])-1]
            return bytes(("Success at storing : key - "+keyAndValue[0]+", value - "
                          +keyAndValue[1][0:len(keyAndValue[1])-1]), encoding='utf8')
        except IndexError:
            return bytes("Invalid key-value pair... try form: STORE __=__", encoding='utf8')

    killMe = True
    return bytes("Wrong input format, please use: STORE key=value   or    GET key", encoding='utf8') 
    '''

'''
    Getting the parameters and setting up the roster
'''
if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <numberOfMappers> <numberOfReducers>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
numberOfMappers = int(sys.argv[3])
numberOfReducers = int(sys.argv[4])
createRoster()

'''
    Socket set up
'''
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("[OKServer] listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


'''
    We only terminate when everyone on the roster has been checked off
'''
try:
    while len(roster) != 0:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("[OKServer] caught keyboard interrupt, exiting")
finally:
    print("[OKServer] FINALLY")
    sel.close()