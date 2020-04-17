import numpy as np

from game_data import GRID_SIZE, GridCellType
from network_constants import LobbyStatus


class Lobby:
    def __init__(self, _lobbyID: int, max_players: int = 2):
        """
        Creates a lobby to play a game
        :param _lobbyID: int
        :param max_players: int
        """
        self.lobbyID = _lobbyID
        self.max_players = max_players
        self.all_players = list()
        self.all_grids = dict()
        self.all_guessed = dict()
        self.start = False
        self.current_turn = set()
        self.status = LobbyStatus.WAIT_FOR_PLAYERS

    def add_player(self, player_id: int, username: str):
        """
        Add a new player in the lobby if lobby not full
        :param player_id: int
        :param username: str
        :return: None
        """
        if not self.is_full():
            self.all_players.append((player_id, username))
            print(f"[LOBBY] {username} is connected in lobby number {self.lobbyID}")
            if self.all_players.__len__() == 1:
                self.current_turn = username
            if self.is_full():
                self.status = LobbyStatus.WAIT_FOR_GRIDS

    def change_turn(self):
        if self.current_turn == self.all_players[0][1]:
            self.current_turn = self.all_players[1][1]
        elif self.current_turn == self.all_players[1][1]:
            self.current_turn = self.all_players[0][1]
        print("Current turn:" + str(self.current_turn))

    def add_grid_player(self, player_id: int, grid: np.ndarray):
        self.all_grids[str(player_id)] = grid
        self.add_guessed_grid(player_id)
        if self.all_players.__len__() == self.all_grids.__len__() == self.max_players:
            self.start = True

    def add_guessed_grid(self, player_id: int):
        self.all_guessed[str(player_id)] = np.full(GRID_SIZE, GridCellType.water.value, dtype=int)

    def is_full(self):
        return self.max_players == len(self.all_players)

    def get_number_players_connected(self):
        return len(self.all_players)

    def remove_player(self, playerID: int, username: str):
        """
        Remove player from all_players dict
        :param playerID: int
        :return: None
        """
        self.all_players.remove((playerID, username))
        del self.all_grids[str(playerID)]
