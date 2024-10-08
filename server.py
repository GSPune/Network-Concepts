# echo-server.py

import socket

HOST = "localhost"
PORT = 12345 #Port to listen to 

# Create a TCP Connection
# AF_INET is the Internet address family for IPv4 & SOCK_STREAM is the socket type for TCP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))

# Listen for incoming connections
s.listen(1)
print(f"Server listening on port {PORT}")

while True:
    #Wait for a connection
    client_socket,addr = s.accept()
    print(f"Connected by {addr}")
    try:
        data = client_socket.recv(1024) #reads up to 1K bytes
        if not data:
            break
        print(f"Received: {data.decode()}")
        client_socket.sendall(data)
        
    finally:
        client_socket.close()


