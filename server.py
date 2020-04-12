import socket
import threading
import pickle
from network_constants import SERVER_IP, ADDRESS_SERVER, HEADER, DISCONNECT_MESSAGE, FORMAT, make_header
from ship import Ship


def handle_client(conn: socket, address: tuple):
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


def threaded_client(conn: socket, address: tuple, _clientID: int):
    """
    runs a new thread for each player connected to server
    :param conn: new client's socket object
    :param address: client's address (ip, port)
    :param _clientID: client id (int)
    :return: None
    """
    global connections, players

    current_id = _clientID

    conn.send(str.encode(str(current_id)))
    username = conn.recv(16).decode(FORMAT)

    print(f"[LOG] {str(address[0])} connected, username {username}")

    players[current_id] = Ship(username, 0, 0)

    connected = True
    while connected:
        pass


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    global _idCount

    while True:
        conn, address = server.accept()  # wait for a new client to connect

        _idCount += 1
        print(f"[ACTIVE CONNECTIONS] {_idCount}")
        thread = threading.Thread(target=handle_client, args=(conn, address))  # Start a new thread for each client
        thread.start()


if __name__ == "__main__":

    connections = set()
    players = {}
    _idCount = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(ADDRESS_SERVER)
        print(f"[STARTING] Server is starting with ip {SERVER_IP}")
        start()
    except socket.error as e:
        print(str(e))
        print("[SERVER_IP] Server could not start")
        quit()
