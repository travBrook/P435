import sys
import socket
import selectors
import types
import time
import comms_pb2

sel = selectors.DefaultSelector()

'''
    Call this to give a mapper its data and give the mapper
    its corresponding reducer as well as the map fn
'''

def start_connections(host, port):

    server_addr = (host, port)
    #print("[Mapper] starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connid="dataRelayer",
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=list(messages),
        outb=b"",
    )
    sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print("[dataRelayer] received", repr(recv_data), "from the server")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            #print("[Mapper] closing connection to server")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            #print("[Mapper] these are the messages still to be sent : ", data.messages)
            data.outb = data.messages.pop(0)
        if data.outb:
            #print("[Mapper] sending", repr(data.outb), "to server")
            sent = sock.send(data.outb)  # Should be ready to write
            time.sleep(1)   # This sleep allows the server to receive each message individually
            data.outb = data.outb[sent:]



if len(sys.argv) != 6:
    print("usage:", sys.argv[0], "<mapperHost> <mapperPort> <reducerHost> <reducerPort> <mapFn>")
    sys.exit(1)

host = sys.argv[1]
port = sys.argv[2]
#mapID = sys.argv[3]

thisMessage = comms_pb2.AMessage()

#thisMessage.theSender.name = "Mapper" + mapID
#thisMessage.theSender.host = port
#thisMessage.theSender.port = host

#print(sys.stdin.readline())
thisMessage.data = sys.stdin.readline()
thisMessage.theFriend.name = "RDRcvr"
thisMessage.theFriend.host = sys.argv[3]
thisMessage.theFriend.port = sys.argv[4]
thisMessage.functionFileName = sys.argv[5]

finalMessage = thisMessage.SerializeToString()
messages = [finalMessage]

start_connections(host, int(port))

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
    print("[dataRelayer] caught keyboard interrupt, exiting")
finally:
    sel.close()