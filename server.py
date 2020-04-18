import socket
import threading

import numpy as np

from game_data import GridCellType
from lobby import Lobby
from network_constants import SERVER_IP, ADDRESS_SERVER, send_data_pickle, receive_data_pickle, MessageType, \
    MAX_PLAYERS_LOBBY


def find_lobby(client_id: int, username: str):
    """
    Finds a lobby with a free place and create a new lobby if necessary
    :param client_id: int
    :param username: str
    :return: lobby in which player will play
    """

    global lobbies
    lobbyFound = False
    new_lobby = set()

    for lobby in lobbies:
        if not lobby.is_full():
            lobby.add_player(player_id=client_id, username=username)
            lobbyFound = True
            new_lobby = lobby
            break

    if not lobbyFound:
        new_id_lobby = len(lobbies)
        print(f"[LOBBY] Creating new lobby with id {new_id_lobby}.")
        new_lobby = Lobby(new_id_lobby, MAX_PLAYERS_LOBBY)
        new_lobby.add_player(client_id, username)
        lobbies.append(new_lobby)

    return new_lobby


def get_opponent(my_username: str, lobby: Lobby):
    """
    Get opponent info (id and username)
    :param my_username: str my username
    :param lobby: my lobby
    :return: tuple (opponent id :int, opponent username: str)
    """
    if lobby.all_players[0][1] == my_username:
        return lobby.all_players[1]
    else:
        return lobby.all_players[0]


def check_attack_result(my_guessed: np.ndarray, opponent_grid: np.ndarray):
    """
    Check result of player's attack on opponent
    :param my_guessed: numpy array
    :param opponent_grid: numpy array
    :return: touched :boolean, my_guessed : numpy, opponent_grid : numpy
    """
    touched = False

    for i in range(my_guessed.shape[0]):
        for j in range(my_guessed.shape[1]):
            if my_guessed[i][j] == GridCellType.guess:
                if opponent_grid[i][j] == GridCellType.boat:
                    touched = True
                    my_guessed[i][j] = GridCellType.touched
                    opponent_grid[i][j] = GridCellType.touched
                    return touched, my_guessed, opponent_grid
                break
    return touched, my_guessed, opponent_grid


def threaded_client(conn: socket, address: tuple, _client_id: int):
    """
    runs a new thread for each player connected to server

    :param conn: new client's socket object
    :param address: client's address (ip, port)
    :param _client_id: client id (int)
    :return: None
    """

    global connections, lobbies
    current_id = _client_id
    connected = True

    username = str(receive_data_pickle(conn)[1])
    print(f"[SERVER] {str(address[0])} connected, username {username}.")
    lobby = find_lobby(current_id, username)
    lobbyID = lobby.lobbyID

    opponent = tuple()

    for lobby in lobbies:
        print(f"[SERVER] Lobby {lobby.lobbyID} active, players connected : {str(lobby.all_players)}.")

    send_data_pickle(conn, (MessageType.REPLY_ACK, (current_id, lobbyID)))

    while connected:
        data = receive_data_pickle(conn)

        if data[0] == MessageType.SEND_MY_GRID:
            print(f"[LOBBY {lobbyID}] {username} sends its grid.")
            lobby.add_grid_player(current_id, data[1])
            send_data_pickle(conn, (MessageType.REPLY_ACK, "[SERVER] Grid received."))

            # Wait for other player
            send_start = False
            while not send_start:
                if lobby.start:
                    send_start = True
            send_data_pickle(conn, (MessageType.START_PLAY, ""))
            opponent = get_opponent(username, lobby)

        if data[0] == MessageType.SEND_MY_GUESSED:
            guessed = data[1]
            print(f"[LOBBY {lobbyID}] {username} sends its guessed grid.")
            touched, guessed, lobby.all_grids[str(opponent[0])] = check_attack_result(guessed,
                                                                                      lobby.all_grids[str(opponent[0])])
            if not touched:
                lobby.change_turn()
            send_data_pickle(conn, (MessageType.SEND_MY_GUESSED, guessed))
            lobby.end_turn = True

        if data[0] == MessageType.UPDATED_GRID:
            while True:
                if lobby.end_turn:  # wait for opponent to play
                    break
            lobby.end_turn = False
            send_data_pickle(conn, (MessageType.UPDATED_GRID, lobby.all_grids[str(current_id)]))

        if data[0] == MessageType.WHOSE_TURN:
            send_data_pickle(conn, (MessageType.WHOSE_TURN, lobby.current_turn))

        if data[0] == MessageType.DISCONNECT:
            connected = False
            lobby.remove_player(current_id, username)

        if lobby.end_game():
            print("End Game")
            send_data_pickle(conn, (MessageType.DISCONNECT, ""))
            lobby.remove_player(current_id, username)
            break

    # When user disconnects
    print(f"[DISCONNECT] Name:{username} ({str(address[0])}), Client Id: {current_id} -> disconnected.")
    connections -= 1
    conn.close()


def start():
    server.listen()
    print(f"[SERVER] Server is now listening.")
    global _idCount, lobbies, connections

    while True:
        conn, address = server.accept()  # wait for a new client to connect

        connections += 1

        print(f"[SERVER] Active connections : {connections}.")

        # Start a new thread for each client
        thread = threading.Thread(target=threaded_client, args=(conn, address, _idCount))
        thread.start()
        _idCount += 1


if __name__ == "__main__":

    connections = 0
    lobbies = []
    _idCount = 1

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(ADDRESS_SERVER)
        print(f"[SERVER] Server is starting with ip {SERVER_IP}.")
        start()
        print("[SERVER] Server offline.")

    except socket.error as e:
        print(str(e))
        print("[SERVER_IP] Server could not start.")
        quit()
