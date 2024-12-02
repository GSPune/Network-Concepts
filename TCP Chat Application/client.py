import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = '192.168.1.35'  # Server IP address
    server_port = 12345  # Server port number
    
    # Establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            msg = input("Enter message: ")
            if msg.lower() == 'close':
                client.sendall(msg.encode())
                print("Server closed the connection.")
                break
            client.sendall(msg.encode())

            # Receive message from server
            response = client.recv(1024).decode('utf-8')
            # messages = response.split('\n')
            if response:
                print(f"Received message: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()

            