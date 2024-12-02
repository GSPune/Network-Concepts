import socket
import threading

clients = [] # track of all connected clients

def handle_client(client_socket,addr):

    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode('utf-8')
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break #essentially closing connection
            print(f'Received from ({addr[0]}:{addr[1]}): {request}')
            # response = 'accepted'

            for client in clients:
                if client != client_socket:
                    try:
                        client.send((request+'\n').encode('utf-8'))
                    except:
                        clients.remove(client) # Remove the client if connection fails
                else: 
                    request += '*\n' #add a flag char when sending to original sender
                    client_socket.send(request.encode('utf-8'))
            request = ''

    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server():
    #server_ip = '192.168.1.35'
    server_ip = '0.0.0.0'  # Bind to all network interfaces
    port = 12345

    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((server_ip,port))
        server.listen()
        print(f'Listening on {server_ip}:{port}')

        while True:
            client_socket, addr = server.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            clients.append(client_socket)
            #start a new thread to handle the client
            thread = threading.Thread(target=handle_client,args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.close()
    
run_server()