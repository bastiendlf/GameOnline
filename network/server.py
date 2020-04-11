import socket
import threading
import pickle
from network.network_constants import SERVER, ADDRESS_SERVER, HEADER, DISCONNECT_MESSAGE, FORMAT, make_header

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDRESS_SERVER)
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()


def handle_client(conn, address):
    conn.send(pickle.dumps(f"Welcome to server {ADDRESS_SERVER[0]}"))

    client_pc_name = socket.gethostbyaddr(str(address[0]))[0]
    print(f"[NEW CONNECTION] {str(address[0])} : {client_pc_name} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # get the length of the incoming msg
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)  # adjust the buffer size to the messages's length
            message_object = pickle.loads(msg)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.close()

            print(f"[{client_pc_name} ({str(address[0])})] -> {message_object}")

            answer = pickle.dumps("Message received")
            conn.send(make_header(answer))
            conn.send(answer)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, address = server.accept()  # wait for a new client to connect
        thread = threading.Thread(target=handle_client, args=(conn, address))  # Start a new thread for each client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print(f"[STARTING] Server is starting with ip {SERVER}")
start()
