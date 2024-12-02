import socket
import threading
import signal,sys

clients = []  # Track all connected clients
server = None  # Declare the server as a global variable
lock = threading.Lock()  # Lock for thread synchronization

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if request.lower() == "close":
                # client_socket.send("closed".encode("utf-8"))
                break

            print(f'Received from ({addr[0]}:{addr[1]}): {request}')

            # Broadcast message to other clients
            with lock:  # Ensure thread-safe access to the clients list
                for client in clients:
                    if client != client_socket:
                        try:
                            client.send((request + '\n').encode('utf-8'))
                        except:
                            clients.remove(client)  # Remove faulty clients safely

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        with lock:  # Ensure client removal is thread-safe
            clients.remove(client_socket)
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def signal_handler(sig, frame):
    print("\nShutting down server...")
    for client in clients:
        client.close()
    if server:
        server.close()
    sys.exit(0)

def run_server():
    global server
    server_ip = '0.0.0.0'  # Bind to all network interfaces
    port = 12345

    signal.signal(signal.SIGINT, signal_handler)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f'Listening on {server_ip}:{port}')

        while True:
            client_socket, addr = server.accept()
            print(f'Accepted connection from {addr[0]}:{addr[1]}')
            with lock:
                clients.append(client_socket)  # Append client safely
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.close()

run_server()
