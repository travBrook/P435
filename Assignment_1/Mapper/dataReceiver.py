import selectors
import socket
import types
import sys
import subprocess
import comms_pb2


sel = selectors.DefaultSelector()

isMapped = ['blah']

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

    masterMessage = comms_pb2.AMessage()
    masterMessage.ParseFromString(s)
    #print(masterMessage)

    aMapping = subprocess.Popen(['python.exe', 
    'C:/Users/T Baby/Documents/GitHub/P435/Assignment_1/Mapper/wordCount_map.py'], 
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    aMapping.stdin.write(bytes(masterMessage.data, encoding='utf8'))
    outs, errs = aMapping.communicate(timeout=10)
    #print("BBBLAHHHH : " + repr(outs))
    theData = repr(outs)[2:len(repr(outs))-1].replace('\\n', '')
    theData = theData.replace('\\r', '')
    theReducers = masterMessage.others
    protoHelper = []
    for reducer in theReducers:
        protoHelper.append([[reducer.host,reducer.port], reducer.range])

    toBeSent = theData + "vxyxv" + str(protoHelper)
    print(toBeSent)
    isMapped.pop(0)

    return bytes("Thank you, i'll handle this, master", encoding='utf8')

'''
    Getting the parameters and setting up the roster
'''
if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <id>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

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
    while len(isMapped) != 0:
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