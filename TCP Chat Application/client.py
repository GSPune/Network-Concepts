import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = '192.168.1.35' #"127.0.0.1"  #put in the server's IP address
    server_port = 12345 #put in the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            msg = input("Enter message: ")
            client.sendall(msg.encode())

            #recieve message from server
            response = client.recv(1024)
            response = response.decode('utf-8')
            messages = response.split('\n')
            for msg in messages:
                if msg:
                    if not msg.endswith('*'):
                        print(f"Received message: {msg}") # Print the broadcasted message
                else:
                    # if server sends us "closed" in the payload, we break out of
                    # the loop and close our socket
                    if msg.lower() == 'closed*':
                        break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()
            