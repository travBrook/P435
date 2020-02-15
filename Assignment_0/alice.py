import sys
import socket
import selectors
import types
import time  

host = "127.0.0.1"
port = 65431

sel = selectors.DefaultSelector()
messages = [b"STORE foo=username", b"STORE blah=username2"]

'''
    To run this program:
    >python alice.py args
    where args has the form of either:
    STORE [key]=[value]
    or
    GET [key]
'''


def start_connections(host, port):

    # Add the arguments to the messages to be sent
    for i in range(0, len(sys.argv)):
        if i == 0:
            continue
        else :
            messages.append(bytes(sys.argv[i], encoding='utf8'))

    server_addr = (host, port)
    print("[Alice] starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connid="Alice",
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
            print("[Alice] received", repr(recv_data), "from the server")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print("[Alice] closing connection to server")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            print("[Alice] these are the messages still to be sent : ", data.messages)
            data.outb = data.messages.pop(0)
        if data.outb:
            print("[Alice] sending", repr(data.outb), "to server")
            sent = sock.send(data.outb)  # Should be ready to write
            time.sleep(1) # This sleep allows the server to receive each message individually
            data.outb = data.outb[sent:]


start_connections(host, int(port))

try:
    while True:
        events = sel.select(timeout=0)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("[Alice] caught keyboard interrupt, exiting")
finally:
    sel.close()
