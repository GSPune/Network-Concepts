import socket

# Connect the socket to the server's address and port
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost" # The server's hostname or IP address
PORT = 12345 #Port to connect to, on server

c.connect((HOST,PORT))

try:
    #send data
    message = "Hello, Echo Server"
    print(f"Sending: {message}")
    c.sendall(message.encode())

    #Receive response from server
    response = c.recv(1024)
    print(f"Received: {response.decode()}")

    message = ""
    print(f"Sending: {message}")
    c.sendall(message.encode())
    #Receive response from server
    response = c.recv(1024)
    print(f"Received: {response.decode()}")
finally:
    c.close()