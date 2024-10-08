# echo-server.py

import socket

HOST = "localhost"
PORT = 12345 #Port to listen to 

# Create a TCP Connection
# AF_INET is the Internet address family for IPv4 & SOCK_STREAM is the socket type for TCP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen() # Listen for incoming connections

print(f"Server listening on port {PORT}")
print(f"**Shut down server with message 'Close'.**")

#Wait for a connection
client_socket,addr = s.accept()
print(f"Connected by {addr}")

while True:
    try:
        data = client_socket.recv(1024) #reads up to 1K bytes
        decoded = data.decode()
        if not data or decoded == 'Close':
            break
        print(f"Received: {decoded}")
        client_socket.sendall(data)
    except socket.error as e:
        print(f"Error: {e}")  
        break
print(f"Closing the connection...")
s.close()


