import sys,socket,selectors
import types #often used to define custom types for callbacks or events in conjunction with I/O operations.

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key,mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # should be ready to read
        data.outb += recv_data
    else:
        print(f"Closing connection to {data.addr}")
        sel.unregister(sock)
        sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            # any received data stored in data.outb is echoed to the client using sock.send(). 
            # The bytes sent are then removed from the send buffer

sel = selectors.DefaultSelector()

host,port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock,selectors.EVENT_READ,data=None)

try:
    while True:
        #sel.select(timeout=None) blocks until there are sockets ready for I/O.
        #It returns a list of tuples, one for each socket (key and mask contained)
        events = sel.select(timeout=None)
        # The key is a SelectorKey named tuple that contains a fileobj attribute. 
        # key.fileobj is the socket object, and mask is an event mask of the operations that are ready.
        for key,mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key,mask)
except KeyboardInterrupt:
    print("Caught keyboard interuppt, exiting!")
finally:
    sel.close()
