import socket
import threading

from lobby import Lobby
from network_constants import SERVER_IP, ADDRESS_SERVER, DISCONNECT_MESSAGE, send_data_pickle, receive_data_pickle


def threaded_client(conn: socket, address: tuple, _lobbyID: int, _clientID: int):
    """
    runs a new thread for each player connected to server

    :param conn: new client's socket object
    :param address: client's address (ip, port)
    :param _lobbyID: lobby id (int)
    :param _clientID: client id (int)
    :return: None
    """
    global connections, lobbies

    current_id = _clientID
    lobby = lobbies[_lobbyID]

    username = str(receive_data_pickle(conn))
    send_data_pickle(conn, (current_id, _lobbyID))

    print(f"[LOG] {str(address[0])} connected, username {username}")

    lobby.add_player(current_id, username)

    print(f"[LOBBY {_lobbyID}] Starting game")

    while True:
        data = receive_data_pickle(conn)

        print(f"[{username} ({str(address[0])})] -> {str(data)}")
        print(f"[SERVER] Reply to {username} ({str(address[0])}) -> Message received : {str(data)}")

        send_data_pickle(conn, f"Message received : {str(data)}")

        if data == DISCONNECT_MESSAGE:
            break

    # When user disconnects
    print(f"[DISCONNECT] Name:{username} ({str(address[0])}), Client Id: {current_id} -> disconnected")
    connections -= 1
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is now listening")
    global _idCount, lobbies, connections

    while True:
        conn, address = server.accept()  # wait for a new client to connect

        lobbyID = (_idCount - 1) // 2
        if _idCount % 2 == 1:  # create a new lobby every 2 players
            lobbies[lobbyID] = Lobby(lobbyID)
            print(f"[LOBBY] Creating a new lobby with id : {lobbyID}")

        connections += 1

        print(f"[ACTIVE CONNECTIONS] {connections}")

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
