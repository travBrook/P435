import selectors
import socket
import types
import sys

host = "127.0.0.1"
host2 = "127.0.0.2" 
port = 65431
port2 = 65433

messages = [b"STORE foo=username", b"STORE blah=username2"]

sel = selectors.DefaultSelector()

keyValues = {}

'''
    To run this program:
    >python server.py
    It does NOT do anything with arguments... 
    I could not see a reason for this...
'''

def start_connections(host, port):

    # Add the arguments to the messages to be sent
    for i in range(0, len(sys.argv)):
        if i == 0:
            continue
        else :
            messages.append(bytes(sys.argv[i], encoding='utf8'))

    print("Yippee")
    

    server_addr = (host, port)
    print("[ServerV2] starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connid="ServerV2",
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=list(messages),
        outb=b"",
    )
    sel.register(sock, events, data=data)
    


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('[ServerV2] accepted connection from', addr)
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
            sendBack = addToKeyValue(repr(recv_data))
            data.outb += recv_data
        else:
            print('[ServerV2] closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #Here is where we send the status or value back to the client
            sock.send(data.outb)

            if (b'Welcome' != sendBack):
                sent = sock.send(sendBack)  # Should be ready to write
                print("[ServerV2] Current key values on server: ", keyValues)
                data.outb = data.outb[sent:]


'''
    Takes user request (GET or STORE) and returns appropriate response
'''
def addToKeyValue(s):
    
    #First see if user is storing or getting key-value
    command = s.split(" ")
    theCommand = command[0][2:len(command[0])]

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

    return bytes("Wrong input format, please use: STORE key=value   or    GET key", encoding='utf8') 


def startAndLookForConnections(host, port):
    start_connections(host, int(port),)
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("[ServerV2] caught keyboard interrupt, exiting")
    finally:
        sel.close()


sendReady = False

#Socket set up
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host2, port2))
lsock.listen()
print("[ServerV2] listening on", (host2, port2))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=1)
        if sendReady :
            print("yip")
            startAndLookForConnections(host, port)

        for key, mask in events:
            print("wow")
            if key.data is None:
                accept_wrapper(key.fileobj)
                sendReady = True
            else:
                service_connection(key, mask)

        sendReady = True

except KeyboardInterrupt:
    print("[Server] caught keyboard interrupt, exiting")
finally:
    print("[Server] FINALLY")
    sel.close()