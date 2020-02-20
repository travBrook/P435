import selectors
import socket
import types
import sys

host = "127.0.0.1"
port = 65431

sel = selectors.DefaultSelector()

keyValues = {}


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('[Server] accepted connection from', addr)
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
            print('[Server] closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #Here is where we send the status or value back to the client
            if (b'Welcome' != sendBack):
                sent = sock.send(sendBack)  # Should be ready to write
                print("[Server] Current key values on server: ", keyValues)
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

#Socket set up
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("[Server] listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("[Server] caught keyboard interrupt, exiting")
finally:
    print("[Server] FINALLY")
    sel.close()