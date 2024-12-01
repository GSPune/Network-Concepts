import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  #put in the server's IP address
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
            print(f'Received echo: {response}')  # Print the broadcasted message
            # if server sends us "closed" in the payload, we break out of
            # the loop and close our socket
            if response.lower() == "closed":
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()
            