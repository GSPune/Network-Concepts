import socket

# Connect the socket to the server's address and port
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost" # The server's hostname or IP address
PORT = 12345 #Port to connect to, on server

c.connect((HOST,PORT))

while True:
        #send data
        message = input("Enter your message for the server: ")
        print(f"Sending: {message}")
        if c.sendall(message.encode()):
            print("Huh??")
        if message == 'Close': 
              break
        #Receive response from server
        response = c.recv(1024)
        print(f"Received: {response.decode()}")
print(f"Closing the connection...")
c.close()