import socket
import threading

clients = [] # track of all connected clients

def handle_client(client_socket,addr):
    clients.append(client_socket)

    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode('utf-8')
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break #essentially closing connection
            print(f'Received from ({addr[0]}:{addr[1]}): {request}')
            response = 'accepted'

            for client in clients:
                if client != client_socket:
                    try:
                        client.send(response.encode('utf-8'))
                    except:
                        clients.remove(client) # Remove the client if connection fails
                else: 
                    response += '*' #add a flag char when sending to original sender
                    client.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server():
    server_ip = '192.168.1.35'
    port = 12345

    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((server_ip,port))
        server.listen()
        print(f'Listening on {server_ip}:{port}')

        while True:
            client_socket, addr = server.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            #start a new thread to handle the client
            thread = threading.Thread(target=handle_client,args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.close()
    
run_server()