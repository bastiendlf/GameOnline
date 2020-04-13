import socket
import threading
import pickle
from network_constants import SERVER_IP, ADDRESS_SERVER, HEADER, DISCONNECT_MESSAGE, FORMAT, make_header, \
    send_data_pickle, receive_data_pickle
from lobby import Lobby
from ship import Ship


def handle_client(conn: socket, address: tuple):  # old
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


def threaded_client(conn: socket, address: tuple, _lobbyID: int, _clientID: int):
    """
    runs a new thread for each player connected to server

    :param conn: new client's socket object
    :param address: client's address (ip, port)
    :param _lobbyID: lobby id (int)
    :param _clientID: client id (int)
    :return: None
    """
    global connections, lobbies, connections

    current_id = _clientID
    lobby = lobbies[_lobbyID]

    send_data_pickle(conn, (current_id, _lobbyID))
    username = str(receive_data_pickle(conn))

    print(f"[LOG] {str(address[0])} connected, username {username}")

    lobby.add_player(Ship(username))

    connected = True
    while connected:
        if lobby.start:
            pass


    # When user disconnects
    print("[DISCONNECT] Name:", username, ", Client Id:", current_id, "disconnected")
    connections -= 1
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    global _idCount, lobbies, connections

    while True:
        conn, address = server.accept()  # wait for a new client to connect

        lobbyID = (_idCount - 1) // 2
        if _idCount % 2 == 1:  # create a new lobby every 2 players
            lobbies[lobbyID] = Lobby(lobbyID)

        connections += 1

        print(f"[ACTIVE CONNECTIONS] {connections}")
        # thread = threading.Thread(target=handle_client, args=(conn, address))  # Start a new thread for each client

        # Start a new thread for each client
        thread = threading.Thread(target=threaded_client, args=(conn, address, lobbyID, _idCount))
        thread.start()
        _idCount += 1


if __name__ == "__main__":

    connections = 0
    lobbies = {}
    _idCount = 1

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(ADDRESS_SERVER)
        print(f"[STARTING] Server is starting with ip {SERVER_IP}")
        start()
        print("[SERVER] Server offline")

    except socket.error as e:
        print(str(e))
        print("[SERVER_IP] Server could not start")
        quit()
